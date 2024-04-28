from fastapi import APIRouter, status, Depends
from api.db.db_engine import db_worker
from api.backend.exceptions.history_exception import *
from api.backend.schemas.HistoryPDSchema import *
from api.backend.schemas.TokenPDSchema import *
from api.backend.services.HistoryService import HistoryAPIService
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List


history_router: APIRouter = APIRouter(
    prefix="/history",
    tags=["History"]
)


@history_router.post("/create_history",
                     status_code=status.HTTP_201_CREATED,
                     response_model=HistoryIsCreatedPDSchema)
async def add_new_history(
    session: Annotated[AsyncSession, Depends(db_worker.get_session)],
    new_history: AddNewHistoryPDSchema
) -> HistoryIsCreatedPDSchema:
    """
    Create a new history
    """

    return await HistoryAPIService.add_a_new_history(session=session, new_history=new_history)


@history_router.get("/get_history",
                    status_code=status.HTTP_200_OK,
                    response_model=GetHistoryPDSchema)
async def get_history_by_id(
    session: Annotated[AsyncSession, Depends(db_worker.get_session)],
    history_id: int
) -> GetHistoryPDSchema:
    """
    Return information about history
    """

    return await HistoryAPIService.get_history_by_id(session=session, id=history_id)


@history_router.get("/all_histories",
                    status_code=status.HTTP_200_OK,
                    response_model=Union[List, List[GetHistoryPDSchema]])
async def get_all_history(session: Annotated[AsyncSession, Depends(db_worker.get_session)], token: str) -> Union[List, List[GetHistoryPDSchema]]:
    """
    Return all histories user
    """

    return await HistoryAPIService.get_all_history_for_user(session=session, token=token)


@history_router.delete("/delete_history",
                       status_code=status.HTTP_202_ACCEPTED,
                       response_model=HistoryIsDeletedPDSchema)
async def del_history(
    session: Annotated[AsyncSession, Depends(db_worker.get_session)],
    history_id: int
) -> HistoryIsDeletedPDSchema:
    """
    Return result operation - delete
    """

    return await HistoryAPIService.delete_history(session=session, history_id=history_id)