"""User model with ABAC attributes."""

from typing import Dict, Any
from dataclasses import dataclass, asdict


@dataclass
class Location:
    """User location attributes."""
    branch: str
    region: str
    country: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class UserAttributes:
    """User attributes for ABAC authorization."""
    department: str
    seniority: str
    location: Location
    clearance_level: int

    VALID_DEPARTMENTS = {'teller', 'loan_officer', 'branch_manager', 'auditor', 'customer_service', 'customer'}
    VALID_SENIORITY = {'junior', 'mid', 'senior', 'executive'}

    def __post_init__(self):
        """Validate attribute values."""
        if self.department not in self.VALID_DEPARTMENTS:
            raise ValueError(f"Invalid department: {self.department}. Must be one of {self.VALID_DEPARTMENTS}")
        
        if self.seniority not in self.VALID_SENIORITY:
            raise ValueError(f"Invalid seniority: {self.seniority}. Must be one of {self.VALID_SENIORITY}")
        
        if not isinstance(self.clearance_level, int) or not (1 <= self.clearance_level <= 5):
            raise ValueError(f"Invalid clearance_level: {self.clearance_level}. Must be an integer between 1 and 5")

    def to_dict(self) -> Dict[str, Any]:
        return {
            'department': self.department,
            'seniority': self.seniority,
            'location': self.location.to_dict(),
            'clearance_level': self.clearance_level
        }


@dataclass
class User:
    """User model with ABAC attributes."""
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
        """Create User from dictionary."""
        location = Location(**data['attributes']['location'])
        attributes = UserAttributes(
            department=data['attributes']['department'],
            seniority=data['attributes']['seniority'],
            location=location,
            clearance_level=data['attributes']['clearance_level']
        )
        return cls(
            id=data['id'],
            name=data['name'],
            attributes=attributes
        )
