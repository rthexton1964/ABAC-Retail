"""Decision logger for authorization decisions."""

import json
from typing import List, Dict, Any, Optional
from datetime import datetime
from app.authorization.models import AuthorizationDecision


class LogQueryFilters:
    """Filters for querying decision logs."""
    
    def __init__(
        self,
        user_id: Optional[str] = None,
        action_type: Optional[str] = None,
        decision: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ):
        self.user_id = user_id
        self.action_type = action_type
        self.decision = decision
        self.start_time = start_time
        self.end_time = end_time


class DecisionStatistics:
    """Statistics about authorization decisions."""
    
    def __init__(
        self,
        total_decisions: int,
        permit_rate: float,
        deny_rate: float,
        by_user_department: Dict[str, int],
        by_action_type: Dict[str, int]
    ):
        self.total_decisions = total_decisions
        self.permit_rate = permit_rate
        self.deny_rate = deny_rate
        self.by_user_department = by_user_department
        self.by_action_type = by_action_type

    def to_dict(self) -> Dict[str, Any]:
        return {
            'total_decisions': self.total_decisions,
            'permit_rate': self.permit_rate,
            'deny_rate': self.deny_rate,
            'by_user_department': self.by_user_department,
            'by_action_type': self.by_action_type
        }


class DecisionLogger:
    """Logger for authorization decisions."""

    def __init__(self):
        self.decisions: List[AuthorizationDecision] = []

    def log(self, decision: AuthorizationDecision):
        """Log an authorization decision."""
        self.decisions.append(decision)

    def query(self, filters: LogQueryFilters) -> List[AuthorizationDecision]:
        """Query decision logs with filters."""
        results = self.decisions

        if filters.user_id:
            results = [d for d in results if d.request and d.request.user.id == filters.user_id]

        if filters.action_type:
            results = [d for d in results if d.request and d.request.action == filters.action_type]

        if filters.decision:
            results = [d for d in results if d.decision == filters.decision]

        if filters.start_time:
            results = [d for d in results if d.timestamp >= filters.start_time]

        if filters.end_time:
            results = [d for d in results if d.timestamp <= filters.end_time]

        return results

    def get_statistics(self) -> DecisionStatistics:
        """Get statistics about authorization decisions."""
        total = len(self.decisions)
        
        if total == 0:
            return DecisionStatistics(
                total_decisions=0,
                permit_rate=0.0,
                deny_rate=0.0,
                by_user_department={},
                by_action_type={}
            )

        permits = sum(1 for d in self.decisions if d.decision == 'permit')
        denies = sum(1 for d in self.decisions if d.decision == 'deny')

        # Count by user department
        by_department: Dict[str, int] = {}
        for decision in self.decisions:
            if decision.request:
                dept = decision.request.user.attributes.department
                by_department[dept] = by_department.get(dept, 0) + 1

        # Count by action type
        by_action: Dict[str, int] = {}
        for decision in self.decisions:
            if decision.request:
                action = decision.request.action
                by_action[action] = by_action.get(action, 0) + 1

        return DecisionStatistics(
            total_decisions=total,
            permit_rate=permits / total,
            deny_rate=denies / total,
            by_user_department=by_department,
            by_action_type=by_action
        )

    def export_logs(self, format: str = 'json') -> str:
        """Export decision logs in specified format."""
        if format != 'json':
            raise ValueError(f"Unsupported format: {format}")

        logs = [d.to_dict() for d in self.decisions]
        return json.dumps(logs, indent=2)

    def clear(self):
        """Clear all logs (useful for testing)."""
        self.decisions.clear()
