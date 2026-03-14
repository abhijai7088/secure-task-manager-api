"""
Consistent API response helpers.
"""

from typing import Any, Optional


def success_response(message: str, data: Any = None, status_code: int = 200) -> dict:
    """Build a standardised success response dict."""
    response = {"message": message}
    if data is not None:
        response["data"] = data
    return response


def error_response(message: str, errors: Optional[Any] = None) -> dict:
    """Build a standardised error response dict."""
    response = {"success": False, "message": message}
    if errors is not None:
        response["errors"] = errors
    return response
