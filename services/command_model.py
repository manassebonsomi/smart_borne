from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Command:
    """
    Représentation structurée d'une commande.
    Cette classe constitue le pont entre
    le Parser LL(1) et la couche d'exécution.
    """

    action: str
    subject: Optional[str] = None
    arguments: Dict[str, Any] = field(default_factory=dict)
    tokens: List[Any] = field(default_factory=list)
    raw: Optional[str] = None

    # DICTIONNAIRE
    def to_dict(self):
        """
        Transforme la commande en dictionnaire.
        """
        return {
            "action": self.action,
            "subject": self.subject,
            "arguments": self.arguments,
            "raw": self.raw
        }

    # AFFICHAGE
    def __repr__(self):
        return (
            "Command("
            f"action={self.action!r}, "
            f"subject={self.subject!r}, "
            f"arguments={self.arguments!r}"
            ")"
        )