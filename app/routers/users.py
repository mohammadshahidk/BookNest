from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas import users as user_schemas
from app.database import get_db
from app.models import User
from app.auth import hash_password, verify_password, create_access_token
from app.utils import parse_user_csv

router = APIRouter()

@router.post('/register/')
def register(
    request: user_schemas.RegisterRequest,
    db: Session = Depends(get_db)):
    if db.query(User).filter(User.phone == request.phone).first():
        raise HTTPException(
            status_code=400, detail='Phonenumber already registered')
    
    user = User(
        name=request.name,
        phone=request.phone,
        password=hash_password(request.password),
        role=request.role)
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {'message': 'User registered successfully'}

@router.post('/login/')
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail='Invalid credentials')
    
    access_token = create_access_token(data={'sub':str(user.id)})
    
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post('/upload/')
async def create_user_from_csv(
    file: UploadFile= File(...), db: Session = Depends(get_db)):
    content = await file.read()
    csv_str = content.decode("utf-8")
    users = parse_user_csv(csv_str)
    
    for user in users:
        db_user = User(**user.dict())
        db.add(db_user)
    db.commit()
    
    return {"message": f"{len(users)} users added successfully"}
