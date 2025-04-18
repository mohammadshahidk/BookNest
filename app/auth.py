from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from .config import settings
from .database import get_db
from .models import User
from sqlalchemy.orm import Session


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password:str, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict,expires_delta: int = 30):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get('sub')
        role = payload.get('role')
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=401, detail='Invalid token')
        return {'user_id': user_id, 'role': role}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Toekn expired')
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail='Invalid token')
    
    
def admin_required(user: dict = Depends(get_current_user)):
    if user['role'] == 'admin':
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return user
        