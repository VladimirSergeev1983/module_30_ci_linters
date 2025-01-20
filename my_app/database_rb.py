from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./my_app/recipe_book.db"

engine = create_async_engine(DATABASE_URL, echo=True)

a_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
session = a_session()
Base = declarative_base()
