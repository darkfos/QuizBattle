from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app_settings import db_settings
from db.decl_base import MainBase
from db.models.UserTable import User
from db.models.ReviewTable import Review
from db.models.HistoryTable import History

class DatabaseEngine:
    
    def __init__(self) -> None:
       self.async_engine = create_async_engine(
           url=db_settings.url_db,
           echo=db_settings.echo
       )

       self.async_session = async_sessionmaker(bind=self.async_engine)

    async def get_session(self) -> AsyncSession:
        """
        Return session
        """

        async with self.async_engine.begin() as session:
            return session
        
    async def create_tables(self) -> None:
        """
        Create all tables
        """
        
        MainBase.metadata.create_all(bind=self.async_engine)

db_worker: DatabaseEngine = DatabaseEngine()