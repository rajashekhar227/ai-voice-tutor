
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, Response
from pydantic import BaseModel


# ============================================================
# APP
# ============================================================

app = FastAPI(
    title="AI Voice Tutor IVR",
    description="AI Voice Tutor IVR service",
    version="1.0.0"
)


# ============================================================
# PATHS
# ============================================================

AUDIO_DIRECTORY = Path("data/audio").resolve()


# ============================================================
# REQUEST MODELS
# ============================================================

class DigitRequest(BaseModel):
    digit: str


class SubjectRequest(BaseModel):
    language: str
    digit: str


class TopicRequest(BaseModel):
    language: str
    subject: str
    digit: str


# ============================================================
# LESSON DATABASE
# ============================================================

LESSONS = {
    "english": {
        "science": {
            "1": {
                "topic": "Kharif Crops",
                "file": "hesc1dd_kharif_crops_english.wav"
            }
        }
    },

    "hindi": {
        "science": {
            "1": {
                "topic": "Kharif Crops",
                "file": "hesc1dd_kharif_crops_hindi.wav"
            }
        }
    },

    "telugu": {
        "science": {
            "1": {
                "topic": "Kharif Crops",
                "file": "hesc1dd_kharif_crops_telugu.wav"
            }
        }
    }
}


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {
        "status": "running",
        "service": "AI Voice Tutor IVR"
    }


# ============================================================
# START IVR
# ============================================================

@app.get("/ivr")
def start_ivr():

    return {
        "success": True,
        "message": "Welcome to AI Voice Tutor",
        "options": {
            "1": "English",
            "2": "Hindi",
            "3": "Telugu"
        }
    }


# ============================================================
# LANGUAGE SELECTION
# ============================================================

@app.post("/ivr/language")
def select_language(request: DigitRequest):

    languages = {
        "1": "english",
        "2": "hindi",
        "3": "telugu"
    }

    language = languages.get(request.digit)

    if language is None:

        return {
            "success": False,
            "message": "Invalid language selection",
            "options": {
                "1": "English",
                "2": "Hindi",
                "3": "Telugu"
            }
        }

    return {
        "success": True,
        "language": language,
        "message": f"{language.title()} selected",
        "next": "/ivr/subject"
    }


# ============================================================
# SUBJECT SELECTION
# ============================================================

@app.post("/ivr/subject")
def select_subject(request: SubjectRequest):

    language = request.language.lower()
    digit = request.digit

    # Check language
    if language not in LESSONS:

        return {
            "success": False,
            "message": "Invalid language"
        }

    subjects = {
        "1": "science"
    }

    subject = subjects.get(digit)

    if subject is None:

        return {
            "success": False,
            "message": "Invalid subject selection",
            "options": {
                "1": "Science"
            }
        }

    return {
        "success": True,
        "language": language,
        "subject": subject,
        "message": f"{subject.title()} selected",
        "next": "/ivr/topic"
    }


# ============================================================
# TOPIC SELECTION
# ============================================================

@app.post("/ivr/topic")
def select_topic(request: TopicRequest):

    language = request.language.lower()
    subject = request.subject.lower()
    digit = request.digit

    # Check language
    if language not in LESSONS:

        return {
            "success": False,
            "message": "Invalid language"
        }

    # Check subject
    if subject not in LESSONS[language]:

        return {
            "success": False,
            "message": "Invalid subject"
        }

    # Find lesson
    lesson = LESSONS[language][subject].get(digit)

    if lesson is None:

        return {
            "success": False,
            "message": "Invalid topic selection",
            "options": {
                "1": "Kharif Crops"
            }
        }

    filename = lesson["file"]

    audio_path = AUDIO_DIRECTORY / filename

    # Check audio exists
    if not audio_path.exists():

        return {
            "success": False,
            "message": "Audio file not found",
            "file": filename
        }

    return {
        "success": True,
        "language": language,
        "subject": subject,
        "topic": lesson["topic"],
        "audio_file": filename,
        "audio_url": f"/audio/{filename}"
    }


# ============================================================
# AUDIO FILE
# ============================================================

@app.get("/audio/{filename}")
def get_audio(filename: str):

    audio_path = AUDIO_DIRECTORY / filename

    # Security check
    try:

        audio_path.resolve().relative_to(
            AUDIO_DIRECTORY
        )

    except ValueError:

        return Response(
            content="Invalid audio path",
            status_code=400
        )

    # File doesn't exist
    if not audio_path.exists():

        return Response(
            content="Audio file not found",
            status_code=404
        )

    # Only WAV files
    if audio_path.suffix.lower() != ".wav":

        return Response(
            content="Only WAV files are allowed",
            status_code=400
        )

    return FileResponse(
        path=audio_path,
        media_type="audio/wav",
        filename=audio_path.name
    )

