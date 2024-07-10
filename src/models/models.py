from pydantic import BaseModel
from typing import Optional, List

class SubmissionRequest(BaseModel):
    id: str
    userId: str
    questionId: str
    language: str
    code: str
    status: str
    result: Optional[str] = None
    createdAt: str

class SubmissionResponse(BaseModel):
    id: int
    ## fill in

class ValidationResultModel(BaseModel):
    isCorrectAnswer: bool
    errorStackTrace: str
    logs: Optional[List[str]] = None