from app.controller.rds import rds_controller
from app.controller.s3 import s3_controller
from app.models.student import Student
import base64

class StudentLogic:
    def insert_student(self, student:Student, profile_pic:bytes):
        rds_controller.insert_student(student)
        student = rds_controller.get_student_email(student.email)
        s3_controller.insert_json(student.model_dump_json(), f"students/{student.id}/student.json")
        s3_controller.insert_file(profile_pic, f"students/{student.id}/profile_pic.jpg")
        return {"status": "ok", "student": student, "file_name": f"students/{student.id}/profile_pic.jpg"}
    
    def get_student(self, email:str)->(Student, str):
        student = rds_controller.get_student_email(email)
        if student.id >= 0:
            picture=s3_controller.get_file(f"students/{student.id}/profile_pic.jpg")
            picture_base64 = base64.b64encode(picture).decode('utf-8')
            return student, picture_base64
        else:
            return None, ''

student_logic = StudentLogic()