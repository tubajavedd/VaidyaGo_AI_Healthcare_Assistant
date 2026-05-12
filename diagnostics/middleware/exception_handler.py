from rest_framework.views import exception_handler
from ..utils.response import error_response
from rest_framework import status

def diagnostic_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        return error_response(response.data, response.status_code)
    
    # Custom handling for unhandled exceptions
    return error_response(str(exc), status.HTTP_500_INTERNAL_SERVER_ERROR)
