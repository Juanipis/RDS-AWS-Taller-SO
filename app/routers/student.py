from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from app.models.student import Student
from app.usecase.students.student import student_logic
router = APIRouter()

@router.post("/students/insert")
async def create_student(name: str = Form(...),
                        age: int = Form(...),
                        grade: int = Form(...),
                        email: str = Form(...),
                        password: str = Form(...),
                        profile_pic: UploadFile = File(...)):
    
    student = Student(name=name, age=age, grade=grade, email=email, password=password)
    profile_pic = await profile_pic.read()
    return student_logic.insert_student(student, profile_pic)

@router.get("/students/get")
async def get_student(email: str):
    student, picture = student_logic.get_student(email)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"student": student, "picture": picture}