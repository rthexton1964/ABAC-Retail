"""Banking-specific authorization rules."""

from app.authorization.rules import AuthorizationRule
from app.authorization.models import AuthorizationRequest


def create_teller_rules():
    """Create authorization rules for tellers."""
    rules = []
    
    # Teller can perform small transactions at their branch
    def teller_small_transaction(req: AuthorizationRequest) -> bool:
        return (
            req.user.attributes.department == 'teller' and
            req.user.attributes.location.branch == req.resource.attributes.branch and
            req.action in ['deposit', 'withdrawal', 'view_balance', 'view_history'] and
            (req.action_attributes.amount is None or req.action_attributes.amount < 5000)
        )
    
    rules.append(AuthorizationRule(
        id='teller_small_transaction',
        name='Teller Small Transaction Rule',
        condition=teller_small_transaction,
        priority=100,
        effect='permit'
    ))
    
    # Deny tellers from cross-branch operations
    def teller_cross_branch_deny(req: AuthorizationRequest) -> bool:
        return (
            req.user.attributes.department == 'teller' and
            req.user.attributes.location.branch != req.resource.attributes.branch
        )
    
    rules.append(AuthorizationRule(
        id='teller_cross_branch_deny',
        name='Teller Cross-Branch Restriction',
        condition=teller_cross_branch_deny,
        priority=200,  # Higher priority to deny first
        effect='deny'
    ))
    
    return rules


def create_branch_manager_rules():
    """Create authorization rules for branch managers."""
    rules = []
    
    # Branch manager can approve larger transactions at their branch
    def manager_large_transaction(req: AuthorizationRequest) -> bool:
        return (
            req.user.attributes.department == 'branch_manager' and
            req.user.attributes.location.branch == req.resource.attributes.branch and
            req.action in ['deposit', 'withdrawal', 'transfer'] and
            (req.action_attributes.amount is None or req.action_attributes.amount < 50000)
        )
    
    rules.append(AuthorizationRule(
        id='manager_large_transaction',
        name='Branch Manager Large Transaction Rule',
        condition=manager_large_transaction,
        priority=100,
        effect='permit'
    ))
    
    # Branch manager can freeze accounts at their branch
    def manager_freeze_account(req: AuthorizationRequest) -> bool:
        return (
            req.user.attributes.department == 'branch_manager' and
            req.user.attributes.location.branch == req.resource.attributes.branch and
            req.action == 'freeze_account'
        )
    
    rules.append(AuthorizationRule(
        id='manager_freeze_account',
        name='Branch Manager Account Freeze Rule',
        condition=manager_freeze_account,
        priority=100,
        effect='permit'
    ))
    
    return rules


def create_loan_officer_rules():
    """Create authorization rules for loan officers."""
    rules = []
    
    # Loan officer can approve loans based on seniority
    def loan_officer_approval(req: AuthorizationRequest) -> bool:
        if req.user.attributes.department != 'loan_officer' or req.action != 'approve_loan':
            return False
        
        if req.action_attributes.amount is None:
            return False
        
        # Seniority-based limits
        limits = {
            'junior': 25000,
            'mid': 50000,
            'senior': 100000,
            'executive': 500000
        }
        
        limit = limits.get(req.user.attributes.seniority, 0)
        return req.action_attributes.amount <= limit
    
    rules.append(AuthorizationRule(
        id='loan_officer_approval',
        name='Loan Officer Approval Rule',
        condition=loan_officer_approval,
        priority=100,
        effect='permit'
    ))
    
    return rules


def create_auditor_rules():
    """Create authorization rules for auditors."""
    rules = []
    
    # Auditor can view all accounts but not modify
    def auditor_read_only(req: AuthorizationRequest) -> bool:
        return (
            req.user.attributes.department == 'auditor' and
            req.action in ['view_balance', 'view_history']
        )
    
    rules.append(AuthorizationRule(
        id='auditor_read_only',
        name='Auditor Read-Only Rule',
        condition=auditor_read_only,
        priority=100,
        effect='permit'
    ))
    
    return rules


def create_account_owner_rules():
    """Create authorization rules for account owners."""
    rules = []
    
    # Account owner can perform operations on their own accounts
    def owner_self_service(req: AuthorizationRequest) -> bool:
        return (
            req.user.id == req.resource.attributes.owner and
            req.action in ['deposit', 'withdrawal', 'view_balance', 'view_history'] and
            (req.action_attributes.amount is None or req.action_attributes.amount < 10000)
        )
    
    rules.append(AuthorizationRule(
        id='owner_self_service',
        name='Account Owner Self-Service Rule',
        condition=owner_self_service,
        priority=100,
        effect='permit'
    ))
    
    return rules


def create_environmental_rules():
    """Create environmental authorization rules."""
    rules = []
    
    # Deny high-risk transactions outside business hours
    def after_hours_high_risk_deny(req: AuthorizationRequest) -> bool:
        return (
            not req.environment.business_hours and
            req.action_attributes.amount is not None and
            req.action_attributes.amount > 10000
        )
    
    rules.append(AuthorizationRule(
        id='after_hours_high_risk_deny',
        name='After Hours High-Risk Transaction Denial',
        condition=after_hours_high_risk_deny,
        priority=300,  # Very high priority
        effect='deny'
    ))
    
    return rules


def create_all_banking_rules():
    """Create all banking authorization rules."""
    rules = []
    rules.extend(create_environmental_rules())  # Highest priority
    rules.extend(create_teller_rules())
    rules.extend(create_branch_manager_rules())
    rules.extend(create_loan_officer_rules())
    rules.extend(create_auditor_rules())
    rules.extend(create_account_owner_rules())
    return rules
