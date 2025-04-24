from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import openai
import os

# Validate OpenAI API key at startup
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise RuntimeError("OPENAI_API_KEY environment variable is not set")

# Create FastAPI app with metadata
app = FastAPI(
    title="AI Text Summarization API",
    description="A microservice that provides text summarization using OpenAI's GPT model",
    version="1.0.0",
    contact={
        "name": "manola1109",
        "url": "https://github.com/manola1109"
    }
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SummarizationRequest(BaseModel):
    text: str = Field(..., description="The text to be summarized")
    max_tokens: Optional[int] = Field(
        150, ge=1, le=2000, description="Maximum tokens in the summary"
    )
    temperature: Optional[float] = Field(
        0.7, ge=0, le=1, description="Temperature for text generation"
    )

    class Config:
        schema_extra = {
            "example": {
                "text": "Your text to summarize goes here",
                "max_tokens": 150,
                "temperature": 0.7
            }
        }

class SummarizationResponse(BaseModel):
    summary: str
    original_length: int
    summary_length: int
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

    class Config:
        schema_extra = {
            "example": {
                "summary": "Summarized text example",
                "original_length": 100,
                "summary_length": 50,
                "created_at": "2025-04-24T08:15:25"
            }
        }

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Custom exception handler to format error responses.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "status_code": exc.status_code,
                "message": exc.detail,
                "timestamp": datetime.utcnow().isoformat()
            }
        }
    )

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint that provides basic API information and available endpoints.
    """
    return {
        "service": "AI Text Summarization API",
        "version": "1.0.0",
        "status": "operational",
        "current_time": datetime.utcnow().isoformat(),
        "endpoints": {
            "root": "/",
            "health": "/health",
            "docs": "/docs",
            "openapi": "/openapi.json",
            "summarize": "/summarize"
        },
        "maintainer": "manola1109"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify the service is running properly.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "environment": "development"
    }

@app.post("/summarize", response_model=SummarizationResponse, tags=["Summarization"])
async def summarize_text(request: SummarizationRequest):
    """
    Summarize the provided text using OpenAI's GPT model.
    """
    # Validate non-empty text
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    try:
        # Call OpenAI API for summarization
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a text-summarization expert. Provide concise summaries."},
                {"role": "user", "content": f"Summarize the following text:\n\n{request.text}"}
            ],
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        summary = resp.choices[0].message.content.strip()

    except HTTPException:
        # Propagate HTTPException (e.g., our 400 for empty text)
        raise
    except Exception as e:
        # Catch-all for other errors
        raise HTTPException(status_code=500, detail=f"Summarization failed: {e}")

    return SummarizationResponse(
        summary=summary,
        original_length=len(request.text),
        summary_length=len(summary),
        created_at=datetime.utcnow().isoformat()
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
