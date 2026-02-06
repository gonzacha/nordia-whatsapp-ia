from dataclasses import dataclass
from typing import List, Optional


@dataclass
class HandlerResult:
    """Resultado estructurado de un handler."""
    reply: str
    next_state: Optional[str] = None
    side_effects: List[str] = None  # Futuro: eventos

    def __post_init__(self):
        if self.side_effects is None:
            self.side_effects = []
