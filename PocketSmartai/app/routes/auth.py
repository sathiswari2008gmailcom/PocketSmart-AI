from fastapi import APIRouter,Depends,HTTPException,Response
from sqlalchemy import or_
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import RegisterRequest,LoginRequest
from ..auth import hash_password,verify_password,create_access_token
from ..dependencies import current_user
router=APIRouter(prefix="/api/auth",tags=["Authentication"])
@router.post("/register")
def register(p:RegisterRequest,db:Session=Depends(get_db)):
    email=p.email.strip().lower(); username=p.username.strip()
    if db.query(User).filter(or_(User.email==email,User.username==username)).first(): raise HTTPException(409,"Username or email already exists")
    u=User(username=username,email=email,password_hash=hash_password(p.password)); db.add(u); db.commit(); db.refresh(u)
    return {"message":"Registration successful","access_token":create_access_token(u.id)}
@router.post("/login")
def login(p:LoginRequest,response:Response,db:Session=Depends(get_db)):
    u=db.query(User).filter(User.email==p.email.strip().lower()).first()
    if not u or not verify_password(p.password,u.password_hash): raise HTTPException(401,"Invalid email or password")
    token=create_access_token(u.id); response.set_cookie("access_token",token,httponly=True,samesite="lax",secure=False,max_age=3600)
    return {"message":"Login successful","access_token":token,"user":{"id":u.id,"username":u.username,"email":u.email}}
@router.post("/logout")
def logout(response:Response): response.delete_cookie("access_token"); return {"message":"Logged out"}
@router.get("/session-info")
def session_info(user=Depends(current_user)): return {"logged_in":True,"user":{"id":user.id,"username":user.username,"email":user.email}}
@router.post("/token")
def token(p:LoginRequest,response:Response,db:Session=Depends(get_db)): return login(p,response,db)
