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
import redis

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
    if int(password_n[-2:]) + int(password_n[:1]) == 20:
        num = int(password_n[1:-2])
        pool = redis.ConnectionPool(host='pike.redistogo.com',
                                    port=11574, db=0, password='585f4a2cfe0f853d9753d7dd38a550d2')
        r = redis.StrictRedis(connection_pool=pool)
        now_time = datetime.datetime.now().timestamp()
        o_time = r.get(password_n)
        if o_time:
            o_time = str(o_time, encoding='utf-8')
            if now_time > float(o_time) + 600:
                return {"no": "sss"}
        r.set(password_n, datetime.datetime.now().timestamp())
        if num > 999999:
            image_file = "logo.png"
            image_title = "はしれ！まえせつロゴ"
            image_desc = "はしれ！まえせつのために作ったオリジナルロゴです。"
            image_num = "100000"
        elif num > 199999:
            image_file = "ed.png"
            image_title = "はしれ！まえせつリザルト"
            image_desc = "はしれ！まえせつのために作ったオリジナルリザルト画面です。"
            image_num = "20000"
        elif num > 9999:
            image_file = "ed.png"
            image_title = "はしれ！まえせつリザルト"
            image_desc = "はしれ！まえせつのために作ったオリジナルリザルト画面です。"
            image_num = "10000"
        else:
            image_file = "kon.jpg"
            image_title = "困惑してるまふゆ"
            image_desc = "困惑しているまふゆです"
            image_num = "100"
    return templates.TemplateResponse("sub.html", {
        "request": request,
        "number": str(num),
        "image_url": f'https://maesetu-line-bot.herokuapp.com/static/{image_file}',
        "image_title": image_title,
        "image_desc": image_desc,
        "image_num": f"{image_num}点以上特典です。"

    })


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    TextMessageRouter(event).distribution_message()
