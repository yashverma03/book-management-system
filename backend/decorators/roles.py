from functools import wraps
from user.models import UserRole
from utils.exceptions import ForbiddenException, UnauthorizedException


def roles(allowed_roles):
    """
    Decorator to restrict access to views based on user roles.
    Checks roles from request.user['role'].

    Args:
        allowed_roles: List of UserRole enum values that are allowed to access the view
                      Example: [UserRole.ADMIN, UserRole.MANAGER]

    Usage:
        @roles([UserRole.ADMIN])
        @api_view(['GET'])
        def admin_only_view(request):
            pass

        @roles([UserRole.ADMIN, UserRole.MANAGER])
        @api_view(['POST'])
        def admin_or_manager_view(request):
            pass

    Raises:
        UnauthorizedException: If user is not authenticated
        ForbiddenException: If user's role is not in allowed_roles
    """
    # Convert to list if single role is passed
    if not isinstance(allowed_roles, list):
        allowed_roles = [allowed_roles]

    # Convert UserRole enum values to their string values for comparison
    allowed_role_values = [role.value if hasattr(role, 'value') else str(role) for role in allowed_roles]

    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            # Check if user is authenticated
            if not hasattr(request, 'user') or not request.user:
                raise UnauthorizedException('Authentication required.')

            # Check if user has a role (supports both dict and attribute access)
            if isinstance(request.user, dict):
                if 'role' not in request.user:
                    raise ForbiddenException('User role not found.')
                user_role = request.user.get('role')
            elif hasattr(request.user, 'role'):
                user_role = request.user.role
            else:
                raise ForbiddenException('User role not found.')
            if hasattr(user_role, 'value'):
                user_role_value = user_role.value
            else:
                user_role_value = str(user_role)

            # Check if user's role is in allowed roles
            if user_role_value not in allowed_role_values:
                role_names = ', '.join([role.value if hasattr(role, 'value') else str(role) for role in allowed_roles])
                raise ForbiddenException(
                    f'Access denied. Required roles: {role_names}'
                )

            # User has required role, proceed with view
            return view_func(request, *args, **kwargs)

        return wrapped_view
    return decorator
