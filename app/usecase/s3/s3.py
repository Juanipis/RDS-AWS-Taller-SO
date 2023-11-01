
from app.controller.s3 import s3_controller


class RDSLogic:
    def get_all_files(self) -> (list, int):
        filenames, file_count = s3_controller.get_all_files_path()
        return filenames, file_count

rds_logic = RDSLogic()