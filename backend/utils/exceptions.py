from rest_framework import status
from rest_framework.exceptions import APIException
import requests

class BaseAPIException(APIException):
    """Base exception class for API exceptions with status codes"""
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'A server error occurred.'
    default_code = 'error'

    def __init__(self, detail=None, code=None, status_code=None, error=None):
        if status_code is not None:
            self.status_code = status_code
        self.error = error
        super().__init__(detail, code)


class ConflictException(BaseAPIException):
    """409 Conflict - Resource already exists"""
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'Resource conflict occurred.'
    default_code = 'conflict'


class NotFoundException(BaseAPIException):
    """404 Not Found - Resource not found"""
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Resource not found.'
    default_code = 'not_found'


class BadRequestException(BaseAPIException):
    """400 Bad Request - Invalid request"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Bad request.'
    default_code = 'bad_request'


class UnauthorizedException(BaseAPIException):
    """401 Unauthorized - Authentication required"""
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Authentication required.'
    default_code = 'unauthorized'


class ForbiddenException(BaseAPIException):
    """403 Forbidden - Access denied"""
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'Access denied.'
    default_code = 'forbidden'


class ExternalAPIException(BaseAPIException):
    """Exception for external API request failures"""
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'External API request failed.'
    default_code = 'external_api_error'

    def __init__(self, detail=None, code=None, status_code=None, error=None):
        """
        Initialize ExternalAPIException with error structure containing request and response.
        """
        # If code is a RequestException, treat it as error (for convenience when passing as second arg)
        try:
            if isinstance(code, requests.exceptions.RequestException):
                error = code
                code = None
        except ImportError:
            pass

        # Handle requests exception object - extract request and response info
        if error is not None:
            try:
                if isinstance(error, requests.exceptions.RequestException):
                    # Extract request information from e.request
                    request_info = {}
                    if hasattr(error, 'request') and error.request is not None:
                        request_info = {
                            'url': error.request.url if hasattr(error.request, 'url') else None,
                            'method': error.request.method if hasattr(error.request, 'method') else None,
                            'headers': dict(error.request.headers) if hasattr(error.request, 'headers') and error.request.headers else {},
                            'body': error.request.body.decode('utf-8')[:1000] if hasattr(error.request, 'body') and error.request.body else None
                        }
                    else:
                        request_info = {
                            'url': None,
                            'method': None,
                            'headers': {},
                            'body': None
                        }

                    # Extract response information from e.response
                    response_info = {}
                    if hasattr(error, 'response') and error.response is not None:
                        try:
                            response_body = None
                            if hasattr(error.response, 'text') and error.response.text:
                                response_body = error.response.text[:1000]
                            elif hasattr(error.response, 'content') and error.response.content:
                                try:
                                    response_body = error.response.content.decode('utf-8')[:1000]
                                except (UnicodeDecodeError, AttributeError):
                                    response_body = str(error.response.content)[:1000]

                            response_info = {
                                'status_code': error.response.status_code if hasattr(error.response, 'status_code') else None,
                                'reason': error.response.reason if hasattr(error.response, 'reason') else None,
                                'headers': dict(error.response.headers) if hasattr(error.response, 'headers') and error.response.headers else {},
                                'data': response_body,
                                'message': error.response.reason if hasattr(error.response, 'reason') else None
                            }
                        except Exception:
                            response_info = {
                                'status_code': error.response.status_code if hasattr(error.response, 'status_code') else None,
                                'reason': None,
                                'headers': {},
                                'data': None,
                                'message': None
                            }
                    else:
                        response_info = {
                            'status_code': None,
                            'reason': None,
                            'headers': {},
                            'data': None,
                            'message': None
                        }

                    error = {
                        'request': request_info,
                        'response': response_info
                    }
                elif isinstance(error, dict):
                    # If it's already a dict, ensure it has request and response keys
                    if 'request' not in error:
                        error['request'] = {}
                    if 'response' not in error:
                        error['response'] = {}
                else:
                    # For other types, create empty structure
                    error = {
                        'request': {},
                        'response': {}
                    }
            except ImportError:
                # If requests is not available, treat as regular dict
                if isinstance(error, dict):
                    if 'request' not in error:
                        error['request'] = {}
                    if 'response' not in error:
                        error['response'] = {}
                else:
                    error = {
                        'request': {},
                        'response': {}
                    }
        else:
            # If error is None, create empty structure
            error = {
                'request': {},
                'response': {}
            }

        super().__init__(detail, code, status_code, error)
