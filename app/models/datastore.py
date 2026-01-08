"""In-memory data store for users and accounts."""

import uuid
from typing import Dict, Optional
from app.models.user import User
from app.models.account import Account


class DataStore:
    """In-memory storage for users and accounts (Singleton pattern)."""
    
    _instance = None
    _initialized = False

    def __new__(cls):
        """Ensure only one instance exists (Singleton pattern)."""
        if cls._instance is None:
            cls._instance = super(DataStore, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize storage only once."""
        if not DataStore._initialized:
            self.users: Dict[str, User] = {}
            self.accounts: Dict[str, Account] = {}
            DataStore._initialized = True

    def create_user(self, user: User) -> User:
        """Create a new user with unique ID."""
        if not user.id:
            user.id = self._generate_unique_id('user')
        
        if user.id in self.users:
            raise ValueError(f"User with ID {user.id} already exists")
        
        self.users[user.id] = user
        return user

    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        return self.users.get(user_id)

    def create_account(self, account: Account) -> Account:
        """Create a new account with unique ID."""
        if not account.id:
            account.id = self._generate_unique_id('account')
        
        if account.id in self.accounts:
            raise ValueError(f"Account with ID {account.id} already exists")
        
        self.accounts[account.id] = account
        return account

    def get_account(self, account_id: str) -> Optional[Account]:
        """Get account by ID."""
        return self.accounts.get(account_id)

    def update_account(self, account: Account) -> Account:
        """Update an existing account."""
        if account.id not in self.accounts:
            raise ValueError(f"Account with ID {account.id} does not exist")
        
        self.accounts[account.id] = account
        return account

    def _generate_unique_id(self, prefix: str) -> str:
        """Generate a unique ID with prefix."""
        return f"{prefix}_{uuid.uuid4().hex[:12]}"

    def clear(self):
        """Clear all data (useful for testing)."""
        self.users.clear()
        self.accounts.clear()
