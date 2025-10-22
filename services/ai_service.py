import boto3
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

def analyze_image(image_path: str):
    try:
        # Get values from environment (with fallback)
        aws_region = os.getenv("AWS_REGION") or "us-east-1"

        rekognition = boto3.client(
            "rekognition",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=aws_region,
        )

        with open(image_path, "rb") as image_file:
            response = rekognition.detect_labels(
                Image={"Bytes": image_file.read()},
                MaxLabels=5
            )

        labels = [label["Name"] for label in response["Labels"]]
        return {"labels": labels}

    except Exception as e:
        print(f"Error analyzing image: {e}")
        return {"error": str(e)}
