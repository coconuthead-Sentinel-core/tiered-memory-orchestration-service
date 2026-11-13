"""
L1 Brain Stem: Hardware Abstraction Layer (HAL)
Grid Coordinate: Grid Alpha (F5-I8)
Anchors autonomic knowledge to shield logic from platform amnesia.
"""

import logging
import platform

import psutil

logger = logging.getLogger(__name__)


class HAL:
    def __init__(self):
        self.coordinate = "Grid Alpha (F5-I8)"
        self.system_info = self._get_system_info()
        logger.info(f"🔌 HAL Initialized at {self.coordinate}")

    def _get_system_info(self):
        return {
            "system": platform.system(),
            "node": platform.node(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "cpu_count": psutil.cpu_count(),
            "memory_total": psutil.virtual_memory().total,
        }

    def get_anchor_status(self):
        return {
            "status": "ANCHORED",
            "layer": "L1 Brain Stem",
            "coordinate": self.coordinate,
            "persistence": "AUTONOMIC",
        }


hal = HAL()
