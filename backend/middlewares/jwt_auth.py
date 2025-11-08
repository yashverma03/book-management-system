from types import SimpleNamespace
import jwt
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.urls import resolve
from utils.exceptions import UnauthorizedException, BaseAPIException
from utils.exception_handler import custom_exception_handler

class JWTAuthMiddleware(MiddlewareMixin):
    """
    Global JWT Authentication Middleware.
    Checks Authorization header, decodes JWT token, and adds user to request.user.
    Applied globally to all routes unless marked as public with @is_public decorator.
    """

    def process_request(self, request):
        # Skip for OPTIONS requests (CORS preflight)
        if request.method == 'OPTIONS':
            return None

        # Skip for Django admin, static files, and media files
        if (request.path.startswith('/admin') or
            request.path.startswith('/static') or
            request.path.startswith('/media') or
            request.path.startswith('/swagger') or
            request.path.startswith('/redoc')):
            return None

        # Check if the view function is marked as public
        try:
            resolved = resolve(request.path)
            view_func = resolved.func

            # Check if view has _is_public attribute (set by @is_public decorator)
            # Also check wrapped functions (for @api_view decorator)
            if hasattr(view_func, '_is_public') and view_func._is_public:
                return None

            # Check if the underlying function is marked as public
            # This handles cases where @api_view wraps the function
            if hasattr(view_func, 'cls') and hasattr(view_func.cls, '_is_public'):
                return None
            if hasattr(view_func, 'view_class') and hasattr(view_func.view_class, '_is_public'):
                return None

        except Exception:
            # If URL resolution fails, continue with auth check
            pass

        # Skip authentication if explicitly marked (for cases where decorator runs)
        if hasattr(request, 'skip_auth') and request.skip_auth:
            return None

        # Get token from Authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')

        if not auth_header:
            exc = UnauthorizedException('Authentication required. No token provided.')
            return self._handle_exception(request, exc)

        # Extract token from "Bearer <token>" format
        try:
            parts = auth_header.split(' ')
            if len(parts) == 2 and parts[0].lower() == 'bearer':
                token = parts[1]
            else:
                # If no "Bearer" prefix, assume the whole header is the token
                token = auth_header
        except (IndexError, AttributeError):
            exc = UnauthorizedException('Invalid token header format. Use: Bearer <token>')
            return self._handle_exception(request, exc)

        # Verify and decode token
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=['HS256']
            )

            user_id = payload.get('user_id')
            if not user_id:
                exc = UnauthorizedException('Invalid token payload.')
                return self._handle_exception(request, exc)
            user = SimpleNamespace(**payload)
            request.user = user

        except jwt.ExpiredSignatureError:
            exc = UnauthorizedException('Token has expired.')
            return self._handle_exception(request, exc)
        except jwt.DecodeError:
            exc = UnauthorizedException('Invalid token.')
            return self._handle_exception(request, exc)
        except jwt.InvalidTokenError:
            exc = UnauthorizedException('Invalid token.')
            return self._handle_exception(request, exc)
        except BaseAPIException as e:
            # Re-raise custom exceptions to be handled
            return self._handle_exception(request, e)
        except Exception as e:
            exc = UnauthorizedException(f'Authentication failed: {str(e)}')
            return self._handle_exception(request, exc)

        return None

    def _handle_exception(self, request, exception):
        """
        Handle exceptions by routing them through the exception handler.
        Returns a formatted JSON response as Django HttpResponse.
        """
        if isinstance(exception, BaseAPIException):
            # Use the custom exception handler to automatically format the response
            context = {'request': request, 'view': None}
            drf_response = custom_exception_handler(exception, context)

            # Convert DRF Response to Django HttpResponse
            # This ensures the response is properly rendered and can be accessed by other middleware
            from django.http import JsonResponse
            return JsonResponse(
                drf_response.data,
                status=drf_response.status_code,
                safe=False
            )

        # If it's not a BaseAPIException, return None to let it propagate
        return None
