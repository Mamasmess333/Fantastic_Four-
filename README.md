
# 🧠 BiteWise AI Backend

A FastAPI-based backend service for **BiteWise AI**, a smart food image analysis tool that uses **AWS Rekognition** and **S3** to identify food items from uploaded images and analyze nutritional data.

---

## 🚀 Features
- Upload images and analyze them using **AWS Rekognition**
- Store and retrieve files from **Amazon S3**
- Fully integrated **FastAPI** backend with organized routes and services
- CORS-enabled for frontend connection
- `.env`-based configuration for secure AWS integration

---

## 🧩 Project Structure


Fantastic_Four/
│
├── app.py                 # FastAPI main entry point
├── routes/                # API route handlers (upload, analysis, etc.)
├── services/              # S3 and AI (Rekognition) service logic
├── test/                  # Optional test files
├── temp/                  # Temporary file storage for uploads
│
├── .env.example           # Environment variable template (safe to share)
├── .gitignore             # Ignores sensitive and unneeded files
├── requirements.txt       # Python dependencies
└── venv/                  # (Local only) Python virtual environment

---

## ⚙️ Setup Instructions

Follow these steps to get the backend running locally:

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Mamasmess333/Fantastic_Four-.git
cd Fantastic_Four-


2️⃣ Set Up a Virtual Environment
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate


3️⃣ Install Dependencies
pip install -r requirements.txt


4️⃣ Create Your .env File
Copy the example file and fill in your AWS credentials:
cp .env.example .env

Open .env and add your own values:
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_here
AWS_REGION=us-east-1
S3_BUCKET_NAME=bitewise-ai-uploads


5️⃣ Run the Server
~/.local/bin/uvicorn app:app --reload

The backend will start running at:
http://127.0.0.1:8000


🧪 API Endpoints
Once the server is running, you can test the API at:
http://127.0.0.1:8000/docs

EndpointMethodDescription/uploadPOSTUploads an image to S3 and analyzes it with Rekognition/analysisGETRetrieves the results of image analysis/GETSimple health check for backend connection

🧰 Environment Variables
VariableDescriptionAWS_ACCESS_KEY_IDYour AWS access keyAWS_SECRET_ACCESS_KEYYour AWS secret keyAWS_REGIONThe region for your AWS services (e.g. us-east-1)S3_BUCKET_NAMEName of your S3 bucket for image storage

🧑‍💻 Developer Notes


Never push your real .env file — it’s ignored by Git for security.


To update dependencies after adding new packages:
pip freeze > requirements.txt



To deactivate your environment:
deactivate




👥 Team Collaboration


Main branch: main


Andrew’s branch: andrew


To create a new branch:
git checkout -b yourname-feature

To pull updates from main:
git pull origin main

To push your branch:
git push -u origin yourname-feature


📦 Deployment (Optional)
This project can be deployed on:


AWS EC2


Render


Railway


or any VPS that supports Python 3.10+ and FastAPI.



🏁 Summary
✅ Secure .env setup
✅ AWS Rekognition + S3 integration
✅ FastAPI backend ready to connect with frontend
✅ Easy setup for all team members

Developed by the Fantastic Four Team 💻

---

✅ Just copy all of that into a file named `README.md` in your project root — GitHub will render it perfectly.
