"""Authorization rules for ABAC evaluation."""

from typing import Callable
from dataclasses import dataclass
from app.authorization.models import AuthorizationRequest


@dataclass
class AuthorizationRule:
    """Authorization rule with condition and priority."""
    id: str
    name: str
    condition: Callable[[AuthorizationRequest], bool]
    priority: int
    effect: str = 'permit'  # 'permit' or 'deny'

    def evaluate(self, request: AuthorizationRequest) -> bool:
        """Evaluate the rule condition."""
        try:
            return self.condition(request)
        except Exception:
            # If evaluation fails, rule doesn't apply
            return False
