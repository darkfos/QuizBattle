from api.db.db_engine import db_worker
import asyncio


asyncio.run(db_worker.create_tables())