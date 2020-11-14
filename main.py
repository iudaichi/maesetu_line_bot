from fastapi import FastAPI, Header, Body, HTTPException
from linebot.exceptions import InvalidSignatureError
from config.line_bot_api import handler
from api import router as api_router
from utils.line_router import TextMessageRouter
from linebot.models import MessageEvent, TextMessage
import json
from fastapi.staticfiles import StaticFiles
app = FastAPI()

app.include_router(
    api_router.app,
    prefix="/api",
    tags=["api"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.post("/callback")
def callback(X_Line_Signature: str = Header(...), body=Body(...)):
    try:
        body = json.dumps(body, ensure_ascii=False).replace(' ', '')
        handler.handle(body, X_Line_Signature)
    except InvalidSignatureError:
        raise HTTPException(
            status_code=400, detail=f"InvalidSignatureError")
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    TextMessageRouter(event).distribution_message()
