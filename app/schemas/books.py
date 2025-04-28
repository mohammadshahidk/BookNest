from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.schemas import users as user_schemas


class GetAllBooks(BaseModel):
    id: int
    title: str
    author: str
    genre: Optional[str] = None
    borrower_id: Optional[int] = None
    
class BorrowHistory(BaseModel):
    id: int
    book: GetAllBooks
    borrower: Optional[user_schemas.UserList] = None
    borrowed_date: Optional[datetime] = None
    return_date: Optional[datetime] = None
    
    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.strftime('%d-%m-%Y') if v else None
        }
    
    
    
class BookCreate(BaseModel):
    title: str
    author: str
    genre: str
    
    
    