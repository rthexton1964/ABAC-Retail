"""Authorization rules for Retail-ABAC."""

from app.authorization.rules import AuthorizationRule
from app.authorization.models import AuthorizationRequest


def create_retail_abac_rules():
    """Create authorization rules for Retail-ABAC."""
    rules = []
    
    # Rule 1: Basic role-based access
    def basic_access(req: AuthorizationRequest) -> bool:
        return req.user.attributes.role in {"cashier", "manager", "inventory_clerk"}
    
    rules.append(AuthorizationRule(
        id='basic_access',
        name='Basic Access Rule',
        condition=basic_access,
        priority=100,
        effect='permit'
    ))
    
    # Rule 2: Senior level access
    def senior_access(req: AuthorizationRequest) -> bool:
        return (
            req.user.attributes.level in {'senior', 'executive'} and
            req.action in {"process_sale", "process_return", "adjust_inventory", "void_transaction"}
        )
    
    rules.append(AuthorizationRule(
        id='senior_access',
        name='Senior Level Access',
        condition=senior_access,
        priority=90,
        effect='permit'
    ))
    
    # Rule 3: Owner access
    def owner_access(req: AuthorizationRequest) -> bool:
        return req.user.id == req.resource.attributes.owner_id
    
    rules.append(AuthorizationRule(
        id='owner_access',
        name='Resource Owner Access',
        condition=owner_access,
        priority=95,
        effect='permit'
    ))
    
    # Rule 4: Location-based access
    def location_access(req: AuthorizationRequest) -> bool:
        return req.user.attributes.location.primary == req.resource.attributes.location
    
    rules.append(AuthorizationRule(
        id='location_access',
        name='Same Location Access',
        condition=location_access,
        priority=85,
        effect='permit'
    ))
    
    # Rule 5: Clearance level access
    def clearance_access(req: AuthorizationRequest) -> bool:
        return req.user.attributes.clearance_level >= req.resource.attributes.sensitivity_level
    
    rules.append(AuthorizationRule(
        id='clearance_access',
        name='Clearance Level Access',
        condition=clearance_access,
        priority=80,
        effect='permit'
    ))
    
    # Rule 6: After hours restriction
    def after_hours_deny(req: AuthorizationRequest) -> bool:
        return not req.environment.business_hours and req.action_attributes.amount and req.action_attributes.amount > 1000
    
    rules.append(AuthorizationRule(
        id='after_hours_deny',
        name='After Hours High-Value Restriction',
        condition=after_hours_deny,
        priority=200,
        effect='deny'
    ))
    
    # Rule 7: Cross-location restriction
    def cross_location_deny(req: AuthorizationRequest) -> bool:
        return (
            req.user.attributes.role == 'cashier' and
            req.user.attributes.location.primary != req.resource.attributes.location
        )
    
    rules.append(AuthorizationRule(
        id='cross_location_deny',
        name='Cross-Location Restriction',
        condition=cross_location_deny,
        priority=150,
        effect='deny'
    ))
    
    # Rule 8: Inactive resource restriction
    def inactive_resource_deny(req: AuthorizationRequest) -> bool:
        return req.resource.attributes.status == 'inactive'
    
    rules.append(AuthorizationRule(
        id='inactive_resource_deny',
        name='Inactive Resource Restriction',
        condition=inactive_resource_deny,
        priority=180,
        effect='deny'
    ))
    
    # Rule 9: Junior level restriction
    def junior_restriction(req: AuthorizationRequest) -> bool:
        return req.user.attributes.level == 'junior' and req.action in {"adjust_inventory", "void_transaction"}
    
    rules.append(AuthorizationRule(
        id='junior_restriction',
        name='Junior Level Restriction',
        condition=junior_restriction,
        priority=120,
        effect='deny'
    ))
    
    # Rule 10: High sensitivity restriction
    def high_sensitivity_deny(req: AuthorizationRequest) -> bool:
        return (
            req.resource.attributes.sensitivity_level >= 4 and
            req.user.attributes.clearance_level < 4
        )
    
    rules.append(AuthorizationRule(
        id='high_sensitivity_deny',
        name='High Sensitivity Restriction',
        condition=high_sensitivity_deny,
        priority=190,
        effect='deny'
    ))
    
    return rules


def create_all_rules():
    """Create all authorization rules."""
    return create_retail_abac_rules()
