from rest_framework.views import exception_handler


def api_exception_handler(exc, context):
    """Custom API exception handler."""
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:
        errors = {}
        for key, value in response.data.items():
            if isinstance(value, list):
                errors[key] = value[0]
            else:
                errors[key] = value
        response.data = errors
    return response