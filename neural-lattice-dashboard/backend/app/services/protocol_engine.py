PROTOCOLS = [
    {
        "id": "PROTO-001",
        "name": "Onset Omega 1",
        "activation_rule": "ALWAYS active",
        "color": "#4CAF50",
    },
    {
        "id": "PROTO-002",
        "name": "Joy Protocol",
        "activation_rule": "IF cognitive_load > 7",
        "color": "#2196F3",
    },
    {
        "id": "PROTO-003",
        "name": "Coconut Head",
        "activation_rule": "IF session active",
        "color": "#FF9800",
    },
]


class ProtocolEngine:
    @staticmethod
    def evaluate(cognitive_load: int = 0, session_active: bool = False) -> list[dict]:
        results = []
        for proto in PROTOCOLS:
            if proto["id"] == "PROTO-001":
                status = "ACTIVE"
            elif proto["id"] == "PROTO-002":
                status = "ACTIVE" if cognitive_load > 7 else "STANDBY"
            elif proto["id"] == "PROTO-003":
                status = "ACTIVE" if session_active else "STANDBY"
            else:
                status = "STANDBY"
            results.append({**proto, "status": status})
        return results

    @staticmethod
    def has_conflicts(active_protocols: list[dict]) -> bool:
        active_ids = {p["id"] for p in active_protocols if p["status"] == "ACTIVE"}
        return False if "PROTO-001" in active_ids or not active_ids else False
