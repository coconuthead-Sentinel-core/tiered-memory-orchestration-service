import asyncio
import logging
import math
import random
from typing import Any, Dict

from backend.eventbus import bus

logger = logging.getLogger(__name__)


class CNOAXMetacognitionEngine:
    """
    CNO-AX Metacognition Engine

    Responsible for:
    1. Real-time Urban Traffic Optimization Loop.
    2. Metacognitive analysis of system performance.
    3. Generating '1000 Strikes' simulation data for the Sentient City.
    """

    def __init__(self):
        self.active = False
        self.optimization_loop_task = None

    async def start_traffic_optimization_loop(self):
        """Initiates the 1000 Strikes protocol for traffic optimization."""
        if self.active:
            logger.warning("CNO-AX Engine already active.")
            return

        self.active = True
        logger.info("CNO-AX Metacognition Engine: ACTIVATED. Protocol: 1000 Strikes.")
        self.optimization_loop_task = asyncio.create_task(self._run_loop())

    async def stop_traffic_optimization_loop(self):
        """Stops the optimization loop."""
        self.active = False
        if self.optimization_loop_task:
            self.optimization_loop_task.cancel()
            try:
                await self.optimization_loop_task
            except asyncio.CancelledError:
                pass
        logger.info("CNO-AX Metacognition Engine: DEACTIVATED.")

    async def _run_loop(self):
        """Internal loop generating traffic data and optimization events."""
        strike_count = 0
        try:
            while self.active and strike_count < 1000:
                strike_count += 1

                # Simulate Traffic Data
                # Golden Ratio Phi for "natural" flow
                phi = 1.61803398875
                time_factor = asyncio.get_running_loop().time()

                # Traffic Flow (sinusoidal with phi resonance)
                flow = 500 + 200 * math.sin(time_factor / phi) + random.randint(-20, 20)

                # Optimization Metric (Efficiency)
                efficiency = 0.85 + 0.1 * math.cos(time_factor / (phi * 2))

                # Generate Event Data
                event_data = {
                    "strike_id": strike_count,
                    "type": "traffic.optimization",
                    "metrics": {
                        "flow_rate": round(flow, 2),
                        "efficiency": round(efficiency, 4),
                        "congestion_level": round(1.0 - efficiency, 4),
                        "active_nodes": 144,  # 12 * 12
                        "optimization_strategy": "Recursive Phi-Balancing",
                    },
                    "metacognition": {
                        "intent": "Harmonize Urban Flow",
                        "status": "OPTIMIZING",
                    },
                }

                # Publish to Event Bus (Topic: 'cognitive' or 'city')
                # Using 'cognitive' as it's already wired to the dashboard
                bus.publish(
                    {"type": "cno_ax.traffic_update", "data": event_data},
                    topic="cognitive",
                )

                # Log occasionally
                if strike_count % 50 == 0:
                    logger.info(
                        f"CNO-AX Strike {strike_count}: Efficiency {efficiency:.2f}"
                    )

                # High frequency updates for "Real-Time" feel (approx 100ms)
                await asyncio.sleep(0.1)

            # Completion
            bus.publish(
                {
                    "type": "cno_ax.complete",
                    "data": {
                        "strikes_completed": strike_count,
                        "status": "STILLWATER_STATE_ACHIEVED",
                    },
                },
                topic="cognitive",
            )
            logger.info("CNO-AX Protocol Complete: Stillwater State Achieved.")
            self.active = False

        except Exception as e:
            logger.error(f"CNO-AX Engine Error: {e}")
            self.active = False


# Singleton Instance
cno_ax_engine = CNOAXMetacognitionEngine()
