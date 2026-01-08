"""Main application entry point."""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/..'))

from app.api.app import create_app


def main():
    """Run the Flask application."""
    app = create_app()
    
    # Get configuration from environment variables
    port = int(os.environ.get('PORT', 5055))
    debug = os.environ.get('DEBUG', 'false').lower() == 'true'
    
    app.run(host='0.0.0.0', port=port, debug=debug)


if __name__ == '__main__':
    main()
