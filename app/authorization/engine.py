"""Authorization engine for ABAC evaluation."""

from typing import List
from datetime import datetime
from app.authorization.models import AuthorizationRequest, AuthorizationDecision
from app.authorization.rules import AuthorizationRule


class AuthorizationEngine:
    """ABAC authorization engine."""

    def __init__(self):
        self.rules: List[AuthorizationRule] = []

    def add_rule(self, rule: AuthorizationRule):
        """Add an authorization rule."""
        self.rules.append(rule)
        # Sort rules by priority (higher priority first)
        self.rules.sort(key=lambda r: r.priority, reverse=True)

    def get_rules(self) -> List[AuthorizationRule]:
        """Get all authorization rules."""
        return self.rules.copy()

    def evaluate(self, request: AuthorizationRequest) -> AuthorizationDecision:
        """Evaluate authorization request against all rules."""
        evaluated_rules = []
        
        # Default deny
        decision = 'deny'
        reason = 'No applicable rules found'
        
        # Evaluate rules in priority order
        for rule in self.rules:
            if rule.evaluate(request):
                evaluated_rules.append(rule.name)
                
                if rule.effect == 'permit':
                    decision = 'permit'
                    reason = f'Permitted by rule: {rule.name}'
                    break  # First permit wins
                elif rule.effect == 'deny':
                    decision = 'deny'
                    reason = f'Denied by rule: {rule.name}'
                    break  # First deny wins
        
        return AuthorizationDecision(
            decision=decision,
            reason=reason,
            evaluated_rules=evaluated_rules,
            timestamp=datetime.now(),
            request=request
        )
