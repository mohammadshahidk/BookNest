from fastapi import FastAPI
from app.routers import users, books
 
app = FastAPI()

app.include_router(users.router, prefix='/users', tags=['users'])
app.include_router(books.router, prefix='/books', tags=['books'])
