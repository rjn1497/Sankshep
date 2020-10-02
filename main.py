from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from cld3 import get_language
from utilities.summary import Summary

app = FastAPI()

class TextSummary(BaseModel):
    summary: str
    reponse_length: int
    original_length: int

@app.get("/")
def index():
    return {
        "about":
            "Sankshep provides text summarization as a service."
    }

@app.get("/summarize", response_model=TextSummary)
def get_summary(text: str, percentage: float=None, abstractive: bool=False):
    if get_language(text).language != 'hi':
        raise HTTPException(status_code=418, detail="Summarization only available for Hindi.")

    summary = Summary(text, percentage, abstractive)
    response_length = len(summary)
    original_length = len(text)
    
    return {
        "summary": summary,
        "response_length": response_length,
        "original_length": original_length
        }
