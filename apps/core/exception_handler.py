from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Custom exception handler for API endpoints.
    
    Provides consistent error response format:
    {
        "success": false,
        "error": "Error message",
        "status_code": 400,
        "details": {...}  # Additional validation errors if applicable
    }
    """
    response = exception_handler(exc, context)

    if response is not None:
        # Wrap error response
        error_response = {
            "success": False,
            "error": str(response.data) if isinstance(response.data, str) else "Error",
            "status_code": response.status_code,
            "details": response.data if isinstance(response.data, dict) else None,
        }

        # For validation errors, use the actual error details
        if isinstance(response.data, dict):
            error_response["details"] = response.data

        return Response(
            error_response,
            status=response.status_code
        )

    # Handle server errors
    return Response(
        {
            "success": False,
            "error": "Internal server error",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "details": None,
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
