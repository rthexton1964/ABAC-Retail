"""Authorization request and decision models."""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
from app.models.user import User
from app.models.account import Account


@dataclass
class Environment:
    """Environmental attributes for authorization."""
    timestamp: datetime
    ip_address: Optional[str] = None
    location: Optional[str] = None
    business_hours: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            'timestamp': self.timestamp.isoformat(),
            'ip_address': self.ip_address,
            'location': self.location,
            'business_hours': self.business_hours
        }


@dataclass
class ActionAttributes:
    """Action attributes for authorization."""
    amount: Optional[float] = None
    type: str = ''

    def to_dict(self) -> Dict[str, Any]:
        return {
            'amount': self.amount,
            'type': self.type
        }


@dataclass
class AuthorizationRequest:
    """Authorization request containing all attributes."""
    user: User
    action: str
    resource: Account
    environment: Environment
    action_attributes: ActionAttributes

    def to_dict(self) -> Dict[str, Any]:
        return {
            'user': self.user.to_dict(),
            'action': self.action,
            'resource': self.resource.to_dict(),
            'environment': self.environment.to_dict(),
            'action_attributes': self.action_attributes.to_dict()
        }


@dataclass
class AuthorizationDecision:
    """Authorization decision with reasoning."""
    decision: str  # 'permit' or 'deny'
    reason: str
    evaluated_rules: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    request: Optional[AuthorizationRequest] = None

    def to_dict(self) -> Dict[str, Any]:
        result = {
            'decision': self.decision,
            'reason': self.reason,
            'evaluated_rules': self.evaluated_rules,
            'timestamp': self.timestamp.isoformat()
        }
        if self.request:
            result['request'] = self.request.to_dict()
        return result
