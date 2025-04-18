from pydantic import BaseModel

class GetAllBooks(BaseModel):
    id: int
    title: str
    author: str
    published_year: int
    
    
class CreateBook(BaseModel):
    title: str
    author: str
    published_year: int
    
    
    