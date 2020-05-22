from fastapi import FastAPI
from cld3 import get_language
from utilities.summary import Summary


app = FastAPI()

@app.get("/")
def index():
    return {
        "about":
            "Sankshep provides text summarization as a service."
    }