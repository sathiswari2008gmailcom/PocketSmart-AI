import hashlib
import hmac
import os
from datetime import datetime,timedelta,timezone
import jwt
from jwt.exceptions import InvalidTokenError
from .config import get_settings
from .models import User
settings=get_settings()
ALGORITHM="HS256"
def hash_password(password:str)->str:
    salt=os.urandom(16)
    digest=hashlib.scrypt(password.encode(),salt=salt,n=2**14,r=8,p=1)
    return "scrypt$"+salt.hex()+"$"+digest.hex()
def verify_password(password:str,stored:str)->bool:
    try:
        _,salt_hex,digest_hex=stored.split("$",2)
        actual=hashlib.scrypt(password.encode(),salt=bytes.fromhex(salt_hex),n=2**14,r=8,p=1)
        return hmac.compare_digest(actual,bytes.fromhex(digest_hex))
    except (ValueError,TypeError): return False
def create_access_token(user_id:int)->str:
    exp=datetime.now(timezone.utc)+timedelta(minutes=settings.access_token_expire_minutes)
    return jwt.encode({"sub":str(user_id),"exp":exp},settings.secret_key,algorithm=ALGORITHM)
def get_user_from_token(token,db):
    try: uid=int(jwt.decode(token,settings.secret_key,algorithms=[ALGORITHM])["sub"])
    except (InvalidTokenError,KeyError,ValueError,TypeError): return None
    return db.get(User,uid)
