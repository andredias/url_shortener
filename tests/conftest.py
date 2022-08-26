import os
from collections.abc import AsyncIterable

from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from pytest import fixture

os.environ['ENV'] = 'testing'

from url_shortener.main import app as _app  # noqa: E402
from url_shortener.resources import db  # noqa: E402


@fixture(scope='session')
async def session_app() -> AsyncIterable[FastAPI]:
    """
    Create a FastAPI instance.
    """
    async with LifespanManager(_app):
        yield _app


@fixture
async def app(session_app: FastAPI) -> AsyncIterable[FastAPI]:
    async with db.transaction(force_rollback=True):
        yield session_app


@fixture
async def client(app: FastAPI) -> AsyncIterable[AsyncClient]:
    async with AsyncClient(app=app, base_url='http://testserver') as client:
        yield client
