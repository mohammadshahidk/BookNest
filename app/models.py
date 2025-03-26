from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm  import relationship
from .database import Base

 
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,nullable=False, index=True)
    phone = Column(String,nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    joined_at = Column(DateTime, defaul=func.now())
    

class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    published_year = Column(Integer)
    borrower_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    
    borrower = relationship('User', backref='borrower_books')
    
    

