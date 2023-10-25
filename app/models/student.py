from pydantic import BaseModel

class Student(BaseModel):
    name: str
    age: int
    grade: int
    email: str
    password: str
