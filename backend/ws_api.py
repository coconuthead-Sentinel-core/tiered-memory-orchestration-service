import asyncio
import json
import logging
from typing import Any

from fastapi import (  # type: ignore[reportMissingImports]
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
)

from .eventbus import bus
from .security import websocket_require_api_key
from .service import service

logger = logging.getLogger(__name__)


router = APIRouter()


@router.websocket("/ws/sync")
async def ws_sync(websocket: WebSocket) -> Any:
    """Compatibility stream that forwards all EventBus traffic without an initial snapshot."""
    websocket_require_api_key(websocket)
    await websocket.accept()
    loop = asyncio.get_running_loop()
    queue = bus.subscribe(loop, maxsize=100, policy="latest", topic=None)

    try:
        while True:
            event = await queue.get()
            await websocket.send_json(event)
    except WebSocketDisconnect:
        logger.info("Client disconnected from /ws/sync.")
    except Exception as e:
        logger.error(f"An unexpected error occurred in /ws/sync: {e}", exc_info=True)
    finally:
        bus.unsubscribe(queue)


@router.websocket("/ws/cognitive")
async def ws_cognitive(websocket: WebSocket) -> Any:
    """WebSocket endpoint for real-time cognitive processing events."""
    # Enforce API key if configured
    websocket_require_api_key(websocket)
    await websocket.accept()
    loop = asyncio.get_running_loop()

    # Subscribe to all relevant cognitive event topics
    cognitive_queue = bus.subscribe(
        loop, maxsize=100, policy="latest", topic="cognitive"
    )
    symbolic_queue = bus.subscribe(loop, maxsize=100, policy="latest", topic="symbolic")
    glyph_queue = bus.subscribe(loop, maxsize=100, policy="latest", topic="glyph")

    try:
        # Send initial cognitive state snapshot
        from .services.memory_zones import get_memory_manager

        memory_manager = get_memory_manager()
        zone_metrics = (
            memory_manager.get_zone_metrics()
            if hasattr(memory_manager, "get_zone_metrics")
            else {}
        )

        initial_state = {
            "type": "cognitive.state",
            "data": {
                "zone_metrics": zone_metrics,
                "active_lens": "neurotypical",  # Placeholder for dynamic lens state
                "timestamp": __import__("time").time(),
            },
        }
        await websocket.send_json(initial_state)

        # Create tasks to listen to each queue
        cognitive_task = asyncio.create_task(cognitive_queue.get())
        symbolic_task = asyncio.create_task(symbolic_queue.get())
        glyph_task = asyncio.create_task(glyph_queue.get())

        pending = {cognitive_task, symbolic_task, glyph_task}

        while True:
            # Wait for any of the listening tasks to complete
            done, pending_after = await asyncio.wait(
                pending, return_when=asyncio.FIRST_COMPLETED
            )

            for task in done:
                try:
                    event = task.result()
                    await websocket.send_json(event)
                except Exception as e:
                    logger.warning(f"Error processing WebSocket event: {e}")

                # Reschedule the completed task to listen for the next event
                if task is cognitive_task:
                    cognitive_task = asyncio.create_task(cognitive_queue.get())
                    pending_after.add(cognitive_task)
                elif task is symbolic_task:
                    symbolic_task = asyncio.create_task(symbolic_queue.get())
                    pending_after.add(symbolic_task)
                elif task is glyph_task:
                    glyph_task = asyncio.create_task(glyph_queue.get())
                    pending_after.add(glyph_task)

            pending = pending_after

    except WebSocketDisconnect:
        logger.info("Client disconnected from /ws/cognitive.")
    except Exception as e:
        logger.error(
            f"An unexpected error occurred in /ws/cognitive: {e}", exc_info=True
        )
    finally:
        # Unsubscribe from all event bus topics
        bus.unsubscribe(cognitive_queue)
        bus.unsubscribe(symbolic_queue)
        bus.unsubscribe(glyph_queue)
        # Cancel any pending listener tasks
        for task in pending:
            task.cancel()


@router.websocket("/ws/metrics")
async def websocket_metrics(websocket: WebSocket):
    """WebSocket endpoint for real-time, event-driven metrics streaming."""
    websocket_require_api_key(websocket)
    await websocket.accept()
    loop = asyncio.get_running_loop()

    # Subscribe to the 'cognitive' topic for metrics-related events
    queue = bus.subscribe(loop, maxsize=100, policy="latest", topic="cognitive")

    try:
        # Send an initial snapshot of memory zone metrics
        from .services.memory_zones import get_memory_manager

        memory_manager = get_memory_manager()
        initial_metrics = (
            memory_manager.get_zone_metrics()
            if hasattr(memory_manager, "get_zone_metrics")
            else {}
        )

        await websocket.send_json(
            {
                "type": "metrics.initial_state",
                "data": initial_metrics,
                "timestamp": __import__("time").time(),
            }
        )

        # Listen for and forward relevant real-time events
        while True:
            event = await queue.get()

            # Filter for events that are relevant to metrics
            if event.get("type") in ["zone.classified", "zone.transition"]:
                await websocket.send_json(event)

    except WebSocketDisconnect:
        logger.info("Client disconnected from /ws/metrics.")
    except Exception as e:
        logger.error(f"Error in /ws/metrics endpoint: {e}", exc_info=True)
    finally:
        bus.unsubscribe(queue)
