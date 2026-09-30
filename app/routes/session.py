import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_current_user
from app.db.database import get_db
from app.models.models import User, RecommendationHistory

router = APIRouter(tags=["session"])

@router.get("/session-info")
def session_info(user: User = Depends(get_current_user)):
    return {"logged_in": True, "user_id": user.id, "name": user.name, "email": user.email}

@router.get("/session-data")
def session_data(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    count = db.query(RecommendationHistory).filter(RecommendationHistory.user_id == user.id).count()
    return {"user_id": user.id, "recommendation_count": count}

@router.get("/history")
def history(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = (
        db.query(RecommendationHistory)
        .filter(RecommendationHistory.user_id == user.id)
        .order_by(RecommendationHistory.created_at.desc())
        .limit(50).all()
    )
    return [{
        "id": row.id,
        "planner": row.planner,
        "created_at": row.created_at.isoformat(),
        "request": json.loads(row.request_json),
        "response": json.loads(row.response_json),
    } for row in rows]

@router.get("/recommendations-details/{history_id}")
def recommendation_details(history_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    row = db.query(RecommendationHistory).filter(
        RecommendationHistory.id == history_id,
        RecommendationHistory.user_id == user.id
    ).first()
    if not row:
        from fastapi import HTTPException
        raise HTTPException(404, "Recommendation not found")
    return {"id": row.id, "planner": row.planner, "request": json.loads(row.request_json), "response": json.loads(row.response_json)}
