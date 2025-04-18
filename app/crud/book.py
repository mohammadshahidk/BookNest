from sqlalchemy.orm import Session
from app.models import Book


def get_all_books(db: Session):
    return db.query(Book).all()


