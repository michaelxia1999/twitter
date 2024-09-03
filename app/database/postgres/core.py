from app.database.postgres.orm import ORM
from app.settings import POSTGRES_URL
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

engine = create_async_engine(url=POSTGRES_URL, echo=True)
SessionLocal = async_sessionmaker(bind=engine)


async def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        await db.rollback()
        raise
    finally:
        await db.commit()
        await db.close()


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(ORM.metadata.create_all)


async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(ORM.metadata.drop_all)
