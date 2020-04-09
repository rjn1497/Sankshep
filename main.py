from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def index():
    return {
        "about":
            "Sankshep provides text summarization as a service."
    }
