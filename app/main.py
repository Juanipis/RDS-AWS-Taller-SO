from fastapi import FastAPI
from app.routers import s3, student

app = FastAPI()
app.include_router(student.router)
app.include_router(s3.router)
