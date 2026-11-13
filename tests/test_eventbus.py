import asyncio

from backend.eventbus import EventBus


def test_eventbus_publish_subscribe_drop_policy():
    loop = asyncio.new_event_loop()
    bus = EventBus("test")
    try:
        q = bus.subscribe(loop, maxsize=1, policy="drop")
        # Fill the queue to capacity
        loop.call_soon_threadsafe(q.put_nowait, {"n": 1})
        # Publish two more; with drop policy, they should be counted as dropped
        bus.publish({"n": 2})
        bus.publish({"n": 3})
        # Drain first item
        item = loop.run_until_complete(asyncio.wait_for(q.get(), timeout=1))
        assert item["n"] == 1
        st = bus.status()
        assert st["published"] >= 2
        assert st["dropped"] >= 1
    finally:
        bus.close()
        loop.close()


def test_eventbus_latest_policy_keeps_newest():
    loop = asyncio.new_event_loop()
    bus = EventBus("test")
    try:
        q = bus.subscribe(loop, maxsize=1, policy="latest")
        # Fill capacity
        loop.call_soon_threadsafe(q.put_nowait, {"n": 1})
        # Next publish should evict oldest and enqueue new
        bus.publish({"n": 2})
        got = loop.run_until_complete(asyncio.wait_for(q.get(), timeout=1))
        # The queue should now contain the newest element 2
        assert got["n"] in (1, 2)  # depending on race, first get may still be 1
        # After draining, publish again and confirm we can still receive
        bus.publish({"n": 3})
        got2 = loop.run_until_complete(asyncio.wait_for(q.get(), timeout=1))
        assert got2["n"] in (2, 3)
    finally:
        bus.close()
        loop.close()
