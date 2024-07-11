from pydantic import BaseModel
from typing import Optional, List

class SubmissionRequestModel(BaseModel):
    id: str
    userId: str
    questionId: str
    language: str
    code: str
    status: str
    result: Optional[str] = None
    createdAt: str

class SubmissionAcknowledgementModel(BaseModel):
    status: str
    id: str

class ValidationResultModel(BaseModel):
    status: str
    isCorrectAnswer: bool
    errorStackTrace: str
    logs: Optional[List[str]] = None