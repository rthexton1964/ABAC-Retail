"""API routes for the banking application."""

from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
from app.models.user import User, UserAttributes, Location
from app.models.account import Account, AccountAttributes
from app.authorization.models import Environment
from app.authorization.decision_logger import LogQueryFilters
from app.api.errors import ValidationError, NotFoundError


def create_routes_blueprint():
    """Create and configure routes blueprint."""
    bp = Blueprint('api', __name__, url_prefix='/api')
    
    @bp.route('/', methods=['GET'])
    def root():
        """Root endpoint - API information."""
        return jsonify({
            'name': 'ABAC Banking Application',
            'version': '1.0.0',
            'endpoints': {
                'users': '/api/users',
                'accounts': '/api/accounts',
                'transactions': '/api/transactions',
                'decisions': '/api/decisions',
                'schema': '/api/schema',
                'health': '/health'
            }
        })

    # User endpoints
    @bp.route('/users', methods=['POST'])
    def create_user():
        """Create a new user."""
        data = request.get_json()
        
        if not data:
            raise ValidationError("Request body is required")
        
        try:
            # Validate required fields
            if 'name' not in data:
                raise ValidationError("Field 'name' is required")
            if 'attributes' not in data:
                raise ValidationError("Field 'attributes' is required")
            
            attrs = data['attributes']
            location = Location(**attrs['location'])
            user_attrs = UserAttributes(
                department=attrs['department'],
                seniority=attrs['seniority'],
                location=location,
                clearance_level=attrs['clearance_level']
            )
            
            user = User(
                id=data.get('id', ''),
                name=data['name'],
                attributes=user_attrs
            )
            
            created_user = current_app.datastore.create_user(user)
            return jsonify(created_user.to_dict()), 201
            
        except (KeyError, TypeError) as e:
            raise ValidationError(f"Invalid user data: {str(e)}")
        except ValueError as e:
            raise ValidationError(str(e))

    @bp.route('/users/<user_id>', methods=['GET'])
    def get_user(user_id):
        """Get user by ID."""
        user = current_app.datastore.get_user(user_id)
        if not user:
            raise NotFoundError(f"User with ID {user_id} not found")
        return jsonify(user.to_dict())

    # Account endpoints
    @bp.route('/accounts', methods=['POST'])
    def create_account():
        """Create a new account."""
        data = request.get_json()
        
        if not data:
            raise ValidationError("Request body is required")
        
        try:
            if 'attributes' not in data:
                raise ValidationError("Field 'attributes' is required")
            
            account_attrs = AccountAttributes(**data['attributes'])
            account = Account(
                id=data.get('id', ''),
                attributes=account_attrs
            )
            
            created_account = current_app.datastore.create_account(account)
            return jsonify(created_account.to_dict()), 201
            
        except (KeyError, TypeError) as e:
            raise ValidationError(f"Invalid account data: {str(e)}")
        except ValueError as e:
            raise ValidationError(str(e))

    @bp.route('/accounts/<account_id>', methods=['GET'])
    def get_account(account_id):
        """Get account by ID."""
        account = current_app.datastore.get_account(account_id)
        if not account:
            raise NotFoundError(f"Account with ID {account_id} not found")
        return jsonify(account.to_dict())

    # Transaction endpoint
    @bp.route('/transactions', methods=['POST'])
    def execute_transaction():
        """Execute a transaction with authorization."""
        data = request.get_json()
        
        if not data:
            raise ValidationError("Request body is required")
        
        try:
            # Validate required fields
            if 'user_id' not in data:
                raise ValidationError("Field 'user_id' is required")
            if 'account_id' not in data:
                raise ValidationError("Field 'account_id' is required")
            if 'action' not in data:
                raise ValidationError("Field 'action' is required")
            
            # Get user and account
            user = current_app.datastore.get_user(data['user_id'])
            if not user:
                raise NotFoundError(f"User with ID {data['user_id']} not found")
            
            account = current_app.datastore.get_account(data['account_id'])
            if not account:
                raise NotFoundError(f"Account with ID {data['account_id']} not found")
            
            # Create environment
            environment = Environment(
                timestamp=datetime.now(),
                business_hours=data.get('business_hours', True),
                ip_address=data.get('ip_address'),
                location=data.get('location')
            )
            
            # Execute transaction
            success, message, transaction = current_app.transaction_executor.execute_transaction(
                user=user,
                account=account,
                action=data['action'],
                amount=data.get('amount'),
                environment=environment
            )
            
            return jsonify({
                'success': success,
                'message': message,
                'transaction': transaction.to_dict()
            }), 200 if success else 403
            
        except (KeyError, TypeError) as e:
            raise ValidationError(f"Invalid transaction data: {str(e)}")

    # Decision log endpoints
    @bp.route('/decisions', methods=['GET'])
    def query_decisions():
        """Query authorization decision logs."""
        filters = LogQueryFilters(
            user_id=request.args.get('userId'),
            action_type=request.args.get('actionType'),
            decision=request.args.get('decision')
        )
        
        decisions = current_app.decision_logger.query(filters)
        return jsonify([d.to_dict() for d in decisions])

    @bp.route('/decisions/statistics', methods=['GET'])
    def get_statistics():
        """Get decision statistics."""
        stats = current_app.decision_logger.get_statistics()
        return jsonify(stats.to_dict())

    @bp.route('/decisions/export', methods=['GET'])
    def export_decisions():
        """Export decision logs as JSON."""
        logs_json = current_app.decision_logger.export_logs('json')
        return logs_json, 200, {'Content-Type': 'application/json'}

    # Schema endpoint
    @bp.route('/schema', methods=['GET'])
    def get_schema():
        """Get attribute schemas."""
        schema = {
            'userAttributes': {
                'department': list(UserAttributes.VALID_DEPARTMENTS),
                'seniority': list(UserAttributes.VALID_SENIORITY),
                'location': {
                    'branch': 'string',
                    'region': 'string',
                    'country': 'string'
                },
                'clearanceLevel': {'min': 1, 'max': 5}
            },
            'accountAttributes': {
                'type': list(AccountAttributes.VALID_TYPES),
                'status': list(AccountAttributes.VALID_STATUSES),
                'balance': {'type': 'number'},
                'owner': {'type': 'string'},
                'branch': {'type': 'string'}
            },
            'actionAttributes': {
                'type': [
                    'deposit', 'withdrawal', 'transfer', 'view_balance',
                    'view_history', 'freeze_account', 'close_account', 'approve_loan'
                ],
                'amount': {'type': 'number'}
            },
            'environmentAttributes': {
                'businessHours': {'type': 'boolean'},
                'timestamp': {'type': 'date'},
                'ipAddress': {'type': 'string'},
                'location': {'type': 'string'}
            }
        }
        return jsonify(schema)

    # Health check
    @bp.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint."""
        return jsonify({'status': 'healthy'}), 200

    return bp
