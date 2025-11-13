"""
FastAPI routes for User APIs
"""
from fastapi import APIRouter, Path
from schemas.user import UserCreate, UserUpdate, UserLogin
from services import user_service

router = APIRouter()


@router.get("/get-all")
def get_all_users():
    """Get all users"""
    return user_service.service_get_all_users()


@router.get("/{user_id}")
def get_user_by_id(user_id: int = Path(..., description="User ID to fetch")):
    """Get user by ID"""
    return user_service.service_get_user_by_id(user_id)


@router.post("/create")
def create_user(data: UserCreate):
    """Create a new user"""
    return user_service.service_create_user(data)


@router.put("/{user_id}/update")
def update_user(user_id: int, data: UserUpdate):
    """Update existing user"""
    return user_service.service_update_user(user_id, data)


@router.delete("/{user_id}/delete")
def delete_user(user_id: int):
    """Delete a user"""
    return user_service.service_delete_user(user_id)


@router.post("/login")
def login_user(credentials: UserLogin):
    """Verify login credentials"""
    return user_service.login_user(credentials.user_mail, credentials.user_password)
