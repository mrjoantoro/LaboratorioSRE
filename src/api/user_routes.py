from fastapi import APIRouter, Depends
from src.services.user_service import create_user_service, authenticate_user
from src.models.user import UserCreate
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/users/")
async def create_user(user_data: UserCreate):
    return create_user_service(user_data)

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return authenticate_user(form_data)
