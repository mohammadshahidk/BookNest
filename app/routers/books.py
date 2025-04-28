from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models import Book, User, BorrowHistory
from app.schemas import books as book_schemas
from app.auth import get_current_user
from app.crud import book as book_crud
from typing import List
from app.utils import parse_csv
from typing import Optional

router = APIRouter()


@router.get('/books/', response_model=List[book_schemas.GetAllBooks])
def all_books(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)):
    books = book_crud.get_all_books(db)
    return books

@router.get('/available-books/', response_model=List[book_schemas.GetAllBooks])
def all_books(
    db: Session = Depends(get_db),
    genre: Optional[str] = None,
    search: Optional[str] = None,
    current_user: dict = Depends(get_current_user)):
    books = book_crud.get_available_books(db, genre, search)
    return books

@router.post('/books/')
def create_books(
    request: book_schemas.BookCreate, db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)):
    book = Book(
        title=request.title,
        author=request.author
        )
    db.add(book)
    db.commit()
    db.refresh(book)
    
    return {'message': 'Book created Successfully'}
    
    

@router.post('/{book_id}/borrow/')
def borrow_book(
    book_id: int, current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    
    
    if not book:
        raise HTTPException(status=404, details='Book not found')
    if book.borrower_id:
        raise HTTPException(status=400, details='Book already borrowed')
    
    book.borrower_id = current_user['user_id']
    borrowhistory = BorrowHistory(
        borrower_id=current_user['user_id'],
        book_id=book.id,
        borrowed_date=datetime.now()
    )
    db.add(borrowhistory)
    db.commit()
    db.refresh(borrowhistory)
    return {'message': f'Book {book.title} borrowed'}

@router.post('/{book_id}/return')
def return_book(
    book_id: int, current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book or book.borrower_id != int(current_user['user_id']):
        raise HTTPException(
            status_code=403,
            detail="You can't return a book you didn't borrow")
    
    borrowhistory = db.query(BorrowHistory).filter(
        BorrowHistory.book_id == book.id,
        BorrowHistory.borrower_id == book.borrower_id).first()
    if borrowhistory:
        borrowhistory.return_date = datetime.now()
    book.borrower_id = None
    db.commit()
    return {'message': f'Book {book.title} returned successfully'}


@router.get('/borrow/history', response_model=List[book_schemas.BorrowHistory])
def borrow_history(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)):
    history = book_crud.get_borrowhistory(db)
    return history


@router.post('/upload/')
async def create_book_from_csv(
    file: UploadFile= File(...),db: Session = Depends(get_db)):
    content = await file.read()
    csv_str = content.decode("utf-8")
    books = parse_csv(csv_str)
    
    for book in books:
        db_book = Book(**book.dict())
        db.add(db_book)
    db.commit()
    
    return {"message": f"{len(books)} books added successfully"}

