"""Flask application factory."""

from flask import Flask
from app.api.errors import register_error_handlers
from app.models.datastore import DataStore
from app.authorization.engine import AuthorizationEngine
from app.authorization.decision_logger import DecisionLogger
from app.authorization.banking_rules import create_all_banking_rules
from app.models.transaction_executor import TransactionExecutor


def create_app():
    """Create and configure Flask application."""
    app = Flask(__name__)
    
    # Configure JSON serialization
    app.config['JSON_SORT_KEYS'] = False
    
    # Initialize components
    datastore = DataStore()
    auth_engine = AuthorizationEngine()
    decision_logger = DecisionLogger()
    transaction_executor = TransactionExecutor(datastore, auth_engine, decision_logger)
    
    # Load banking rules
    for rule in create_all_banking_rules():
        auth_engine.add_rule(rule)
    
    # Store components in app context
    app.datastore = datastore
    app.auth_engine = auth_engine
    app.decision_logger = decision_logger
    app.transaction_executor = transaction_executor
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register blueprints
    from app.api.routes import create_routes_blueprint
    app.register_blueprint(create_routes_blueprint())
    
    # Add root route
    @app.route('/')
    def root():
        return {
            'name': 'ABAC Banking Application',
            'version': '1.0.0',
            'description': 'Test banking app with fine-grained ABAC authorization',
            'endpoints': {
                'api': '/api',
                'health': '/health',
                'users': '/api/users',
                'accounts': '/api/accounts',
                'transactions': '/api/transactions',
                'decisions': '/api/decisions',
                'schema': '/api/schema'
            }
        }
    
    return app
