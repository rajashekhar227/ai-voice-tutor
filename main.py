from fastapi import FastAPI, Request

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


@app.get("/ivr/exotel")
async def exotel_ivr(request: Request):
    # Get all parameters sent by Exotel
    params = dict(request.query_params)

    # Get the keypad digit
    digits = params.get("digits", "")

    # Remove quotes that Exotel may send around the digit
    digits = digits.strip('"')

    print("Exotel request:", params)
    print("Key pressed:", digits)

    return {
        "status": "success",
        "digit": digits
    }