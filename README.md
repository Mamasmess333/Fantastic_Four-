# 🧠 BiteWise AI - Food Image Analysis Platform

A full-stack **BiteWise AI** application that uses **AWS Rekognition**, **S3**, and **PostgreSQL** to identify food items from uploaded images and store analysis results. Built with **FastAPI** backend and vanilla JavaScript frontend.

---

## 🚀 Features

- **Image Upload & Analysis**: Upload food images and analyze them using AWS Rekognition
- **Cloud Storage**: Automatic upload to Amazon S3 with unique file identifiers
- **Database Persistence**: Store analysis results in PostgreSQL (AWS RDS)
- **RESTful API**: Fully integrated FastAPI backend with organized routes and services
- **Static Frontend Hosting**: Serves HTML/CSS/JS frontend directly from FastAPI
- **CORS-enabled**: Ready for frontend integration
- **Secure Configuration**: Environment-based setup for AWS and database credentials

---

## 🧩 Project Structure

```
Fantastic_Four-/
│
├── backend/
│   ├── app.py                    # FastAPI main entry point
│   ├── init_db.py                # Database initialization script
│   │
│   ├── routes/                   # API route handlers
│   │   ├── upload.py             # Image upload & analysis endpoint
│   │   └── analysis.py           # Additional analysis endpoints
│   │
│   ├── services/                 # Business logic services
│   │   ├── ai_service.py         # AWS Rekognition integration
│   │   ├── s3_service.py         # S3 file upload service
│   │   └── db_service.py         # Database operations
│   │
│   ├── database/                 # Database configuration
│   │   └── connection.py         # SQLAlchemy engine & session
│   │
│   ├── models/                   # Database models
│   │   └── analysis_result.py    # AnalysisResult ORM model
│   │
│   └── temp/                     # Temporary file storage for uploads
│
├── frontend/                     # Frontend static files
│   ├── index.html                # Main UI
│   └── script.js                 # Client-side logic
│
├── test/                         # Test files
│   ├── test_db.py                # Database tests
│   └── test_analysis_route.py    # API endpoint tests
│
├── .env.example                  # Environment variable template
├── .gitignore                    # Git ignore rules
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

---

## ⚙️ Setup Instructions

Follow these steps to get the application running locally:

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Mamasmess333/Fantastic_Four-.git
cd Fantastic_Four-
```

### 2️⃣ Set Up a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies include:**
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `boto3` - AWS SDK
- `python-dotenv` - Environment variable management
- `sqlalchemy` - ORM for database
- `psycopg2-binary` - PostgreSQL adapter

### 4️⃣ Create Your .env File

Copy the example file and fill in your credentials:

```bash
cp .env.example .env
```

Open `.env` and add your actual values:

```env
# AWS Credentials
AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY
AWS_REGION=us-east-2
S3_BUCKET_NAME=your-s3-bucket-name

# Database Configuration
endpoint=your-database-endpoint.rds.amazonaws.com
db_host=your-database-endpoint.rds.amazonaws.com
db_port=5432
db_name=your_database_name
db_user=your_database_user
db_pass=your_database_password

# Database URL (use your actual values from above)
DATABASE_URL=postgresql+psycopg2://db_user:db_pass@db_host:db_port/db_name
```

### 5️⃣ Initialize the Database

```bash
cd backend
python init_db.py
```

This creates the necessary tables in your PostgreSQL database.

### 6️⃣ Run the Server

```bash
cd backend
uvicorn app:app --reload
```

The application will start running at:
- **Backend API**: http://127.0.0.1:8000
- **Frontend UI**: http://127.0.0.1:8000
- **API Docs**: http://127.0.0.1:8000/docs

---

## 🧪 API Endpoints

Once the server is running, you can test the API at http://127.0.0.1:8000/docs

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Serves the frontend UI |
| `/upload` | POST | Uploads an image to S3, analyzes it with Rekognition, and saves results to DB |
| `/analyze` | POST | Analyzes an existing image by URL or path |
| `/static/*` | GET | Serves static frontend files |

### Example `/upload` Request

```bash
curl -X POST "http://127.0.0.1:8000/upload" \
  -F "file=@/path/to/image.jpg"
```

**Response:**
```json
{
  "status": "success",
  "labels": ["Pizza", "Food", "Dish", "Cheese"]
}
```

---

## 🧰 Environment Variables

| Variable | Description |
|----------|-------------|
| `AWS_ACCESS_KEY_ID` | Your AWS access key |
| `AWS_SECRET_ACCESS_KEY` | Your AWS secret key |
| `AWS_REGION` | AWS region for services (e.g., `us-east-2`) |
| `S3_BUCKET_NAME` | Name of your S3 bucket for image storage |
| `db_host` | PostgreSQL database host (RDS endpoint) |
| `db_port` | Database port (default: `5432`) |
| `db_name` | Database name |
| `db_user` | Database username |
| `db_pass` | Database password |
| `DATABASE_URL` | Full PostgreSQL connection string |

---

## 🗄️ Database Schema

### `analysis_results` Table

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer | Primary key, auto-increment |
| `status` | String | Analysis status (e.g., "success") |
| `labels` | JSON | Array of detected labels |
| `image_url` | String | S3 URL of uploaded image |
| `created_at` | DateTime | Timestamp of record creation |

---

## 🧑‍💻 Developer Notes

- **Never push your real `.env` file** — it's ignored by Git for security
- To update dependencies after adding new packages:
  ```bash
  pip freeze > requirements.txt
  ```
- To deactivate your environment:
  ```bash
  deactivate
  ```
- The `temp/` folder is created automatically for temporary file storage during uploads
- S3 files are saved with unique UUIDs to prevent naming conflicts

---

## 🧪 Testing

Run tests using pytest:

```bash
pytest test/
```

---

## 📦 Deployment

This project can be deployed on:
- **AWS EC2** (with RDS for database)
- **Render**
- **Railway**
- **Heroku**
- Or any VPS that supports Python 3.10+ and FastAPI

**Note**: Make sure to set all environment variables in your deployment platform's configuration.

---

## 🏁 Summary

✅ AWS Rekognition + S3 integration for image analysis
✅ PostgreSQL database with SQLAlchemy ORM
✅ RESTful FastAPI backend with organized architecture
✅ Static frontend hosting
✅ Secure environment-based configuration
✅ Easy setup for all team members

---

## 👥 Team Members & Contributions

### Jehun Kim's Contributions (branch: jkim)

**Backend Architecture & AWS Integration**

- **Project Restructuring**: Created `backend/` folder and reorganized project structure by moving `services/`, `routes/`, and `app.py` into organized directories
- **Database Integration**: Set up and configured AWS RDS PostgreSQL connection and implemented database persistence - analyzed data is now successfully saved to the database
- **Testing & Quality**: Built and refactored `test_db.py` for improved test coverage and maintainability
- **S3 Upload Fix**: Fixed critical bug where empty image files were being saved to S3 - now actual image files are properly uploaded with full content
- **Code Quality**: Fixed typos in `s3_service.py` and refactored upload logic for better reliability
- **Environment Configuration**: Updated `.env.example` to include comprehensive database configuration and DATABASE_URL examples
- **AWS Infrastructure**: Enhanced and customized the existing AWS setup—including S3, RDS PostgreSQL, and EC2—by modifying configurations and integrations to ensure seamless functionality with the project’s backend services

---

**Developed by the Fantastic Four Team** 💻
