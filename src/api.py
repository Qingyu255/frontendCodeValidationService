from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from common.CodeValidator import CodeValidator
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


@app.post("/process_html/")
async def process_html(req: SubmissionRequest):
    print(req)
    # do stuff
    # Here you can process the HTML content, e.g., store it in the database, test, etc.

    # TODO: validation service returns result (decide return type)

    validationResult = code_validator.validate_HTML_CSS_JS_Code(req.code, req.questionId, req.id)
    print("Completed Result: ", validationResult)
    payload = {
        "message": "HTML String content received and processed.. wtv not", 
        "validation_outcome": validationResult
    }
    return payload

if __name__ == "__main__":
    uvicorn.run(app, port=5000)
