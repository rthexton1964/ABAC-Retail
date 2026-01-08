"""Transaction model with ABAC attributes."""

from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class TransactionAttributes:
    """Transaction attributes for ABAC authorization."""
    type: str
    amount: Optional[float]
    timestamp: datetime
    source_account: Optional[str] = None
    target_account: Optional[str] = None

    VALID_TYPES = {
        'deposit', 'withdrawal', 'transfer', 'view_balance', 
        'view_history', 'freeze_account', 'close_account', 'approve_loan'
    }

    def __post_init__(self):
        """Validate attribute values."""
        if self.type not in self.VALID_TYPES:
            raise ValueError(f"Invalid transaction type: {self.type}. Must be one of {self.VALID_TYPES}")
        
        if self.amount is not None and not isinstance(self.amount, (int, float)):
            raise ValueError(f"Invalid amount: {self.amount}. Must be a number or None")
        
        if self.amount is not None and self.amount < 0:
            raise ValueError(f"Invalid amount: {self.amount}. Must be non-negative")

    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': self.type,
            'amount': self.amount,
            'timestamp': self.timestamp.isoformat(),
            'source_account': self.source_account,
            'target_account': self.target_account
        }


@dataclass
class Transaction:
    """Transaction model with ABAC attributes."""
    id: str
    attributes: TransactionAttributes

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'attributes': self.attributes.to_dict()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Transaction':
        """Create Transaction from dictionary."""
        attrs = data['attributes']
        timestamp = datetime.fromisoformat(attrs['timestamp']) if isinstance(attrs['timestamp'], str) else attrs['timestamp']
        
        attributes = TransactionAttributes(
            type=attrs['type'],
            amount=attrs.get('amount'),
            timestamp=timestamp,
            source_account=attrs.get('source_account'),
            target_account=attrs.get('target_account')
        )
        return cls(
            id=data['id'],
            attributes=attributes
        )
