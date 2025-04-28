import csv
from typing import List
from app.schemas import books as book_schemas
from app.schemas import users as user_schemas
from io import StringIO

def parse_csv(file_contents: str) -> List[book_schemas.BookCreate]:
    reader = csv.DictReader(StringIO(file_contents))
    books = []
    for row in reader:
        books.append(book_schemas.BookCreate(**row))
    return books


def parse_user_csv(file_contents: str) -> List[user_schemas.RegisterRequest]:
    reader = csv.DictReader(StringIO(file_contents))
    users = []
    for row in reader:
        users.append(user_schemas.RegisterRequest(
                    phone=str(row['phone']),
                    name=row['name'],
                    role=row['role'],
                    password=row['password']
                ))
    return users
