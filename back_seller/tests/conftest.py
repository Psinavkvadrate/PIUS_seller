import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest
import asyncio
import uuid
from httpx import AsyncClient
from jose import jwt

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Enum as SAEnum, String

# -------------------------------------------------------------------
# 0. ПАТЧИМ ВСЕ ENUM КЛАССЫ ДО ЛЮБОГО ИМПОРТА app.*
# -------------------------------------------------------------------

import app.models as models_module

def patch_enum_classes():
    """
    Заменяем SQLAlchemy Enum(...) на обычный String() ВО ВСЕХ моделях
    до того, как создаются engine и запросы.
    """
    for name in dir(models_module):
        attr = getattr(models_module, name)

        # ищем классы SQLAlchemy моделей
        if hasattr(attr, "__table__"):
            table = attr.__table__
            for column in table.columns:
                if isinstance(column.type, SAEnum):
                    column.type = String()  # ← критично
patch_enum_classes()


# -------------------------------------------------------------------
# 1. ТЕПЕРЬ МОЖНО ИМПОРТИРОВАТЬ ПРОЕКТ
# -------------------------------------------------------------------

import app.database.session as session_module
from app.main import app
from app.database.base import Base
from app.database.session import get_db
from app.security.jwt_dependency import SECRET_KEY, ALGORITHM


TEST_DB = "sqlite+aiosqlite://"


# -------------------------------------------------------------------
# 2. ПАТЧИМ ENGINE ДО СОЗДАНИЯ ЛЮБЫХ СЕССИЙ
# -------------------------------------------------------------------

@pytest.fixture(scope="session", autouse=True)
def patch_engine():
    """
    Полностью заменяет движок проекта на SQLite ДО загрузки приложения.
    """
    engine = create_async_engine(TEST_DB, future=True)

    # Переписываем engine проекта
    session_module.engine = engine
    session_module.async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    return engine


# -------------------------------------------------------------------
# 3. event loop
# -------------------------------------------------------------------

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop


# -------------------------------------------------------------------
# 4. test_db
# -------------------------------------------------------------------

@pytest.fixture
async def test_db(patch_engine):
    engine = patch_engine

    # создаём таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    TestSession = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    yield TestSession

    # удаляем таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# -------------------------------------------------------------------
# 5. Test client
# -------------------------------------------------------------------

@pytest.fixture
async def client(test_db):

    async def override_db():
        async with test_db() as session:
            yield session

    app.dependency_overrides[get_db] = override_db

    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c


# -------------------------------------------------------------------
# 6. JWT tokens
# -------------------------------------------------------------------

@pytest.fixture
def seller_token():
    return jwt.encode(
        {"userId": str(uuid.uuid4()), "isSeller": True},
        SECRET_KEY,
        algorithm=ALGORITHM
    )

@pytest.fixture
def non_seller_token():
    return jwt.encode(
        {"userId": str(uuid.uuid4()), "isSeller": False},
        SECRET_KEY,
        algorithm=ALGORITHM
    )

@pytest.fixture
def bad_token():
    return "invalid.token"