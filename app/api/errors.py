"""Custom error classes and handlers."""

from flask import jsonify


class ValidationError(Exception):
    """Validation error (400)."""
    status_code = 400

    def __init__(self, message, details=None):
        super().__init__()
        self.message = message
        self.details = details


class AuthorizationError(Exception):
    """Authorization error (403)."""
    status_code = 403

    def __init__(self, message, details=None):
        super().__init__()
        self.message = message
        self.details = details


class NotFoundError(Exception):
    """Not found error (404)."""
    status_code = 404

    def __init__(self, message, details=None):
        super().__init__()
        self.message = message
        self.details = details


class ServerError(Exception):
    """Server error (500)."""
    status_code = 500

    def __init__(self, message, details=None):
        super().__init__()
        self.message = message
        self.details = details


def register_error_handlers(app):
    """Register error handlers with Flask app."""

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        response = {
            'error': {
                'code': 'validation_error',
                'message': error.message
            }
        }
        if error.details:
            response['error']['details'] = error.details
        return jsonify(response), error.status_code

    @app.errorhandler(AuthorizationError)
    def handle_authorization_error(error):
        response = {
            'error': {
                'code': 'authorization_error',
                'message': error.message
            }
        }
        if error.details:
            response['error']['details'] = error.details
        return jsonify(response), error.status_code

    @app.errorhandler(NotFoundError)
    def handle_not_found_error(error):
        response = {
            'error': {
                'code': 'not_found',
                'message': error.message
            }
        }
        if error.details:
            response['error']['details'] = error.details
        return jsonify(response), error.status_code

    @app.errorhandler(ServerError)
    def handle_server_error(error):
        response = {
            'error': {
                'code': 'server_error',
                'message': error.message
            }
        }
        return jsonify(response), error.status_code

    @app.errorhandler(Exception)
    def handle_generic_error(error):
        response = {
            'error': {
                'code': 'server_error',
                'message': 'An unexpected error occurred'
            }
        }
        return jsonify(response), 500
