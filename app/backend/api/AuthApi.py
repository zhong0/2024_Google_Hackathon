from fastapi import APIRouter, HTTPException, Depends
from ..service.AuthService import AuthService
from ..entity.UserEntity import User

router = APIRouter()
auth_service = AuthService()

@router.post("/register")
def register(user: User):
    if not auth_service.is_validate_username(user.username):
        raise HTTPException(status_code=400, detail="Username must be at least 5 characters long.")
    if not auth_service.is_validate_password(user.password):
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long and include at least one letter and one number.")
    
    if auth_service.register(user.username, user.password):
        return {"message": "User registered successfully"}
    else:
        raise HTTPException(status_code=400, detail="Username already registered")

@router.post("/login")
def login(user: User):
    if not auth_service.is_validate_username(user.username) or not auth_service.is_validate_password(user.password):
        raise HTTPException(status_code=400, detail="Username or password does not meet requirements")

    if auth_service.authenticate(user.username, user.password):
        return {"message": "Login successfully"}
    else:
        raise HTTPException(status_code=401, detail="Incorrect username or password")