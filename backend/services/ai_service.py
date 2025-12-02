import boto3
import os
from typing import List
from urllib.parse import urlparse
from urllib.request import urlopen

from dotenv import load_dotenv

load_dotenv()


def _read_image_bytes(source: str) -> bytes:
    if source.startswith("http"):
        with urlopen(source) as response:
            return response.read()
    with open(source, "rb") as image_file:
        return image_file.read()


def analyze_image(image_source: str):
    try:
        aws_region = os.getenv("AWS_REGION") or "us-east-1"
        rekognition = boto3.client(
            "rekognition",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=aws_region,
        )

        image_bytes = _read_image_bytes(image_source)
        response = rekognition.detect_labels(Image={"Bytes": image_bytes}, MaxLabels=7)
        labels = [label["Name"] for label in response.get("Labels", [])]
        print("✅ Rekognition labels:", labels)
        return {"labels": labels}
    except Exception as e:
        print("❌ Error analyzing image:", e)
        return {"error": str(e)}


def analyze_text(ingredients: List[str]):
    clean = [token.strip().lower() for token in ingredients if token]
    return {"labels": [token.title() for token in clean]}
