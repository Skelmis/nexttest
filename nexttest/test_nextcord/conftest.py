import pytest
from nextcord.ext import commands


@pytest.fixture
def bot() -> commands.Bot:
    return commands.Bot()
