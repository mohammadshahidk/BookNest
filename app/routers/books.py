from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Book, User, BorrowerHistory
from app.schemas import books as book_schemas
from app.auth import get_current_user
from app.crud import book as book_crud
from typing import List

router = APIRouter()


@router.get('/books/', response_model=List[book_schemas.GetAllBooks])
def all_books(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    books = book_crud.get_all_books(db)
    return books

@router.post('/books/')
def create_books(
    request: book_schemas.CreateBook, db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)):
    book = Book(
        title=request.title,
        author=request.author,
        published_year=request.published_year
        )
    db.add(book)
    db.commit()
    db.refresh(book)
    
    return {'message': 'Book created Successfully'}
    
    

@router.post('/books/{book_id}/borrow/')
def borrow_book(
    book_id: int, current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    
    if not book:
        raise HTTPException(status=404, details='Book not found')
    if book.borrower_id:
        raise HTTPException(status=400, details='Book already borrowed')
    
    book.borrower_id = current_user.id
    db.commit()
    return {'message': f'Book {book.title} borrowed by {current_user.name}'}

@router.post('/books/{book_id}/return')
def return_book(
    book_id: int, current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    
    if not book or book.borrower_id != current_user.id:
        raise HTTPException(status=403, details="You can't return a book you didn't borrow")
    
    book.borrower_id = None
    db.commit()
    return {'message': f'Book {book.title} returned successfully'}
