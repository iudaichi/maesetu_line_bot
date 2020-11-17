from fastapi import FastAPI, Header, Body, HTTPException, Request
from linebot.exceptions import InvalidSignatureError
from config.line_bot_api import handler
from api import router as api_router
from utils.line_router import TextMessageRouter
from linebot.models import MessageEvent, TextMessage
import json
from fastapi.staticfiles import StaticFiles
import datetime
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")
app = FastAPI()

app.include_router(
    api_router.app,
    prefix="/api",
    tags=["api"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")
pass_dic_n = {
    "a": "1",
    "r": "2",
    "b": "3",
    "k": "4",
    "s": "6",
    "z": "7",
    "p": "9",
}


@app.post("/callback")
def callback(X_Line_Signature: str = Header(...), body=Body(...)):
    try:
        body = json.dumps(body, ensure_ascii=False).replace(' ', '')
        handler.handle(body, X_Line_Signature)
    except InvalidSignatureError:
        raise HTTPException(
            status_code=400, detail=f"InvalidSignatureError")
    return 'OK'


@app.get("/test")
async def test(password: str):
    try:
        password_n = ""
        for x in str(password):
            if x in pass_dic_n:
                password_n += pass_dic_n[x]
            else:
                password_n += x
        print(password_n)
        pass1 = int(password_n[-2:])
        pass2 = int(password_n[:1])
        num = password_n[1:-2]
        num = str(int(num, pass1))
        num = int(num, pass2)
        return {
            "result": "ok",
            "password_n": password_n,
            "num": num
        }
    except Exception:
        return {
            "result": "ng",
        }


@app.get("/reward/")
async def reward(request: Request, password: str):
    password_n = ""
    for x in str(password):
        if x in pass_dic_n:
            password_n += pass_dic_n[x]
        else:
            password_n += x
    print(password_n)
    pass1 = int(password_n[-2:])
    pass2 = int(password_n[:1])
    num = password_n[1:-2]
    num = str(int(num, pass1))
    num = int(num, pass2)
    with open('config/time.json') as f:
        time_list = json.load(f)
    now_time = datetime.datetime.now().timestamp()
    if password_n in time_list:
        if now_time + 600 > time_list[password_n]:
            return {"no": "sss"}
    time_list[password_n] = datetime.datetime.now().timestamp()
    with open('config/test2.json', 'w') as f:
        json.dump(time_list, f, indent=4)
    image_file = "logo.png"
    return templates.TemplateResponse("sub.html", {"request": request, "number": num, "image": f'/static/{image_file}'})


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    TextMessageRouter(event).distribution_message()
