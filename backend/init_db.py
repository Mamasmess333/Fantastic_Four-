"""
Database initialization script.
Run this to create all tables defined in your models.
"""
from database.connection import Base, engine
from models.analysis_result import AnalysisResult

def init_db():
    """Create all tables in the database."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ All tables created successfully!")

if __name__ == "__main__":
    init_db()
