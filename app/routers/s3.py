from fastapi import APIRouter
from app.usecase.s3.s3 import rds_logic
router = APIRouter()

@router.get("/get_all_bucket_files")
async def get_all_bucket_files():
    file_list, file_count = rds_logic.get_all_files()
    return {"file_count":file_count, "file_list": file_list, }