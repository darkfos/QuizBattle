from pydantic import BaseModel, Field
from typing import Annotated


class CreateAccessTokenPDSchema(BaseModel):

    telegram_id: Annotated[int, Field()]
    user_id: Annotated[int, Field()]


class GetAccessToken(BaseModel):

    token: Annotated[str, Field()]


class GetRefreshToken(BaseModel):

    refresh_token: Annotated[str, Field()]
    