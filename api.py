from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# from typing import List, Dict, Optional

app = FastAPI()

class SubmissionCreate(BaseModel):
    user_id: str
    ## fill in

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
        "data" : "Hello World"
    }

# @app.post("/submissions/", response_model=SubmissionResponse)
# def create_submission(submission: SubmissionCreate, db: Session = Depends(get_db)):
#     ### SUBMISSION LOGIC TO BD