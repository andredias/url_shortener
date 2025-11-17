from loguru import logger
from sqlalchemy import Column, DateTime, Index, Integer, String, Table
from sqlalchemy.sql import Select, func

from ..resources import db
from ..schemas.link import LinkInfo
from . import metadata

Link = Table(
    'link',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('url', String, nullable=False),
    Column(
        'created_at', DateTime, server_default=func.now()
    ),  # see: https://stackoverflow.com/a/33532154/266362
    Index('link_url', 'url', postgresql_using='hash'),
)


async def _get(query: Select) -> LinkInfo | None:
    logger.debug(query)
    result = await db.fetch_one(query)
    return LinkInfo(**result) if result else None  # type: ignore


async def get_by_url(url: str) -> LinkInfo | None:
    logger.debug(url)
    query = Link.select().where(Link.c.url == url)
    return await _get(query)


async def get(id_: int) -> LinkInfo | None:
    query = Link.select().where(Link.c.id == id_)
    return await _get(query)


async def insert(url: str) -> int:
    stmt = Link.insert().values(url=url)
    logger.debug(stmt)
    return await db.execute(stmt)
