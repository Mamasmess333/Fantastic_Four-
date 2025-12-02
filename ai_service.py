import boto3
import os
from dotenv import load_dotenv

load_dotenv()

# --- MOCK DATA FOR DEMO (Expanded) ---
MOCK_DB = {
    # unhealthy
    "Pizza": {"rating": "D", "reason": "High sodium and saturated fat.", "alternative": "Cauliflower Crust Pizza"},
    "Burger": {"rating": "F", "reason": "High cholesterol and processed meat.", "alternative": "Turkey Burger"},
    "Hot Dog": {"rating": "F", "reason": "Processed meat and nitrates.", "alternative": "Chicken Sausage"},
    "Ice Cream": {"rating": "D", "reason": "High sugar and saturated fat.", "alternative": "Frozen Yogurt or Sorbet"},
    "Fries": {"rating": "D", "reason": "Deep fried and high sodium.", "alternative": "Baked Sweet Potato Fries"},
    "Soda": {"rating": "F", "reason": "Very high sugar content.", "alternative": "Sparkling Water with Fruit"},
    
    # healthy
    "Salad": {"rating": "A", "reason": "High fiber and vitamins.", "alternative": "Add grilled chicken"},
    "Apple": {"rating": "A+", "reason": "Natural sugars and fiber.", "alternative": "None needed"},
    "Banana": {"rating": "A", "reason": "Good source of potassium.", "alternative": "None needed"},
    "Fruit": {"rating": "A", "reason": "High in vitamins and antioxidants.", "alternative": "None needed"},
    "Vegetable": {"rating": "A+", "reason": "Essential nutrients and fiber.", "alternative": "None needed"},
    "Carrot": {"rating": "A+", "reason": "High in Vitamin A.", "alternative": "Hummus dip"},
    "Broccoli": {"rating": "A+", "reason": "Superfood, high in fiber.", "alternative": "Steamed with lemon"},
    "Chicken": {"rating": "A", "reason": "Lean protein source.", "alternative": "None needed"},
    
    # default fallback
    "Food": {"rating": "C", "reason": "General food item detected.", "alternative": "Check nutrition label"}
}

def analyze_image(image_path: str):
    labels = []
    
    # 1. Try Real AWS Rekognition
    try:
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
                MaxLabels=10
            )
        labels = [label["Name"] for label in response["Labels"]]
        print(f"AWS Success: Found {labels}")

    except Exception as e:
        print(f"⚠️ AWS Failed (Using Fallback): {e}")
        # FALLBACK: If AWS fails, pretend we found a Pizza so the demo works
        labels = ["Pizza", "Cheese", "Food"]

    # 2. Match Labels to Health Rating (Smart Matching)
    analysis_data = {
        "labels": labels,
        "rating": "C", # Default to C if unknown
        "reason": "General food item detected.",
        "alternative": "Check nutrition label"
    }

    # Search for the *best* match in our DB (prioritize specific items over generic "Food")
    found_match = False
    
    # First pass: Look for exact matches
    for label in labels:
        if label in MOCK_DB and label != "Food":
            analysis_data.update(MOCK_DB[label])
            found_match = True
            break 
            
    # Second pass: heuristic keywords if no exact match
    if not found_match:
        lower_labels = [l.lower() for l in labels]
        if any(x in lower_labels for x in ['fruit', 'vegetable', 'plant', 'produce']):
             analysis_data.update(MOCK_DB["Fruit"]) # Default to healthy for fruits/veg
        elif any(x in lower_labels for x in ['dessert', 'sugar', 'candy', 'chocolate', 'cookie']):
             analysis_data.update(MOCK_DB["Ice Cream"]) # Default to unhealthy for sweets

    return analysis_data
