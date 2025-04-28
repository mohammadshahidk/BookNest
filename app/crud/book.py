from sqlalchemy.orm import Session
from app.models import Book, BorrowHistory
from typing import Optional
from sqlalchemy import or_


def get_all_books(db: Session):
    return db.query(Book).all()

def get_available_books(db: Session, genre: Optional[str] = None, search: Optional[str] = None):
    query = db.query(Book).filter(Book.borrower_id.is_(None))
    if genre:
        query = query.filter(Book.genre.ilike(f"%{genre}%"))
    if search:
        query = query.filter(
            or_(
                Book.title.ilike(f"%{search}%"),
                Book.author.ilike(f"%{search}%"),
            )
        )
    return query.all()


def get_borrowhistory(
    db: Session, user_id: Optional[int] = None,
    book_id: Optional[int] = None,
    search: Optional[str] = None):
    query = db.query(BorrowHistory).all()
    if user_id:
        query = query.filter(BookHistory.borrower_id == user_id)
        
    if book_id:
        query = query.filter(BookHistory.book_id == book_id)
    if search:
        query = query.join(BorrowHistory.book).join(BorrowHistory.user).filter(
            or_(
                Book.title.ilike(f"%{search}%"),
                User.name.ilike(f"%{search}%")
            )
        )
    return db.query(BorrowHistory).all()
