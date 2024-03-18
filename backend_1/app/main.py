from fastapi import FastAPI, File, UploadFile, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.session import session
from app.metrics import update_metrics
from prometheus_client.exposition import generate_latest, CONTENT_TYPE_LATEST

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/metrics")
def metrics(request: Request) -> Response:
    update_metrics()
    return Response(generate_latest(), headers={"Content-Type": CONTENT_TYPE_LATEST})


@app.post("/upload")
async def upload_file(audio_file: UploadFile = File(alias="audioFile")):
    """
    Endpoint to upload an audio file.
    """
    session.upload_file(await audio_file.read())
    return {"message": f"File '{audio_file.filename}' uploaded successfully."}


class SetTimeRequest(BaseModel):
    seconds: int


@app.post("/set-time")
async def set_time(request_body: SetTimeRequest):
    """
    Endpoint to set the current time in the audio.
    """
    session.set_time(request_body.seconds)
    return {"message": f"Current time set to {request_body.seconds} seconds."}


class SetUserActiveRequest(BaseModel):
    active: bool


@app.post("/set-user-active")
async def set_user_active(request_body: SetUserActiveRequest):
    """
    Endpoint to set the user activity.
    """
    session.set_user_active(request_body.active)
    return {"message": f"User activity set to {request_body.active}."}


@app.get("/info")
async def get_info():
    """
    Endpoint to get information about showing ads.
    """
    return {"showAds": session.show_ads()}
