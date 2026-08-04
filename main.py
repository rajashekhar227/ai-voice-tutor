from fastapi import FastAPI

app = FastAPI(
    title="AI Voice Tutor API",
    version="1.0.0",
    description="Backend for AI Voice Tutor"
)

@app.get("/")
def home():
    return {
        "message": "Welcome to AI Voice Tutor API",
        "status": "Running"
    }