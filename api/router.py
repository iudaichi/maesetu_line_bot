from fastapi import APIRouter

app = APIRouter()
pass_dic_n = {
    "a": "1",
    "r": "2",
    "b": "3",
    "k": "4",
    "s": "6",
    "z": "7",
    "p": "9",
}


@app.post("/test")
async def test():
    return {"result": "ok"}


@app.get("/reward/")
async def reward(password: str):
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
