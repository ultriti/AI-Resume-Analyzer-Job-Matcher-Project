
from pydantic import BaseModel, Field
from typing import Optional

# --------------------------------------
#  input schema -----------------------
class TextInput(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="the sentence to analyze",
        json_schema_extra={"example": "i am so much happy for this"},
    )


class PredictionResponse(BaseModel):
    text: str
    prediction_emotion: str
    confidence: float
    all_probabilities: dict[str, float]


class JobMatch(BaseModel):
    role: str
    score: float
    matched_skills: list[str]
    missing_skills: list[str]


class ResumeAnalysisResponse(BaseModel):
    job_title: Optional[str]
    skills: list[str]
    prediction_category: str
    confidence: float
    all_probabilities: dict[str, float]
    job_analysis: list[JobMatch]


class HealthRepsonse(BaseModel):
    status: str
    model_loaded: bool
