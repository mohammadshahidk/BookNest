from pydantic import BaseModel

class RegisterRequest(BaseModel):
    name: str
    phone: str
    password: str
    role: str
    
class UserList(BaseModel):
    id: int
    name: str
    phone: str
    role: str
    