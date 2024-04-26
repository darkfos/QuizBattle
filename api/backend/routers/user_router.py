from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.backend.schemas.UserPDSchema import *
from api.backend.services.UserService import UserAPIService
from api.db.db_engine import db_worker
from typing import Annotated


user_router: APIRouter = APIRouter(
    prefix="/user",
    tags=["User"]
)


@user_router.post("/create_user",
                  status_code=status.HTTP_201_CREATED,
                  response_model=UserIsCreatedPDSchema)
async def register_user(
    session: Annotated[AsyncSession, Depends(db_worker.get_session)],
    new_user: AddNewUserPDSchema
) -> UserIsCreatedPDSchema:
    """
    Create a new user
    """

    return UserIsCreatedPDSchema(
        is_created=await UserAPIService.create_new_user(session=session, user_data=new_user)
    )