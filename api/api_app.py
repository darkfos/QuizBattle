from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse
import uvicorn

#Routers
from api.backend.routers.auth_router import auth_app_router
from api.backend.routers.user_router import user_router


app: FastAPI = FastAPI(
    title="QuickBattleAPI",
    version="0.1.1"
)


#Include routers
app.include_router(
    auth_app_router
)
app.include_router(
    user_router
)


@app.get("/", status_code=status.HTTP_100_CONTINUE)
async def redirect_to_docs():
    return RedirectResponse("/docs")


def start_api_application():
    #Start api app
    uvicorn.run(
        app=app,
        host="127.0.0.1",
        port="7823",
        workers=True
    )