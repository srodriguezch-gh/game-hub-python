"""PIN-based authentication for game-hub players."""

import re

import bcrypt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import Player


def hash_pin(pin: str) -> str:
    return bcrypt.hashpw(pin.encode(), bcrypt.gensalt()).decode()


def verify_pin(plain_pin: str, hashed_pin: str) -> bool:
    return bcrypt.checkpw(plain_pin.encode(), hashed_pin.encode())


def validate_pin(pin: str) -> tuple[bool, str]:
    if not pin or not isinstance(pin, str):
        return False, "PIN is required"
    if len(pin) != 4 or not re.match(r"^\d{4}$", pin):
        return False, "PIN must be exactly 4 digits"
    return True, ""


async def get_player(session: AsyncSession, name: str) -> Player | None:
    result = await session.execute(select(Player).where(Player.name == name))
    return result.scalar_one_or_none()


async def login_player(session: AsyncSession, name: str, pin: str) -> tuple[bool, str]:
    valid, msg = validate_pin(pin)
    if not valid:
        return False, msg

    player = await get_player(session, name)
    if not player:
        return False, "Player not found"

    if not player.pin:
        player.pin = hash_pin(pin)
        await session.commit()
        return True, "PIN set successfully"

    if verify_pin(pin, player.pin):
        return True, "Logged in"

    return False, "Incorrect PIN"