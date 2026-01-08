"""Resource model for Retail-ABAC."""

from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class TransactionAttributes:
    """Transaction attributes."""
    resource_type: str
    owner_id: str
    status: str
    sensitivity_level: int
    location: str

    VALID_TYPES = {"type_a", "type_b", "type_c"}
    VALID_STATUSES = {"active", "inactive", "pending", "archived"}

    def __post_init__(self):
        if self.resource_type not in self.VALID_TYPES:
            raise ValueError(f"Invalid resource_type: {self.resource_type}")
        if self.status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status: {self.status}")

    def to_dict(self) -> Dict[str, Any]:
        return {
            'resource_type': self.resource_type,
            'owner_id': self.owner_id,
            'status': self.status,
            'sensitivity_level': self.sensitivity_level,
            'location': self.location
        }


@dataclass
class Transaction:
    """Transaction resource."""
    id: str
    attributes: TransactionAttributes

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'attributes': self.attributes.to_dict()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Transaction':
        attributes = TransactionAttributes(**data['attributes'])
        return cls(id=data['id'], attributes=attributes)
