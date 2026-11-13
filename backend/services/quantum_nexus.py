from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

import yaml


@dataclass(frozen=True)
class GreatGreg:
    cell: str
    r: int
    c: int
    node: int
    label: str


class QuantumNexus:
    """
    Loads the Quantum Nexus blueprint and exposes dependency and coordinate helpers.
    """

    def __init__(self, blueprint: Dict[str, Any]):
        self.bp = blueprint
        self._rc_map = (blueprint.get("great_greg_coordinates", {}) or {}).get(
            "rc_map", {}
        ) or {}
        self._deps = {
            d["id"]: d
            for d in (blueprint.get("dependencies") or [])
            if isinstance(d, dict) and "id" in d
        }
        self._nodes = {
            n["id"]: n
            for n in (blueprint.get("nodes") or [])
            if isinstance(n, dict) and "id" in n
        }
        self._cell_lookup = {cell.upper(): info for cell, info in self._rc_map.items()}

    @classmethod
    def from_yaml(cls, path: str | Path) -> "QuantumNexus":
        p = Path(path)
        data = yaml.safe_load(p.read_text(encoding="utf-8"))
        if "quantum_nexus_blueprint" in data:
            data = data["quantum_nexus_blueprint"]
        return cls(data)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "QuantumNexus":
        if "quantum_nexus_blueprint" in data:
            data = data["quantum_nexus_blueprint"]
        return cls(data)

    @property
    def origin(self) -> GreatGreg:
        dep = self._find_dependency_by_type("diagonal_dependency")
        if dep:
            return self.resolve(dep["from"])
        return self.resolve(min(self._cell_lookup, key=self._sort_key))

    @property
    def terminus(self) -> GreatGreg:
        dep = self._find_dependency_by_type("lateral_row_major_dependency")
        if dep:
            return self.resolve(dep["to"])
        return self.resolve(max(self._cell_lookup, key=self._sort_key))

    def dependency(self, dep_id: str) -> Dict[str, Any]:
        if dep_id not in self._deps:
            raise KeyError(f"Dependency not found: {dep_id}")
        return self._deps[dep_id]

    def node(self, node_id: str) -> Dict[str, Any]:
        if node_id not in self._nodes:
            raise KeyError(f"Node not found: {node_id}")
        return self._nodes[node_id]

    def get_node_cells(self, node_id: str) -> List[GreatGreg]:
        node = self.node(node_id)
        return [self.resolve(cell) for cell in node.get("cells", [])]

    def resolve_cell(self, cell: str) -> GreatGreg:
        normalized = cell.strip().upper()
        info = self._cell_lookup.get(normalized)
        if not info:
            raise KeyError(f"Unknown cell: {cell}")
        return GreatGreg(
            cell=normalized,
            r=int(info["r"]),
            c=int(info["c"]),
            node=int(info["node"]),
            label=str(info["label"]),
        )

    def resolve(self, ref: str) -> GreatGreg:
        ref = ref.strip()

        if ":" in ref:
            _, cell = ref.split(":", 1)
            return self.resolve_cell(cell)

        if ".R" in ref.upper() and "C" in ref.upper():
            node_part, rc_part = ref.split(".", 1)
            node = int("".join(ch for ch in node_part if ch.isdigit()))
            rc_part = rc_part.upper().lstrip("R")
            r_str, c_str = rc_part.split("C", 1)
            r, c = int(r_str), int(c_str)
            for cell_name, info in self._cell_lookup.items():
                if (
                    int(info["node"]) == node
                    and int(info["r"]) == r
                    and int(info["c"]) == c
                ):
                    return GreatGreg(
                        cell=cell_name,
                        r=r,
                        c=c,
                        node=node,
                        label=str(info["label"]),
                    )
            raise KeyError(f"No cell found for {ref} (node={node}, r={r}, c={c})")

        return self.resolve_cell(ref)

    def diagonal_trace(self) -> List[GreatGreg]:
        dep = self._find_dependency_by_type("diagonal_dependency")
        if not dep:
            return []
        return [self.resolve(cell) for cell in dep.get("path", [])]

    def lateral_trace(self) -> List[GreatGreg]:
        dep = self._find_dependency_by_type("lateral_row_major_dependency")
        if not dep:
            return []
        ordered_cells: List[str] = []
        for row in dep.get("path", []):
            if isinstance(row, list):
                ordered_cells.extend(row)
            else:
                ordered_cells.append(str(row))
        return [self.resolve(cell) for cell in ordered_cells]

    def to_api_response(self, ref: str) -> Dict[str, Any]:
        coord = self.resolve(ref)
        return {
            "cell": coord.cell,
            "row": coord.r,
            "column": coord.c,
            "node": coord.node,
            "node_id": f"Node_{coord.node}",
            "label": coord.label,
        }

    def _find_dependency_by_type(self, dep_type: str) -> Dict[str, Any] | None:
        for dep in self._deps.values():
            if dep.get("type") == dep_type:
                return dep
        return None

    def _sort_key(self, cell: str) -> tuple[int, int, int]:
        info = self._cell_lookup[cell]
        return int(info["node"]), int(info["r"]), int(info["c"])
