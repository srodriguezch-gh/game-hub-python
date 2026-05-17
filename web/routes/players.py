"""Player management routes."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import login_player
from core.db import Player, get_session

router = APIRouter(prefix="/api", tags=["players"])


class LoginRequest(BaseModel):
    name: str
    pin: str


class ResetPinRequest(BaseModel):
    name: str


@router.get("/players")
async def get_players(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Player))
    players = {}
    for p in result.scalars().all():
        game_wins = p.game_wins if isinstance(p.game_wins, dict) else {}
        players[p.name] = {
            "name": p.name,
            "wins": p.wins,
            "losses": p.losses,
            "gameWins": game_wins,
            "selfie": p.selfie,
            "hasPin": bool(p.pin),
        }
    return players


@router.post("/login")
async def login(data: LoginRequest, session: AsyncSession = Depends(get_session)):
    success, message = await login_player(session, data.name, data.pin)
    if success:
        return {"success": True, "message": message}
    raise HTTPException(status_code=401 if "Incorrect" in message else 400, detail=message)


@router.post("/api/admin/reset-pin")
async def reset_pin(data: ResetPinRequest, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Player).where(Player.name == data.name))
    player = result.scalar_one_or_none()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    player.pin = None
    await session.commit()
    return {"success": True, "message": f"PIN reset for {data.name}"}