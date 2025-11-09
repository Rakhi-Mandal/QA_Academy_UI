"""
Standard API Response Formats
"""
from typing import Any, Optional
from fastapi.responses import JSONResponse

def success_response(
    data: Any = None,
    message: str = "Success",
    status_code: int = 200
) -> JSONResponse:
    """
    Return standard success response
    
    Args:
        data: Response data
        message: Success message
        status_code: HTTP status code
        
    Returns:
        JSONResponse with standard format
    """
    return JSONResponse(
        status_code=status_code,
        content={
            "success": True,
            "message": message,
            "data": data
        }
    )

def error_response(
    message: str = "An error occurred",
    status_code: int = 400,
    errors: Optional[dict] = None
) -> JSONResponse:
    """
    Return standard error response
    
    Args:
        message: Error message
        status_code: HTTP status code
        errors: Additional error details
        
    Returns:
        JSONResponse with standard format
    """
    content = {
        "success": False,
        "message": message,
        "data": None
    }
    
    if errors:
        content["errors"] = errors
    
    return JSONResponse(
        status_code=status_code,
        content=content
    )