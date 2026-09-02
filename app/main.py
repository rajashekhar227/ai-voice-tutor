from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, Response
from pydantic import BaseModel
from twilio.twiml.voice_response import VoiceResponse, Gather

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

# IMPORTANT:
# This is your CURRENT Cloudflare URL.
PUBLIC_BASE_URL = "https://cedar-codes-lab-genealogy.trycloudflare.com"


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
# START IVR - JSON TEST API
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
# LANGUAGE SELECTION - JSON TEST API
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
# SUBJECT SELECTION - JSON TEST API
# ============================================================

@app.post("/ivr/subject")
def select_subject(request: SubjectRequest):

    language = request.language.lower()
    digit = request.digit

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
# TOPIC SELECTION - JSON TEST API
# ============================================================

@app.post("/ivr/topic")
def select_topic(request: TopicRequest):

    language = request.language.lower()
    subject = request.subject.lower()
    digit = request.digit

    if language not in LESSONS:

        return {
            "success": False,
            "message": "Invalid language"
        }

    if subject not in LESSONS[language]:

        return {
            "success": False,
            "message": "Invalid subject"
        }

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
# EXOTEL - PASSTHRU TEST
# ============================================================

@app.get("/ivr/exotel")
async def exotel_ivr(request: Request):

    params = dict(request.query_params)

    digits = params.get("digits", "")

    # Exotel may send the digit with quotes.
    digits = digits.strip('"')

    print("Exotel request:", params)
    print("Key pressed:", digits)

    return {
        "status": "success",
        "digit": digits
    }


# ============================================================
# TWILIO - INCOMING CALL
# ============================================================

@app.post("/ivr/call")
def twilio_call():

    response = VoiceResponse()

    gather = Gather(
        action="/ivr/twilio-language",
        method="POST",
        num_digits=1,
        timeout=10
    )

    gather.say(
        "Welcome to AI Voice Tutor.",
        language="en-US",
        voice="alice"
    )

    gather.say(
        "Press 1 for English. "
        "Press 2 for Hindi. "
        "Press 3 for Telugu.",
        language="en-US",
        voice="alice"
    )

    response.append(gather)

    response.say(
        "No input received. Goodbye.",
        language="en-US",
        voice="alice"
    )

    response.hangup()

    return Response(
        content=str(response),
        media_type="application/xml"
    )


# ============================================================
# TWILIO - LANGUAGE
# ============================================================

@app.post("/ivr/twilio-language")
async def twilio_language(request: Request):

    form = await request.form()

    digit = form.get("Digits")

    response = VoiceResponse()

    languages = {
        "1": "english",
        "2": "hindi",
        "3": "telugu"
    }

    language = languages.get(digit)

    if language is None:

        response.say(
            "Invalid selection. Please try again.",
            language="en-US",
            voice="alice"
        )

        response.redirect(
            f"{PUBLIC_BASE_URL}/ivr/call"
        )

        return Response(
            content=str(response),
            media_type="application/xml"
        )

    # --------------------------------------------------------
    # SUBJECT MENU
    # --------------------------------------------------------

    gather = Gather(
        action=(
            f"{PUBLIC_BASE_URL}"
            f"/ivr/twilio-subject?language={language}"
        ),
        method="POST",
        num_digits=1,
        timeout=10
    )

    if language == "hindi":

        gather.say(
            "Aapne Hindi chuna hai.",
            language="hi-IN",
            voice="alice"
        )

        gather.say(
            "Science ke liye 1 dabayein.",
            language="hi-IN",
            voice="alice"
        )

    elif language == "telugu":

        gather.say(
            "Meeru Telugu enchukunnaru.",
            language="en-IN",
            voice="alice"
        )

        gather.say(
            "Science kosam 1 nokkandi.",
            language="en-IN",
            voice="alice"
        )

    else:

        gather.say(
            "You selected English.",
            language="en-US",
            voice="alice"
        )

        gather.say(
            "Press 1 for Science.",
            language="en-US",
            voice="alice"
        )

    response.append(gather)

    response.say(
        "No input received. Goodbye.",
        language="en-US",
        voice="alice"
    )

    response.hangup()

    return Response(
        content=str(response),
        media_type="application/xml"
    )


# ============================================================
# TWILIO - SUBJECT
# ============================================================

@app.post("/ivr/twilio-subject")
async def twilio_subject(
    request: Request,
    language: str
):

    form = await request.form()

    digit = form.get("Digits")

    response = VoiceResponse()

    if digit != "1":

        response.say(
            "Invalid subject selection. Goodbye.",
            language="en-US",
            voice="alice"
        )

        response.hangup()

        return Response(
            content=str(response),
            media_type="application/xml"
        )

    # --------------------------------------------------------
    # TOPIC MENU
    # --------------------------------------------------------

    gather = Gather(
        action=(
            f"{PUBLIC_BASE_URL}"
            f"/ivr/twilio-topic"
            f"?language={language}"
            f"&subject=science"
        ),
        method="POST",
        num_digits=1,
        timeout=10
    )

    if language == "hindi":

        gather.say(
            "Aapne Science chuna hai.",
            language="hi-IN",
            voice="alice"
        )

        gather.say(
            "Kharif Crops ke lesson ke liye 1 dabayein.",
            language="hi-IN",
            voice="alice"
        )

    elif language == "telugu":

        gather.say(
            "Meeru Science enchukunnaru.",
            language="en-IN",
            voice="alice"
        )

        gather.say(
            "Kharif Crops lesson kosam 1 nokkandi.",
            language="en-IN",
            voice="alice"
        )

    else:

        gather.say(
            "You selected Science.",
            language="en-US",
            voice="alice"
        )

        gather.say(
            "Press 1 for Kharif Crops.",
            language="en-US",
            voice="alice"
        )

    response.append(gather)

    response.say(
        "No input received. Goodbye.",
        language="en-US",
        voice="alice"
    )

    response.hangup()

    return Response(
        content=str(response),
        media_type="application/xml"
    )


# ============================================================
# TWILIO - TOPIC AND AUDIO
# ============================================================

@app.post("/ivr/twilio-topic")
async def twilio_topic(
    request: Request,
    language: str,
    subject: str
):

    form = await request.form()

    digit = form.get("Digits")

    response = VoiceResponse()

    if digit != "1":

        response.say(
            "Invalid topic selection. Goodbye.",
            language="en-US",
            voice="alice"
        )

        response.hangup()

        return Response(
            content=str(response),
            media_type="application/xml"
        )

    # --------------------------------------------------------
    # FIND LESSON
    # --------------------------------------------------------

    lesson = (
        LESSONS
        .get(language, {})
        .get(subject, {})
        .get("1")
    )

    if lesson is None:

        response.say(
            "Lesson not found. Goodbye.",
            language="en-US",
            voice="alice"
        )

        response.hangup()

        return Response(
            content=str(response),
            media_type="application/xml"
        )

    filename = lesson["file"]

    audio_path = AUDIO_DIRECTORY / filename

    # --------------------------------------------------------
    # CHECK AUDIO
    # --------------------------------------------------------

    if not audio_path.exists():

        response.say(
            "The lesson audio could not be found.",
            language="en-US",
            voice="alice"
        )

        response.hangup()

        return Response(
            content=str(response),
            media_type="application/xml"
        )

    # --------------------------------------------------------
    # PUBLIC AUDIO URL
    # --------------------------------------------------------

    audio_url = (
        f"{PUBLIC_BASE_URL}"
        f"/audio/{filename}"
    )

    # --------------------------------------------------------
    # PLAY LESSON
    # --------------------------------------------------------

    response.say(
        "Starting your lesson.",
        language="en-US",
        voice="alice"
    )

    response.play(audio_url)

    response.say(
        "Lesson completed. Thank you for using AI Voice Tutor.",
        language="en-US",
        voice="alice"
    )

    response.hangup()

    return Response(
        content=str(response),
        media_type="application/xml"
    )


# ============================================================
# AUDIO FILE
# ============================================================

@app.get("/audio/{filename}")
def get_audio(filename: str):

    audio_path = AUDIO_DIRECTORY / filename

    # --------------------------------------------------------
    # SECURITY CHECK
    # --------------------------------------------------------

    try:

        audio_path.resolve().relative_to(
            AUDIO_DIRECTORY
        )

    except ValueError:

        return Response(
            content="Invalid audio path",
            status_code=400
        )

    # --------------------------------------------------------
    # FILE DOESN'T EXIST
    # --------------------------------------------------------

    if not audio_path.exists():

        return Response(
            content="Audio file not found",
            status_code=404
        )

    # --------------------------------------------------------
    # ONLY WAV FILES
    # --------------------------------------------------------

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