from fastapi import APIRouter

app = APIRouter()


@app.post("/test")
async def test():
    return {"result": "ok"}
