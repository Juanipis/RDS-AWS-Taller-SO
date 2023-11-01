from pydantic import BaseModel

class Student(BaseModel):
    id: str = ''
    name: str
    age: int
    grade: int
    email: str
    password: str
