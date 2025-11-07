import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from utils.exceptions import BaseAPIException

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler for DRF that handles custom exceptions
    and formats error responses consistently with only message and error fields
    """
    # Log the exception
    request = context.get('request', None)
    view = context.get('view', None)

    logger.error(
        f'Exception occurred: {type(exc).__name__} - {str(exc)}',
        exc_info=exc,
        extra={
            'exception_type': type(exc).__name__,
            'exception_message': str(exc),
            'view': view.__class__.__name__ if view else None,
            'request_path': request.path if request else None,
            'request_method': request.method if request else None,
        }
    )

    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    # If it's a custom exception, format the response
    if isinstance(exc, BaseAPIException):
        custom_response_data = {
            'message': exc.detail if isinstance(exc.detail, str) else str(exc.detail)
        }

        # Add error field if provided
        if hasattr(exc, 'error') and exc.error is not None:
            custom_response_data['error'] = exc.error

        return Response(custom_response_data, status=exc.status_code)

    # If response is None, it's an unhandled exception
    if response is None:
        # Handle unexpected exceptions
        return Response(
            {
                'message': 'An unexpected error occurred'
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # Format standard DRF exceptions
    # Convert DRF validation errors to message and error format
    error_data = response.data
    if isinstance(error_data, dict):
        # If it's a dict with field errors, use it as error object
        custom_response_data = {
            'message': 'Validation error',
            'error': error_data
        }
    else:
        custom_response_data = {
            'message': str(error_data) if error_data else 'An error occurred'
        }

    return Response(custom_response_data, status=response.status_code)
