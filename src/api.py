from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from common.CodeValidatorService import CodeValidatorService
from common.repositories.SubmissionService import SubmissionService
import asyncio
import uvicorn
from models.models import SubmissionRequestModel, SubmissionAcknowledgementModel, ValidationResultModel
import logging

logging.basicConfig(
    level=logging.INFO,
    format="SERVICE %(levelname)s: %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

app = FastAPI()
codeValidatorService = CodeValidatorService()

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

# acts as a cache for active submissions, stores ValidationResultModel objects (basically our responses)
submission_status_store = {}

@app.get("/")
async def helloWorld():
    return {
        "data" : "Hello Code Validator"
    }


@app.post("/submission", response_model=SubmissionAcknowledgementModel)
async def submission(req: SubmissionRequestModel) -> SubmissionAcknowledgementModel:
    try:
        submissionId = req.id
        submission_status_store[submissionId] = {"isCorrectAnswer":False, "errorStackTrace":"", "status": "processing"}
        logger.info("Creating task...")
        asyncio.create_task(handle_submission(req))
        logger.info("Created task! Now processing asynchronously")
        # return {"statusCode": 200, "message": "Submission received", "submission_id": submissionId}
        return SubmissionAcknowledgementModel(
            status="processing",
            id=submissionId
        )
    except Exception as e:
        logger.error("Unexpected Exception: ", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/submission_status/{submission_id}", response_model=ValidationResultModel)
async def get_submission_status(submission_id: str) -> ValidationResultModel:
    if submission_id not in submission_status_store:
        raise HTTPException(status_code=404, detail="Submission ID not found")

    return submission_status_store[submission_id]


async def handle_submission(req: SubmissionRequestModel):
    # see model for validation_result in models/models.py
    validationResultObj = codeValidatorService.handle_validation(
        submission_type=req.language,
        question_id=req.questionId,
        submission_id=req.id,
        raw_string=req.code
    )

    isCorrectAnswer = validationResultObj.isCorrectAnswer
    # errorStackTrace = validation_result.errorStackTrace
    # logs = validation_result.logs

    logger.info("DEBUG: validation result at api.py --> handle_submission: %s", validationResultObj)
    submission_repository = SubmissionService()
    if not isCorrectAnswer:
        submission_repository.updateSubmission(req.id, "fail")
    else:
        submission_repository.updateSubmission(req.id, "success")

    # store in cache
    submission_status_store[req.id] = validationResultObj

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
