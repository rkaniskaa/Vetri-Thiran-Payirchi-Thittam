from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0"
)

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# HTML templates
templates = Jinja2Templates(directory="templates")


class TextRequest(BaseModel):
    text: str = Field(..., min_length=1)


class QARequest(BaseModel):
    question: str = Field(..., min_length=1)


class LearningRequest(BaseModel):
    topic: str = Field(..., min_length=1)
    level: str = "Beginner"


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "application": "EduGenie",
        "message": "EduGenie backend is running."
    }


@app.post("/qa")
async def qa_endpoint(request: QARequest):
    result = answer_question(request.question)

    return {
        "success": True,
        "result": result
    }


@app.post("/explain")
async def explain_endpoint(request: TextRequest):
    result = explain_topic(request.text)

    return {
        "success": True,
        "result": result
    }


@app.post("/quiz")
async def quiz_endpoint(request: TextRequest):
    result = generate_quiz(request.text)

    return {
        "success": True,
        "result": result
    }


@app.post("/summarize")
async def summarize_endpoint(request: TextRequest):
    result = summarize_text(request.text)

    return {
        "success": True,
        "result": result
    }


@app.post("/learn/recommendations")
async def learning_path_endpoint(request: LearningRequest):
    result = get_learning_recommendations(
        request.topic,
        request.level
    )

    return {
        "success": True,
        "result": result
    }


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    import traceback
    traceback.print_exc()

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": str(exc)
        }
    )