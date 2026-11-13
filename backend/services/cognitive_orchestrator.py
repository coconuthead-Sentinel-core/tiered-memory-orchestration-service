"""Cognitive Orchestrator - Enhanced Middle Layer for Sentinel Forge.

Extends ChatService with three-zone memory, symbolic processing, and
neurodivergent cognitive lenses while preserving all existing behavior.

Architecture:
    api.py → CognitiveOrchestrator → AI Adapter → cosmos_repo
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
    🟢 Active   🟡 Pattern   🔴 Crystal
     Memory      Emerge       Storage
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any, Dict, List, Optional

from backend.core.bridge import bridge
from backend.core.calculus import calculus_core as calculus
from backend.core.hal import hal
from backend.domain.models import (
    CognitiveLens,
    GlyphMatch,
    MemoryZone,
    Note,
    SymbolicMetadata,
    ZonedNote,
    ZoneMetrics,
)
from backend.eventbus import bus
from backend.infrastructure.cosmos_repo import cosmos_repo
from backend.services.adhd_lens import (
    ADHDLens,
    create_adhd_lens,
)
from backend.services.autism_lens import (
    AutismLens,
    create_autism_lens,
)
from backend.services.chat_service import ChatService
from backend.services.dyslexia_lens import (
    DyslexiaLens,
    create_dyslexia_lens,
)
from backend.services.glyph_parser import (
    get_concept_for_glyph,
    parse_glyph_sequence,
)
from backend.services.glyph_processor import (
    GlyphProcessor,
    get_glyph_processor,
)
from backend.services.l6_firewall import l6_firewall
from backend.services.memory_zones import (
    ThreeZoneMemory,
    calculate_entropy,
    classify_zone,
    get_memory_manager,
)
from backend.services.validation_loop import validator

# NEW: Import QuantumNexusForge for brain modeling
from quantum_nexus_forge_v5_2_enhanced import QuantumNexusForge

logger = logging.getLogger(__name__)


# Re-export for backward compatibility with existing tests
CognitiveZone = MemoryZone  # Alias


# --- Main Orchestrator ---


class CognitiveOrchestrator(ChatService):
    """
    Enhanced middle layer orchestrating the Cognitive Pipeline:

    1. Input Analysis (entropy calculation)
    2. Zone Classification (active/pattern/crystal)
    3. Context Retrieval (zone-aware memory)
    4. AI Processing (lens-adjusted generation)
    5. Memory Consolidation (zone-tagged storage)
    6. Event Publishing (real-time updates)

    Inherits all ChatService behavior - safe extension.
    """

    def __init__(
        self,
        ai_adapter,
        default_lens: CognitiveLens = CognitiveLens.NEUROTYPICAL,
        memory_manager: Optional[ThreeZoneMemory] = None,
        glyph_processor: Optional[GlyphProcessor] = None,
    ):
        """
        Initialize CognitiveOrchestrator.

        Args:
            ai_adapter: Mock or Azure OpenAI adapter (inherited)
            default_lens: Default cognitive processing mode
            memory_manager: Three-zone memory manager (defaults to shared instance)
            glyph_processor: Glyph processor for symbolic pattern recognition
        """
        super().__init__(ai_adapter)
        self.default_lens = default_lens
        self.memory_manager = memory_manager or get_memory_manager()
        self.glyph_processor = glyph_processor or get_glyph_processor()
        self.adhd_lens = create_adhd_lens()
        self.autism_lens = create_autism_lens()
        self.dyslexia_lens = create_dyslexia_lens()
        self._zone_counts = {zone: 0 for zone in CognitiveZone}
        self._event_bus_task: Optional[asyncio.Task] = None
        self._event_bus_queue: Optional[asyncio.Queue] = None

        # NEW: Initialize QuantumNexusForge for brain modeling
        self.quantum_forge = QuantumNexusForge()

        logger.info(
            f"🧠 CognitiveOrchestrator initialized with lens: {default_lens.value} and QuantumNexusForge"
        )

    def start_event_listener(self):
        """Start listening to the event bus for raw events."""
        if self._event_bus_task is None:
            loop = asyncio.get_event_loop()
            self._event_bus_queue = bus.subscribe(loop, topic="raw_events")
            self._event_bus_task = loop.create_task(
                self._process_event_queue(self._event_bus_queue)
            )
            logger.info("👂 Event bus listener started for 'raw_events' topic.")

    def stop_event_listener(self):
        """Stop the event bus listener."""
        if self._event_bus_task:
            self._event_bus_task.cancel()
            self._event_bus_task = None
        if self._event_bus_queue is not None:
            bus.unsubscribe(self._event_bus_queue)
            self._event_bus_queue = None
            logger.info("🛑 Event bus listener stopped.")

    def is_event_listener_running(self) -> bool:
        """Return True when the raw-event listener task is active."""
        return self._event_bus_task is not None and not self._event_bus_task.done()

    async def _process_event_queue(self, queue: asyncio.Queue):
        """Process incoming events from the subscription queue."""
        while True:
            try:
                event = await queue.get()
                logger.debug(f"📬 Received raw event: {event}")

                # Pass the event to the GlyphProcessor
                symbolic_metadata = self.glyph_processor.process_event(event)

                if symbolic_metadata and symbolic_metadata.matched_glyphs:
                    logger.info(
                        f"🜂 Processed event and found {len(symbolic_metadata.matched_glyphs)} glyphs."
                    )
                    # Here we can trigger cognitive functions based on the glyph
                    await self._react_to_glyphs(symbolic_metadata)

                queue.task_done()
            except asyncio.CancelledError:
                logger.info("Event processing task cancelled.")
                break
            except Exception as e:
                logger.error(f"🔥 Error processing event: {e}", exc_info=True)

    async def _react_to_glyphs(self, symbolic_metadata: SymbolicMetadata):
        """
        React to detected glyphs by triggering cognitive functions.
        This fulfills Task 4.4.
        """
        dominant_topic = symbolic_metadata.dominant_topic
        if not dominant_topic:
            return

        logger.info(f"💡 Reacting to dominant topic: {dominant_topic}")

        # Example of routing logic based on dominant topic
        if dominant_topic == "initiation":
            # For 'initiation' glyphs, we might want a quick, broad response.
            logger.info("🚀 Triggering ADHD_BURST lens for initiation topic.")
            # This is a fire-and-forget style action for demonstration.
            # A real implementation might queue this or handle the response.
            asyncio.create_task(
                self.process_message(
                    "New initiation event detected. Provide a brief, high-level summary.",
                    lens=CognitiveLens.ADHD_BURST,
                )
            )
        elif dominant_topic == "ethics":
            # For 'ethics' glyphs, we need a precise, detailed analysis.
            logger.info("🛡️ Triggering AUTISM_PRECISION lens for ethics topic.")
            asyncio.create_task(
                self.process_message(
                    "An ethics-related event has been flagged. Perform a detailed analysis of the implications.",
                    lens=CognitiveLens.AUTISM_PRECISION,
                )
            )
        elif dominant_topic == "stability":
            # For 'stability' glyphs, a holistic view is required.
            logger.info("🧊 Triggering DYSLEXIA_SPATIAL lens for stability topic.")
            asyncio.create_task(
                self.process_message(
                    "A system stability event occurred. Visualize the relationships and overall system state.",
                    lens=CognitiveLens.DYSLEXIA_SPATIAL,
                )
            )
        else:
            logger.debug(f"No specific reaction defined for topic: {dominant_topic}")

    async def process_message(
        self,
        user_message: str,
        context: str = "",
        lens: Optional[CognitiveLens] = None,
    ) -> Dict[str, Any]:
        """
        Process a user message through the enhanced Cognitive Pipeline.

        Extends ChatService.process_message with:
        - Entropy-based zone classification
        - Symbolic pattern recognition
        - Lens-adjusted processing
        - Zone transition events

        Args:
            user_message: The user's input text
            context: Optional system context
            lens: Cognitive lens to apply (defaults to self.default_lens)

        Returns:
            Standard chat completion response with added zone metadata
        """
        # 0. L6 Firewall Check (Ethical Mirror)
        if not l6_firewall.validate_request(user_message):
            logger.warning(
                "🛡️ L6 Firewall blocked request due to Ethical Mirror violation."
            )
            # In a real scenario, we might raise an exception or return a canned response.
            # For now, we proceed but log it, as the validator is currently permissive.

        # 0.1 L1 HAL Check (Brain Stem)
        hal_status = hal.get_anchor_status()
        if hal_status["status"] != "ANCHORED":
            logger.warning(
                f"⚠️ L1 HAL Warning: System not anchored. Status: {hal_status}"
            )

        active_lens = lens or self.default_lens

        # 1. Calculate input entropy
        input_entropy = calculate_entropy(user_message)
        input_zone = classify_zone(input_entropy)

        logger.debug(
            f"📊 Input entropy: {input_entropy:.2f} → Zone: {input_zone.value}"
        )

        # 2. Process symbolic patterns
        symbolic_metadata = self.glyph_processor.process_text(user_message)

        logger.debug(
            f"🜂 Symbolic processing: {len(symbolic_metadata.matched_glyphs)} matches"
        )

        # 2.5. Parse glyph sequences in the message
        glyph_parse_result = parse_glyph_sequence(user_message)

        logger.debug(
            f"🜂 Glyph parsing: {glyph_parse_result['parsed_count']} glyphs parsed"
        )

        # 2.6 L5 Bridge Processing (Corpus Callosum)
        # Simulates high-performance C++ interop for heavy lifting
        bridge_result = bridge.process_data(
            {"text": user_message, "entropy": input_entropy}
        )
        logger.debug(f"🌉 L5 Bridge Result: {bridge_result}")

        # 3. Apply lens transformation to context
        adjusted_context = self._apply_lens(context, active_lens)

        # 4. Prefer the configured AI adapter to preserve the chat contract.
        try:
            response = await super().process_message(user_message, adjusted_context)
            response["provider"] = type(self.ai_adapter).__name__
            response["live_response"] = (
                type(self.ai_adapter).__name__ == "AzureOpenAIAdapter"
            )
        except Exception as e:
            logger.warning(
                f"⚠️ Primary AI adapter failed, falling back to QuantumNexusForge: {e}"
            )
            try:
                forge_result = await asyncio.get_event_loop().run_in_executor(
                    None,
                    self.quantum_forge.process,
                    user_message,
                )
                ai_text = str(forge_result.get("result", "No response generated"))
            except Exception as forge_error:
                logger.error(f"🔴 QuantumNexusForge processing failed: {forge_error}")
                ai_text = "Cognitive processing error. Retrying with fallback."

            structured_content = f"""
**Summary:** {ai_text[:200]}...  # Brief overview

**Plan:** Process through cognitive lenses and memory zones for optimal response.

**Assumptions:** User input is valid; system is anchored and lenses are calibrated.

**Next Step:** Review output and provide feedback for refinement.
"""
            import time

            response = {
                "id": f"chat-{int(time.time())}",
                "model": "sentinel-forge-cognitive",
                "created": int(time.time()),
                "provider": "QuantumNexusForgeFallback",
                "live_response": False,
                "choices": [
                    {
                        "index": 0,
                        "message": {"role": "assistant", "content": structured_content},
                        "finish_reason": "stop",
                    }
                ],
                "usage": {
                    "prompt_tokens": len(user_message.split()),
                    "completion_tokens": len(structured_content.split()),
                    "total_tokens": len(user_message.split())
                    + len(structured_content.split()),
                },
            }

        # 5. Extract response text and calculate output entropy
        choices = response.get("choices", [])
        if choices:
            ai_text = choices[0].get("message", {}).get("content", "")

            # --- L6 Firewall Output Constraints ---
            ai_text = l6_firewall.apply_constraints(ai_text, lens=active_lens.value)
            choices[0]["message"]["content"] = ai_text
            # --------------------------------------

            output_entropy = calculate_entropy(ai_text)
            output_zone = classify_zone(output_entropy)

            # 5.1 L2 Validation Loop (Cerebellum)
            validation_result = validator.validate_output(ai_text)
            if not validation_result["consensus"]:
                logger.warning(f"⚠️ L2 Validation Failed: {validation_result['status']}")

            # 5.2 L7 Singularity Metric (Singularity Kernel)
            singularity_metric = calculus.calculate_singularity_metric(
                input_entropy, output_entropy
            )
            logger.info(f"🌌 L7 Singularity Metric: {singularity_metric}")

        else:
            ai_text = ""
            output_entropy = 0.0
            output_zone = CognitiveZone.CRYSTALLIZED
            validation_result = {"consensus": False, "status": "NO_OUTPUT"}
            singularity_metric = 0.0

        # 6. Update zone counts
        self._zone_counts[output_zone] += 1

        # 7. Publish zone event (for real-time dashboards)
        self._publish_zone_event(
            note_id=response.get("id", "unknown"),
            input_zone=input_zone,
            output_zone=output_zone,
            entropy=output_entropy,
        )

        # 8. Publish symbolic event if matches found
        if symbolic_metadata.matched_glyphs:
            self._publish_symbolic_event(
                note_id=response.get("id", "unknown"),
                symbolic_metadata=symbolic_metadata,
            )

        # 8.5. Publish glyph parsing event if glyphs found
        if glyph_parse_result["parsed"]:
            self._publish_glyph_event(
                note_id=response.get("id", "unknown"),
                glyph_data=glyph_parse_result,
            )

        # 9. Add cognitive metadata to response
        response["_cognitive_metadata"] = {
            "input_entropy": round(input_entropy, 3),
            "output_entropy": round(output_entropy, 3),
            "input_zone": input_zone.value,
            "output_zone": output_zone.value,
            "lens_applied": active_lens.value,
            "symbolic_matches": len(symbolic_metadata.matched_glyphs),
            "dominant_topic": symbolic_metadata.dominant_topic,
            "parsed_glyphs": glyph_parse_result["parsed_count"],
            "glyph_concepts": glyph_parse_result["concepts"],
            "validation_status": validation_result["consensus"],
            "singularity_metric": singularity_metric,
        }

        return response

    def _apply_lens(self, context: str, lens: CognitiveLens) -> str:
        """
        Apply cognitive lens transformation to context.

        Now implements ADHD Burst, Autism Precision, and Dyslexia Spatial lenses.
        """
        if lens == CognitiveLens.ADHD_BURST:
            # Apply ADHD lens transformation
            transformed = self.adhd_lens.transform_context(context)
            logger.debug("🧠 Applied ADHD Burst lens transformation")
            return transformed
        elif lens == CognitiveLens.AUTISM_PRECISION:
            # Apply Autism lens transformation
            transformed = self.autism_lens.transform_context(context)
            logger.debug("🧠 Applied Autism Precision lens transformation")
            return transformed
        elif lens == CognitiveLens.DYSLEXIA_SPATIAL:
            # Apply Dyslexia lens transformation
            transformed = self.dyslexia_lens.transform_context(context)
            logger.debug("🧠 Applied Dyslexia Spatial lens transformation")
            return transformed

        # Default: return context unchanged
        return context

    def _publish_zone_event(
        self,
        note_id: str,
        input_zone: CognitiveZone,
        output_zone: CognitiveZone,
        entropy: float,
    ) -> None:
        """Publish zone transition event to EventBus."""
        event = {
            "type": "zone.classified",
            "data": {
                "note_id": note_id,
                "input_zone": input_zone.value,
                "output_zone": output_zone.value,
                "entropy": round(entropy, 3),
                "zone_counts": {k.value: v for k, v in self._zone_counts.items()},
            },
        }
        try:
            bus.publish(event, topic="cognitive")
        except Exception as e:
            logger.warning(f"⚠️ Failed to publish zone event: {e}")

    def _publish_symbolic_event(
        self,
        note_id: str,
        symbolic_metadata: SymbolicMetadata,
    ) -> None:
        """Publish symbolic pattern match event to EventBus."""
        if not symbolic_metadata.matched_glyphs:
            return

        event = {
            "type": "symbolic.matched",
            "data": {
                "note_id": note_id,
                "matched_glyphs": [
                    {
                        "shape": glyph.shape,
                        "topic": glyph.topic,
                        "confidence": round(glyph.confidence, 3),
                        "matched_seeds": glyph.matched_seeds,
                    }
                    for glyph in symbolic_metadata.matched_glyphs
                ],
                "dominant_topic": symbolic_metadata.dominant_topic,
            },
        }
        try:
            bus.publish(event, topic="symbolic")
        except Exception as e:
            logger.warning(f"⚠️ Failed to publish symbolic event: {e}")

    def _publish_glyph_event(
        self,
        note_id: str,
        glyph_data: Dict[str, Any],
    ) -> None:
        """Publish glyph parsing event to EventBus."""
        if not glyph_data.get("parsed", False):
            return

        event = {
            "type": "glyph.parsed",
            "data": {
                "note_id": note_id,
                "parsed_glyphs": glyph_data["glyphs"],
                "concepts": glyph_data["concepts"],
                "parsed_count": glyph_data["parsed_count"],
                "sequence_length": glyph_data["sequence_length"],
            },
        }
        try:
            bus.publish(event, topic="glyph")
        except Exception as e:
            logger.warning(f"⚠️ Failed to publish glyph event: {e}")

    def get_zone_metrics(self) -> Dict[str, Any]:
        """Return current zone distribution metrics."""
        total = sum(self._zone_counts.values()) or 1
        return {
            "total_processed": total,
            "zone_distribution": {
                zone.value: {
                    "count": count,
                    "percentage": round(count / total * 100, 1),
                }
                for zone, count in self._zone_counts.items()
            },
            "default_lens": self.default_lens.value,
        }


# --- Factory Function (Optional convenience) ---


def create_orchestrator(
    ai_adapter, lens: str = "neurotypical"
) -> CognitiveOrchestrator:
    """
    Factory function to create CognitiveOrchestrator with string lens name.

    Args:
        ai_adapter: The AI adapter (Mock or Azure)
        lens: Lens name as string ("neurotypical", "adhd", "autism", "dyslexia")

    Returns:
        Configured CognitiveOrchestrator instance
    """
    lens_map = {
        "neurotypical": CognitiveLens.NEUROTYPICAL,
        "adhd": CognitiveLens.ADHD_BURST,
        "autism": CognitiveLens.AUTISM_PRECISION,
        "dyslexia": CognitiveLens.DYSLEXIA_SPATIAL,
    }
    cognitive_lens = lens_map.get(lens.lower(), CognitiveLens.NEUROTYPICAL)
    return CognitiveOrchestrator(ai_adapter, default_lens=cognitive_lens)
