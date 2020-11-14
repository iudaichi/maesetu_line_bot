from main import app
import os
import uvicorn

if __name__ == '__main__':
    port = int(os.getenv("PORT"))
    uvicorn.run(app, host="0.0.0.0", port=port, workers=1, reload=True)
