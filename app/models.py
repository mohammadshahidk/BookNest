from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Enum, Boolean
from sqlalchemy.orm  import relationship
from .database import Base
from enum import Enum as PyEnum


class UserType(PyEnum):
    admin = 'admin'
    librarian = 'librarian'
    member = 'member'


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,nullable=False, index=True)
    phone = Column(String,nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    joined_at = Column(DateTime, default=func.now())
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserType), default=UserType.member)
    

class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    genre = Column(String, nullable=True)
    borrower_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    
    borrower = relationship('User', backref='borrower_books')
    

class BorrowHistory(Base):
    __tablename__ = 'borrowhistories'
    
    id = Column(Integer, primary_key=True, index=True)
    borrower_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=True)
    borrowed_date = Column(DateTime, nullable=True)
    return_date = Column(DateTime, nullable=True)
    
    borrower = relationship('User', backref='borrower_histories')
    book = relationship('Book', backref='book_histories')    

