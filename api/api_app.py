from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse
import uvicorn


app: FastAPI = FastAPI(
    title="QuickBattleAPI",
    version="0.1.1"
)


@app.get("/", status_code=status.HTTP_100_CONTINUE)
async def redirect_to_docs():
    return RedirectResponse("/docs")


if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host="127.0.0.1",
        port="7823",
        workers=True
    )