from sqlalchemy.orm import Session
from models.analysis_result import AnalysisResult

def save_analysis_result(db: Session, status: str, labels: list, user_id: int, image_url: str = None):
    """
    Save AI analysis result into the database
    """
    print("line 8 db_service.py")
    result = AnalysisResult(
        user_id=user_id,
        status=status,
        labels=labels,
        image_url=image_url
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result


def get_analysis_result(db: Session, result_id: int):
    return db.query(AnalysisResult).filter(AnalysisResult.id == result_id).first()
