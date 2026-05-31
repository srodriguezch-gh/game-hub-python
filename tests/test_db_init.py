import pytest

from core.db_init import DEFAULT_PLAYERS


@pytest.mark.anyio
async def test_default_players_are_minimal():
    assert DEFAULT_PLAYERS == ("Emma", "Mateo", "Dad")
