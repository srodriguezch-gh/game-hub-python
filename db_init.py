"""Initialize game-hub database with schema and default players."""

import asyncio
import logging

from sqlalchemy import text

from core.config import get_settings
from core.db import Base, engine, async_session, Player

logger = logging.getLogger(__name__)

DEFAULT_PLAYERS = ["Dad", "Emma", "Mateo", "Calypso", "Traka"]


async def init_schema():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database schema created")


async def init_players():
    async with async_session() as session:
        for name in DEFAULT_PLAYERS:
            result = await session.execute(
                text("SELECT 1 FROM players WHERE name = :name"),
                {"name": name}
            )
            if not result.fetchone():
                session.add(Player(name=name, game_wins={}))
                logger.info(f"Created player: {name}")
        await session.commit()


async def init_tasks_schema():
    async with async_session() as session:
        columns_to_add = [
            ("is_approved", "BOOLEAN DEFAULT FALSE"),
            ("is_paid", "BOOLEAN DEFAULT FALSE"),
            ("is_recurring", "BOOLEAN DEFAULT FALSE"),
            ("series_total", "INTEGER DEFAULT 1"),
            ("series_count", "INTEGER DEFAULT 0"),
            ("last_increment_at", "TIMESTAMP"),
        ]
        for col_name, col_def in columns_to_add:
            try:
                await session.execute(
                    text(f"ALTER TABLE tasks ADD COLUMN IF NOT EXISTS {col_name} {col_def}")
                )
            except Exception:
                pass
        await session.commit()


async def main():
    logging.basicConfig(level=logging.INFO)
    settings = get_settings()
    logger.info(f"Initializing game-hub database at {settings.DB_HOST}")
    await init_schema()
    await init_players()
    await init_tasks_schema()
    logger.info("Database initialization complete")


if __name__ == "__main__":
    asyncio.run(main())