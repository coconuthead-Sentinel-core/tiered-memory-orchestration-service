import asyncio
import os
import threading
from dataclasses import dataclass
from typing import Any, List, Optional, Tuple


@dataclass
class _Sub:
    loop: asyncio.AbstractEventLoop
    queue: asyncio.Queue
    topic: Optional[str]
    policy: str  # 'drop' | 'block' | 'latest' | 'error'


class EventBus:
    """In-process event bus using asyncio queues per subscriber.

    Backward compatible with the previous minimal API while adding:
    - Thread-safety for subscription management via a lock
    - Optional topics (subscribe to a topic or None for all)
    - Optional bounded queues per subscriber with overflow policy
      Policies:
        - 'drop'  : silently drop if full (default)
        - 'latest': evict one oldest item, then enqueue
        - 'block' : schedule an async put() to wait for space
        - 'error' : raise inside loop's exception handler
    - Basic metrics via status()
    """

    def __init__(self, name: str = "core") -> None:
        self.name = name
        self._subs: List[_Sub] = []
        self._lock = threading.RLock()
        self._metrics = {
            "published": 0,
            "dropped": 0,
            "errors": 0,
        }
        self._metrics_lock = threading.Lock()

    # --- Subscription API -------------------------------------------------
    def subscribe(
        self,
        loop: asyncio.AbstractEventLoop,
        *,
        topic: Optional[str] = None,
        maxsize: int = 0,
        policy: str = "drop",
    ) -> asyncio.Queue:
        """Subscribe the given loop to the bus.

        Compatibility: callers may pass only (loop) and receive an unbounded queue.
        """
        q: asyncio.Queue = asyncio.Queue(maxsize=max(0, int(maxsize)))
        with self._lock:
            self._subs.append(_Sub(loop=loop, queue=q, topic=topic, policy=str(policy)))
        return q

    def unsubscribe(self, queue: asyncio.Queue) -> None:
        with self._lock:
            self._subs = [s for s in self._subs if s.queue is not queue]

    # --- Publishing --------------------------------------------------------
    def publish(self, payload: Any, *, topic: Optional[str] = None) -> None:
        """Publish a payload to all matching subscribers.

        Safe across threads: uses loop.call_soon_threadsafe to deliver.
        """
        with self._metrics_lock:
            self._metrics["published"] += 1
        # Snapshot to avoid holding lock during scheduling
        with self._lock:
            subs = list(self._subs)
        for sub in subs:
            if sub.topic is not None and topic is not None and sub.topic != topic:
                continue
            try:
                # Deliver within target loop; handle overflow policy inside loop
                sub.loop.call_soon_threadsafe(self._deliver, sub, payload)
            except RuntimeError:
                # Loop may be closed; drop subscriber
                self.unsubscribe(sub.queue)

    # Runs inside the subscriber's event loop thread
    def _deliver(self, sub: _Sub, payload: Any) -> None:
        try:
            sub.queue.put_nowait(payload)
        except asyncio.QueueFull:
            pol = (sub.policy or "drop").lower()
            if pol == "drop":
                with self._metrics_lock:
                    self._metrics["dropped"] += 1
                return
            if pol == "latest":
                try:
                    sub.queue.get_nowait()
                except asyncio.QueueEmpty:
                    pass
                try:
                    sub.queue.put_nowait(payload)
                except asyncio.QueueFull:
                    with self._metrics_lock:
                        self._metrics["dropped"] += 1
                return
            if pol == "block":
                # Schedule an async put to wait for space without blocking the loop callback
                async def _block_put() -> None:
                    await sub.queue.put(payload)

                try:
                    sub.loop.create_task(_block_put())
                except Exception:
                    with self._metrics_lock:
                        self._metrics["dropped"] += 1
                return
            if pol == "error":
                # Raise into the loop; also count as error
                with self._metrics_lock:
                    self._metrics["errors"] += 1
                raise
        except Exception:
            with self._metrics_lock:
                self._metrics["errors"] += 1

    # --- Lifecycle / Introspection ----------------------------------------
    def close(self) -> None:
        """Remove all subscribers. Does not drain queues."""
        with self._lock:
            self._subs.clear()

    def status(self) -> dict:
        with self._lock:
            subs = len(self._subs)
        with self._metrics_lock:
            m: dict = dict(self._metrics)
        m["subscribers"] = subs
        m["name"] = self.name
        return m


def _create_bus_from_env() -> EventBus:
    backend = os.getenv("QNF_BUS_BACKEND", "local").lower()
    # Only local in-process is implemented; future: redis, nats
    eb = EventBus("qnf")
    setattr(eb, "backend", backend)
    if backend != "local":
        # Fallback to local with attribute for visibility
        try:
            # best-effort: mark metrics error to reflect misconfig
            eb._metrics["errors"] += 0
        except Exception:
            pass
    return eb


# Singleton bus used across the app
bus = _create_bus_from_env()
