from fastapi import Depends,HTTPException,Request,status
from sqlalchemy.orm import Session
from .auth import get_user_from_token
from .database import get_db
from .models import User

def current_user_optional(request:Request,db:Session=Depends(get_db)):
    token=request.cookies.get("access_token")
    if not token and request.headers.get("Authorization","").startswith("Bearer "): token=request.headers[7:]
    return get_user_from_token(token,db) if token else None

def current_user(user=Depends(current_user_optional)):
    if not user: raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Login required")
    return user
