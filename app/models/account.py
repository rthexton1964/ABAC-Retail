"""Account model with ABAC attributes."""

from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class AccountAttributes:
    """Account attributes for ABAC authorization."""
    type: str
    balance: float
    owner: str  # user id
    branch: str
    status: str

    VALID_TYPES = {'checking', 'savings', 'loan', 'investment', 'business'}
    VALID_STATUSES = {'active', 'frozen', 'under_review', 'closed'}

    def __post_init__(self):
        """Validate attribute values."""
        if self.type not in self.VALID_TYPES:
            raise ValueError(f"Invalid account type: {self.type}. Must be one of {self.VALID_TYPES}")
        
        if self.status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status: {self.status}. Must be one of {self.VALID_STATUSES}")
        
        if not isinstance(self.balance, (int, float)):
            raise ValueError(f"Invalid balance: {self.balance}. Must be a number")

    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': self.type,
            'balance': self.balance,
            'owner': self.owner,
            'branch': self.branch,
            'status': self.status
        }


@dataclass
class Account:
    """Account model with ABAC attributes."""
    id: str
    attributes: AccountAttributes

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'attributes': self.attributes.to_dict()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Account':
        """Create Account from dictionary."""
        attributes = AccountAttributes(**data['attributes'])
        return cls(
            id=data['id'],
            attributes=attributes
        )
