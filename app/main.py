from fastapi import FastAPI
from app.routers import student

app = FastAPI()
app.include_router(student.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

