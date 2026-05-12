from rest_framework.response import Response
from rest_framework import status

def success_response(data, message="Success", status_code=status.HTTP_200_OK):
    return Response({
        "status": "success",
        "message": message,
        "data": data
    }, status=status_code)

def error_response(errors, status_code=status.HTTP_400_BAD_REQUEST):
    return Response({
        "status": "error",
        "errors": errors
    }, status=status_code)
