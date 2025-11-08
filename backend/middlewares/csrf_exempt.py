from django.utils.deprecation import MiddlewareMixin


class CsrfExemptMiddleware(MiddlewareMixin):
    """
    Middleware to exempt API endpoints from CSRF protection.
    API endpoints use JWT authentication, so CSRF is not needed.
    """

    def process_request(self, request):
        # Mark API requests as exempt from CSRF
        if request.path.startswith('/api/'):
            setattr(request, '_dont_enforce_csrf_checks', True)
        return None
