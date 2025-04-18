from pydantic import BaseModel

class RegisterRequest(BaseModel):
    name: str
    phone: str
    password: str
    role: str