import pytest
from disnake.ext import commands


class Cog(commands.Cog):
    @commands.command()
    async def my_cmd(self, ctx):
        pass


class CogTwo(commands.Cog):
    async def bot_check(self, ctx) -> bool:
        pass


class CogThree(commands.Cog):
    async def bot_check_once(self, ctx) -> bool:
        pass


def test_commands_bot():
    bot = commands.Bot(command_prefix="?")
    bot.add_cog(Cog())
    bot.add_cog(CogTwo())
    bot.add_cog(CogThree())


def test_auto_sharded_bot():
    bot = commands.AutoShardedBot(command_prefix="?")
    bot.add_cog(Cog())
    bot.add_cog(CogTwo())
    bot.add_cog(CogThree())


def test_inter_bot():
    bot = commands.InteractionBot()
    with pytest.raises(TypeError):
        bot.add_cog(Cog())

    with pytest.raises(TypeError):
        bot.add_cog(CogTwo())

    with pytest.raises(TypeError):
        bot.add_cog(CogThree())


def test_auto_inter_bot():
    bot = commands.AutoShardedInteractionBot()
    with pytest.raises(TypeError):
        bot.add_cog(Cog())

    with pytest.raises(TypeError):
        bot.add_cog(CogTwo())

    with pytest.raises(TypeError):
        bot.add_cog(CogThree())
