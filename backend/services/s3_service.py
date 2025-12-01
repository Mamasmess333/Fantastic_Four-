import boto3
import os
from dotenv import load_dotenv
from uuid import uuid4

load_dotenv()

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_BUCKET = os.getenv("S3_BUCKET_NAME")
S3_REGION = os.getenv("AWS_REGION", "us-east-1")

s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=S3_REGION
)

def upload_to_s3(file_path):
    filename = os.path.basename(file_path)
    file_id = str(uuid4()) + "_" + filename

    with open(file_path, "rb") as f:
        s3.upload_fileobj(f, S3_BUCKET, file_id)

    return f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{file_id}"
