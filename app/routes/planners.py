import json
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.dependencies import get_current_user
from app.db.database import get_db
from app.models.models import User, RecommendationHistory
from app.schemas.schemas import HomeRequest, PartyRequest, RecommendationResponse
from app.services.gemini_utils import generate_recommendations

router = APIRouter(tags=["planners"])

def save_history(db, user, planner, request_data, response_data):
    row = RecommendationHistory(
        user_id=user.id,
        planner=planner,
        request_json=json.dumps(request_data, ensure_ascii=False),
        response_json=json.dumps(response_data, ensure_ascii=False),
    )
    db.add(row)
    db.commit()

@router.post("/generate-home", response_model=RecommendationResponse)
def generate_home(data: HomeRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    result = generate_recommendations("home", data.model_dump())
    result["planner"] = "home"
    result["budget"] = data.budget
    save_history(db, user, "home", data.model_dump(), result)
    return result

@router.post("/generate-party", response_model=RecommendationResponse)
def generate_party(data: PartyRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    result = generate_recommendations("party", data.model_dump())
    result["planner"] = "party"
    result["budget"] = data.budget
    save_history(db, user, "party", data.model_dump(), result)
    return result

@router.post("/generate-jewelry", response_model=RecommendationResponse)
async def generate_jewelry(
    budget: float = Form(...),
    occasion: str = Form(...),
    style: str = Form("elegant"),
    preferences: str = Form(""),
    outfit_image: UploadFile | None = File(None),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if budget <= 0 or budget > 10_000_000:
        raise HTTPException(422, "Budget must be between 1 and 10,000,000")
    image_bytes = None
    image_mime = None
    if outfit_image:
        if outfit_image.content_type not in {"image/jpeg", "image/png", "image/webp"}:
            raise HTTPException(415, "Only JPG, PNG or WEBP images are supported")
        image_bytes = await outfit_image.read()
        if len(image_bytes) > 5 * 1024 * 1024:
            raise HTTPException(413, "Image must be 5 MB or smaller")
        image_mime = outfit_image.content_type

    payload = {
        "budget": budget,
        "occasion": occasion.strip(),
        "style": style.strip(),
        "preferences": preferences.strip(),
        "outfit_image_attached": bool(image_bytes),
    }
    result = generate_recommendations("jewelry", payload, image_bytes, image_mime)
    result["planner"] = "jewelry"
    result["budget"] = budget
    save_history(db, user, "jewelry", payload, result)
    return result
