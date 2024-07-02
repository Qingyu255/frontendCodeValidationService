from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from common.CodeValidator import CodeValidator
from common.repositories.submission import SubmissionRepository
import asyncio
import uvicorn
# from typing import List, Dict, Optional

app = FastAPI()
code_validator = CodeValidator()

class SubmissionRequest(BaseModel):
    id: str
    userId: str
    questionId: str
    language: str
    code: str
    status: str
    result: Optional[str]
    createdAt: str

class SubmissionResponse(BaseModel):
    id: int
    ## fill in

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # Allow requests from specified origin
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

@app.get("/")
async def helloWorld():
    return {
        "data" : "Hello Code Validator"
    }


@app.post("/submission/")
async def submission(req: SubmissionRequest):
    try:
        print("Creating task...")
        asyncio.create_task(handle_submission(req))
        print("Created task! Now processing asynchronously")
        return { "statusCode": 200 }
    except Exception as e:
        print("Error: ", e)
        return { "statusCode": 500 }

async def handle_submission(req: SubmissionRequest):
    validation_result = code_validator.handle_submission(
        submission_type=req.language,
        question_id=req.questionId,
        submission_id=req.id,
        raw_string=req.code
    )
    
    submission_repository = SubmissionRepository()
    if validation_result:
        submission_repository.updateSubmission(req.id, "fail")
    else:
        submission_repository.updateSubmission(req.id, "success")
    return

if __name__ == "__main__":
    uvicorn.run(app, port=5000)
