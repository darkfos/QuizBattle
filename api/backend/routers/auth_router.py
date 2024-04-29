from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from api.backend.auth.security import SecurityAPI
from api.db.db_engine import db_worker
from api.backend.schemas.TokenPDSchema import *


#auth router
auth_app_router: APIRouter = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

#Security auth router
app_security: SecurityAPI = SecurityAPI()


@auth_app_router.post("/create_token/{telegram_id}",
                      status_code=status.HTTP_200_OK,
                      response_model=GetAccessToken)
async def create_access_token(
    session: Annotated[AsyncSession, Depends(db_worker.get_session)],
    telegram_id: int
) -> GetAccessToken:
    """
    Endpoint for create access token
    """

    user_id: int = await app_security.user_is_created(session=session, telegram_id=telegram_id)
    token: dict = await app_security.create_token(
        data_for_token=CreateAccessTokenPDSchema(telegram_id=telegram_id, user_id=user_id)
    )
    acs_token = GetAccessToken(token=token.get("token"))
    response = JSONResponse(
        content=acs_token.model_dump()
    )

    #Set cookies
    response.set_cookie(
        key="refresh_token", value=token.get("refresh_token")
    )

    return response

@auth_app_router.post("/refresh_token",
                      status_code=status.HTTP_200_OK,
                      response_model=GetAccessToken)
async def create_new_token_with_refresh(
    session: Annotated[AsyncSession, Depends(db_worker.get_session)],
    token: str,
) -> GetAccessToken:
    """
    Endpoint for create refresh token
    """

    result = await app_security.create_new_token_with_refresh(
        token=token
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Не удалось получить обновление токена"
        )
    
    response = JSONResponse(
        content=GetAccessToken(token=result.get("token")).model_dump()
    )

    return response