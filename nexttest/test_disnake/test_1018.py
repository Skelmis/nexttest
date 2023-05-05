import pytest
from disnake.ext import commands


class Cog(commands.Cog):
    @commands.command()
    async def my_cmd(self, ctx):
        pass


def test_commands_bot():
    bot = commands.Bot(command_prefix="?")
    bot.add_cog(Cog())


def test_auto_sharded_bot():
    bot = commands.AutoShardedBot(command_prefix="?")
    bot.add_cog(Cog())


def test_inter_bot():
    bot = commands.InteractionBot()
    with pytest.raises(TypeError):
        bot.add_cog(Cog())


def test_auto_inter_bot():
    bot = commands.AutoShardedInteractionBot()
    with pytest.raises(TypeError):
        bot.add_cog(Cog())
