from fastapi import APIRouter, status, Depends
from api.db.db_engine import db_worker
from api.backend.exceptions.history_exception import *
from api.backend.schemas.HistoryPDSchema import *
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