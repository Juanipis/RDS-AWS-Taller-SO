import boto3
import json
from logzero import logger
from pydantic_settings import BaseSettings


class S3Credentials(BaseSettings):
    aws_access_key_id: str
    aws_secret_access_key: str
    s3_bucket: str
    s3_region: str = 'us-west-1'
    drop_s3_bucket: bool = False

class S3Controller:
    def __init__(self, s3_credentials: S3Credentials):
        self.s3_bucket = s3_credentials.s3_bucket
        self.s3_client = boto3.client('s3', region_name=s3_credentials.s3_region,
                                        aws_access_key_id=s3_credentials.aws_access_key_id,
                                        aws_secret_access_key=s3_credentials.aws_secret_access_key)
        if s3_credentials.drop_s3_bucket:
            self.__empty_bucket(s3_credentials)

    def __empty_bucket(self, s3_credentials: S3Credentials):
        logger.info(f"Emptying bucket {s3_credentials.s3_bucket}")
        bucket_name = s3_credentials.s3_bucket
        objects = self.s3_client.list_objects_v2(Bucket=bucket_name)
        if "Contents" not in objects:
            logger.info(f"Bucket {bucket_name} is already empty")
            return
        try:
            logger.info(f"Deleting objects in bucket {bucket_name}")
            for object in objects["Contents"]:
                logger.info(f"Deleting {object['Key']}")
                self.s3_client.delete_object(Bucket=bucket_name, Key=object["Key"])
        
        except Exception as e:
            logger.error(f"Error deleting bucket {bucket_name}: {e}")
    
    def insert_json(self, json_data, s3_path:str):
        json_str = json.dumps(json_data)
        
        self.s3_client.put_object(Body=json_str, Bucket=self.s3_bucket, Key=s3_path)
        return f"JSON guardado en {s3_path} en el bucket {self.s3_bucket}"
    
    def insert_file(self, file:bytes, s3_path:str):
        self.s3_client.put_object(Body=file, Bucket=self.s3_bucket, Key=s3_path)
    
    def get_file(self, path: str) -> bytes:
        response = self.s3_client.get_object(Bucket=self.s3_bucket, Key=path)
        return response['Body'].read()
    
    def delete_file(self, path: str):
        self.s3_client.delete_object(Bucket=self.s3_bucket, Key=path)
        
    def get_all_files_path(self) -> (list, int):
        objects = self.s3_client.list_objects_v2(Bucket=self.s3_bucket)
        if "Contents" not in objects:
            return [], 0
        list_path = []
        for object in objects['Contents']:
            list_path.append(object['Key'])
        return list_path, len(list_path)

s3_controller = S3Controller(S3Credentials())

