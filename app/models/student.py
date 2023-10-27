from pydantic import BaseModel

class Student(BaseModel):
    id: int = None
    name: str
    age: int
    grade: int
    email: str
    password: str
