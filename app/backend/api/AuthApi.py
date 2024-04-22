from fastapi import APIRouter, HTTPException, Depends
from service.AuthService import AuthService
from entity.UserEntity import User
import re

router = APIRouter()
auth_service = AuthService()

# 用戶名長度至少5個字符
def validate_username(username: str) -> bool:
    
    return len(username) >= 5

# 密碼至少8個字符且包含至少一個數字和一個字母
def validate_password(password: str) -> bool:
    if len(password) < 8:
        return False
    if not re.search("[a-zA-Z]", password):
        return False
    if not re.search("[0-9]", password):
        return False
    
    return True

@router.post("/register/")
def register(user: User):
    if not validate_username(user.username):
        raise HTTPException(status_code=400, detail="Username must be at least 5 characters long.")
    if not validate_password(user.password):
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long and include at least one letter and one number.")
    
    if auth_service.register(user.username, user.password):
        return {"message": "User registered successfully"}
    else:
        raise HTTPException(status_code=400, detail="Username already registered")

@router.post("/login/")
def login(user: User):
    if not validate_username(user.username) or not validate_password(user.password):
        raise HTTPException(status_code=400, detail="Username or password does not meet requirements")

    if auth_service.authenticate(user.username, user.password):
        return {"message": "User authenticated"}
    else:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
