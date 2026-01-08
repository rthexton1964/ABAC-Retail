"""User model for Retail-ABAC."""

from typing import Dict, Any
from dataclasses import dataclass, asdict


@dataclass
class Location:
    """User location."""
    primary: str
    secondary: str
    region: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class UserAttributes:
    """User attributes for Retail-ABAC."""
    role: str
    level: str
    location: Location
    clearance_level: int

    VALID_ROLES = {"cashier", "manager", "inventory_clerk", "regional_manager"}
    VALID_LEVELS = {"junior", "mid", "senior", "executive"}

    def __post_init__(self):
        if self.role not in self.VALID_ROLES:
            raise ValueError(f"Invalid role: {self.role}")
        if self.level not in self.VALID_LEVELS:
            raise ValueError(f"Invalid level: {self.level}")
        if not isinstance(self.clearance_level, int) or not (1 <= self.clearance_level <= 5):
            raise ValueError(f"Invalid clearance_level: {self.clearance_level}")

    def to_dict(self) -> Dict[str, Any]:
        return {
            'role': self.role,
            'level': self.level,
            'location': self.location.to_dict(),
            'clearance_level': self.clearance_level
        }


@dataclass
class User:
    """User model."""
    id: str
    name: str
    attributes: UserAttributes

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'attributes': self.attributes.to_dict()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        location = Location(**data['attributes']['location'])
        attributes = UserAttributes(
            role=data['attributes']['role'],
            level=data['attributes']['level'],
            location=location,
            clearance_level=data['attributes']['clearance_level']
        )
        return cls(id=data['id'], name=data['name'], attributes=attributes)
