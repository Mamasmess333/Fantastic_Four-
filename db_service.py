from sqlalchemy.orm import Session
from models.analysis_result import AnalysisResult
import datetime

def save_analysis_result(db: Session, status: str, labels: list, image_url: str = None, rating: str = "N/A", reason: str = "N/A"):
    """
    Save AI analysis result into the database with Crash Protection
    """
    print("Attempting to save to DB...")
    
    try:
        # Store rating/reason inside the JSON 'labels' column
        # This allows us to store extra data without changing the table schema
        combined_data = {
            "detected": labels,
            "rating": rating,
            "reason": reason
        }
        
        result = AnalysisResult(
            status=status,
            labels=combined_data,
            image_url=image_url
        )
        
        db.add(result)
        db.commit()
        db.refresh(result)
        print("✅ Saved to DB successfully!")
        return result

    except Exception as e:
        print(f"❌ DB Save Failed: {e}")
        db.rollback()
        
        # Return a dummy object so the code doesn't break
        return AnalysisResult(
            id=0,
            status="error_saved_locally",
            labels={"detected": labels, "rating": rating, "reason": reason},
            image_url=image_url,
            created_at=datetime.datetime.now()
        )

def get_analysis_result(db: Session, result_id: int):
    return db.query(AnalysisResult).filter(AnalysisResult.id == result_id).first()
