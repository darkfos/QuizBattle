from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.backend.schemas.UserPDSchema import *
from api.backend.schemas.TokenPDSchema import GetAccessToken
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


@user_router.get("/about_me",
                 status_code=status.HTTP_200_OK,
                 response_model=UserBasePDSchema)
async def get_info_about_user(
    session: Annotated[AsyncSession, Depends(db_worker.get_session)],
    token: str
) -> UserBasePDSchema:
    """
    Endpoint which return info about user
    """

    return await UserAPIService.get_user_info(
        session=session,
        token=token
    )


@user_router.get("/about_me/full-information",
                 status_code=status.HTTP_200_OK,
                 response_model=UserFullInformationPDSchema)
async def get_full_information_about_user(
    session: Annotated[AsyncSession, Depends(db_worker.get_session)],
    token: str
) -> UserFullInformationPDSchema:
    """
    Endpoint which return full information about user
    """

    return await UserAPIService.get_full_information_about_user(session=session, token=token)


@user_router.put("/update_user_info",
                 status_code=status.HTTP_202_ACCEPTED,
                 response_model=UserIsUpdated)
async def update_user_info(
    session: Annotated[AsyncSession, Depends(db_worker.get_session)],
    user_info: UpdateUserInfoPDSchema
) -> UserIsUpdated:
    """
    Update user info
    """

    return await UserAPIService.update_user(session=session, user_data=user_info)


@user_router.delete("/delete_user",
                    status_code=status.HTTP_202_ACCEPTED,
                    response_model=UserIsDeletedPDSchema)
async def delete_user(
    session: Annotated[AsyncSession, Depends(db_worker.get_session)],
    token: GetAccessToken
) -> UserIsDeletedPDSchema:
    """
    Delete user
    """
    
    return await UserAPIService.delete_user(session=session, token=token)


@user_router.patch("/update_user_score",
                   status_code=status.HTTP_202_ACCEPTED,
                   response_model=UserIsUpdated)
async def update_user_score(
    session: Annotated[AsyncSession, Depends(db_worker.get_session)],
    user_data: UpdateUserScorePDSchema
) -> UserIsUpdated:
    """
    Update user score
    """

    return await UserAPIService.update_user(
        session=session,
        user_data=user_data,
        flag=True
    )