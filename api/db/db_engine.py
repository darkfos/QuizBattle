from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app_settings import db_settings


class DatabaseEngine:
    
    def __init__(self) -> None:
       self.async_engine = create_async_engine(
           url=db_settings.url_db,
           echo=db_settings.echo
       )

       self.async_session = async_sessionmaker(bind=self.async_engine)

    async def get_session(self):
        """
        Return session
        """

        async with self.async_engine.begin() as session:
            yield session
        await session.close()


db_worker: DatabaseEngine = DatabaseEngine()