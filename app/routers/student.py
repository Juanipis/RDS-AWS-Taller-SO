from fastapi import APIRouter, File, Form, UploadFile
from app.controller.s3 import s3_controller
from app.models.student import Student

router = APIRouter()

@router.post("/students/")
async def create_student(name: str = Form(...),
                        age: int = Form(...),
                        grade: int = Form(...),
                        email: str = Form(...),
                        password: str = Form(...),
                        profile_pic: UploadFile = File(...)):
    
    student = Student(name=name, age=age, grade=grade, email=email, password=password)
    profile_pic = await profile_pic.read()
    s3_controller.insert_json(student.model_dump_json(), f"students/{email}/student.json")
    s3_controller.insert_file(profile_pic, f"students/{email}/profile_pic.jpg")
    return {"status": "ok", "student": student, "file_name": f"students/{email}/profile_pic.jpg"}