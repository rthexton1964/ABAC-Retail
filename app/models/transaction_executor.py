"""Transaction executor with authorization integration."""

from datetime import datetime
from app.models.datastore import DataStore
from app.models.transaction import Transaction, TransactionAttributes
from app.models.user import User
from app.models.account import Account
from app.authorization.engine import AuthorizationEngine
from app.authorization.models import AuthorizationRequest, Environment, ActionAttributes
from app.authorization.decision_logger import DecisionLogger


class TransactionExecutor:
    """Executes transactions with authorization checks."""

    def __init__(
        self,
        datastore: DataStore,
        auth_engine: AuthorizationEngine,
        decision_logger: DecisionLogger
    ):
        self.datastore = datastore
        self.auth_engine = auth_engine
        self.decision_logger = decision_logger

    def execute_transaction(
        self,
        user: User,
        account: Account,
        action: str,
        amount: float = None,
        environment: Environment = None,
        transaction_id: str = None
    ) -> tuple[bool, str, Transaction]:
        """
        Execute a transaction with authorization check.
        
        Returns:
            (success, message, transaction)
        """
        # Create environment if not provided
        if environment is None:
            environment = Environment(
                timestamp=datetime.now(),
                business_hours=self._is_business_hours(datetime.now())
            )

        # Create authorization request
        action_attrs = ActionAttributes(amount=amount, type=action)
        auth_request = AuthorizationRequest(
            user=user,
            action=action,
            resource=account,
            environment=environment,
            action_attributes=action_attrs
        )

        # Evaluate authorization
        decision = self.auth_engine.evaluate(auth_request)
        self.decision_logger.log(decision)

        # Create transaction record
        transaction = Transaction(
            id=transaction_id or f"txn_{datetime.now().timestamp()}",
            attributes=TransactionAttributes(
                type=action,
                amount=amount,
                timestamp=environment.timestamp,
                source_account=account.id
            )
        )

        # If denied, return early
        if decision.decision == 'deny':
            return False, decision.reason, transaction

        # Execute the transaction based on action type
        try:
            if action == 'deposit':
                account.attributes.balance += amount
                self.datastore.update_account(account)
                return True, f"Deposited ${amount}", transaction

            elif action == 'withdrawal':
                if account.attributes.balance < amount:
                    return False, "Insufficient funds", transaction
                account.attributes.balance -= amount
                self.datastore.update_account(account)
                return True, f"Withdrew ${amount}", transaction

            elif action == 'transfer':
                # For simplicity, just deduct from source
                if account.attributes.balance < amount:
                    return False, "Insufficient funds", transaction
                account.attributes.balance -= amount
                self.datastore.update_account(account)
                return True, f"Transferred ${amount}", transaction

            elif action == 'view_balance':
                return True, f"Balance: ${account.attributes.balance}", transaction

            elif action == 'view_history':
                return True, "Transaction history retrieved", transaction

            elif action == 'freeze_account':
                account.attributes.status = 'frozen'
                self.datastore.update_account(account)
                return True, "Account frozen", transaction

            elif action == 'close_account':
                account.attributes.status = 'closed'
                self.datastore.update_account(account)
                return True, "Account closed", transaction

            elif action == 'approve_loan':
                # For simplicity, just mark as approved
                return True, f"Loan of ${amount} approved", transaction

            else:
                return False, f"Unknown action: {action}", transaction

        except Exception as e:
            return False, f"Transaction failed: {str(e)}", transaction

    def _is_business_hours(self, timestamp: datetime) -> bool:
        """Check if timestamp is during business hours (9 AM - 5 PM, Mon-Fri)."""
        if timestamp.weekday() >= 5:  # Saturday or Sunday
            return False
        hour = timestamp.hour
        return 9 <= hour < 17
