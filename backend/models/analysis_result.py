from sqlalchemy import Column, Integer, String, JSON, DateTime
from datetime import datetime
from database.connection import Base

class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, nullable=False)
    labels = Column(JSON, nullable=False)  # store list as JSON
    image_url = Column(String, nullable=True)  # optional
    created_at = Column(DateTime, default=datetime.utcnow)
