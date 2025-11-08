from functools import wraps


def is_public(view_func):
    """
    Decorator to mark a route as public (bypasses auth middleware).

    Usage:
        @is_public
        @api_view(['POST'])
        def login(request):
            pass
    """
    # Mark the view function as public (checked by middleware)
    view_func._is_public = True

    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        # Also mark request as public (for additional safety)
        request.skip_auth = True
        return view_func(request, *args, **kwargs)

    # Preserve the marker on the wrapped function
    wrapped_view._is_public = True
    return wrapped_view
