from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class CaseRequest(BaseModel):
    age: int
    gender: str
    symptoms: List[str]
    duration: Optional[str] = None

class ConditionPrediction(BaseModel):
    name: str
    probability: float = Field(ge=0, le=1)

class AnalyzeResponse(BaseModel):
    success: bool
    predictions: list
    prediction_confidence: float
    certainty_level: str
    disclaimer: str

class SeverityLevel(str, Enum):
    mild = "mild"
    moderate = "moderate"
    severe = "severe"


class UserInput(BaseModel):
    symptoms: str = Field(min_length=3)
    duration: str = Field(min_length=1)
    age: int = Field(gt=0, lt=120)
    severity: SeverityLevel


class Condition(BaseModel):
    name: str
    probability: float


class AIResponse(BaseModel):
    conditions: List[Condition]


class FinalResponse(BaseModel):
    conditions: List[Condition]
    red_flag: bool
    message: str