# Retail-ABAC

Industry-specific ABAC authorization system.

## Features

- **Roles**: cashier, manager, inventory_clerk, regional_manager
- **Resource**: Transaction
- **Actions**: process_sale, process_return, adjust_inventory, void_transaction
- **Authorization Rules**: 10+ fine-grained rules
- **Decision Logging**: Complete audit trail for policy mining

## Running

```bash
pip install -r requirements.txt
python app/main.py
```

Server runs on port 5055.

## API Endpoints

- POST /api/users - Create user
- GET /api/users/:id - Get user
- POST /api/accounts - Create resource
- POST /api/transactions - Execute action
- GET /api/decisions - Query decision logs
- GET /api/decisions/export - Export for policy mining
- GET /api/schema - Get attribute schemas

## Authorization Rules

1. Basic role-based access
2. Senior level privileges
3. Resource owner access
4. Location-based access
5. Clearance level requirements
6. After-hours restrictions
7. Cross-location restrictions
8. Inactive resource blocks
9. Junior level limitations
10. High sensitivity controls

## For Policy Mining

Access decision logs at `/api/decisions` with full attribute context.
