import nextcord
import pytest
from nextcord.ext import commands


class ValidCog(commands.Cog):
    @nextcord.slash_command()
    async def valid(self, interaction):
        ...

    @nextcord.slash_command()
    async def valid_arg(self, interaction, user_input: str):
        ...

    @nextcord.slash_command()
    async def valid_typehint(self, interaction: nextcord.Interaction):
        ...

    @nextcord.slash_command()
    async def valid_typehint_arg(
        self, interaction: nextcord.Interaction, user_input: str
    ):
        ...


async def test_loader(bot: commands.Bot):
    bot.add_cog(ValidCog())


class MissingSelf(commands.Cog):
    @nextcord.slash_command()
    async def invalid_one_arg(interaction):
        ...


async def test_invalid_self_load(bot: commands.Bot):
    with pytest.raises(ValueError):
        bot.add_cog(MissingSelf())


class MissingInteraction(commands.Cog):
    @nextcord.slash_command()
    async def invalid_one_arg(self):
        ...


async def test_invalid_interaction_load(bot: commands.Bot):
    with pytest.raises(ValueError):
        bot.add_cog(MissingInteraction())


class NoArgs(commands.Cog):
    @nextcord.slash_command()
    async def invalid_no_args():
        ...


async def test_no_args(bot: commands.Bot):
    with pytest.raises(ValueError):
        bot.add_cog(NoArgs())


class MissingInter(commands.Cog):
    @nextcord.slash_command()
    async def invalid_inter(self, user_input: str):
        ...


async def test_missing_inter_with_args(bot: commands.Bot):
    with pytest.raises(ValueError):
        bot.add_cog(MissingInter())


class MissingSelfArgs(commands.Cog):
    @nextcord.slash_command()
    async def invalid_inter(interaction: nextcord.Interaction, user_input: str):
        ...


async def test_missing_self_with_args(bot: commands.Bot):
    with pytest.raises(ValueError):
        bot.add_cog(MissingSelfArgs())


class CustomInteraction(nextcord.Interaction):
    """For the power users"""

    @property
    def mock_custom_obj(self) -> bool:
        return True


class CustomInterCog(commands.Cog):
    @nextcord.slash_command()
    async def i_am_valid(self, interaction: CustomInteraction, user_input: str):
        ...


async def test_custom_inter(bot: commands.Bot):
    bot.add_cog(CustomInterCog())
