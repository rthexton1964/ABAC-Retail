# Retail ABAC Application

Store chain management with fine-grained ABAC authorization

## Features

- Fine-grained ABAC authorization
- Multiple user roles: Cashiers, Store Managers, Inventory Clerks, Regional Managers
- Resource management: Transactions, Inventory, Returns, Employee Records
- Complete authorization decision logging
- REST API for all operations
- Policy mining support

## Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app/main.py
```

The API will be available at `http://localhost:5055`

## API Endpoints

- `POST /api/users` - Create user
- `GET /api/users/:id` - Get user
- `POST /api/accounts` - Create resource
- `GET /api/accounts/:id` - Get resource
- `POST /api/transactions` - Execute action
- `GET /api/decisions` - Query decision logs
- `GET /api/decisions/statistics` - Get statistics
- `GET /api/decisions/export` - Export logs
- `GET /api/schema` - Get attribute schemas
- `GET /health` - Health check

## For Policy Mining

Access authorization decision logs at:
- `GET /api/decisions` - All decisions with full context
- `GET /api/decisions/export` - JSON export for analysis

## Deployment

Deploy to Heroku:
```bash
heroku create your-app-name
git push heroku main
```

## License

MIT
