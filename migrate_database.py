import asyncio
from pathlib import Path
from subprocess import run

from url_shortener import config
from url_shortener.resources import Database, connect_database

parent_path = Path(__file__).parent


async def migrate() -> None:
    """
    Wait for the database to be ready.
    """
    db = Database(config.DATABASE_URL)
    await connect_database(db)
    await db.disconnect()
    run('alembic upgrade head'.split(), cwd=parent_path)


if __name__ == '__main__':
    asyncio.run(migrate())
