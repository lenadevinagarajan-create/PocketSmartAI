from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class HomeRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    rooms: str = Field(min_length=2, max_length=500)
    style: str = Field(default="modern", max_length=100)
    requirements: str = Field(default="", max_length=2000)

class PartyRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    guests: int = Field(gt=0, le=10000)
    event_type: str = Field(min_length=2, max_length=100)
    venue: str = Field(default="", max_length=500)
    preferences: str = Field(default="", max_length=2000)

class RecommendationItem(BaseModel):
    name: str
    category: str
    estimated_price: float
    platform: str
    reason: str
    url: str

class RecommendationResponse(BaseModel):
    planner: str
    budget: float
    budget_used: float
    summary: str
    allocations: dict[str, float]
    recommendations: list[RecommendationItem]
    source: str
    warning: Optional[str] = None

class HistoryItem(BaseModel):
    id: int
    planner: str
    created_at: str
    request: dict
    response: dict
    model_config = ConfigDict(from_attributes=True)
