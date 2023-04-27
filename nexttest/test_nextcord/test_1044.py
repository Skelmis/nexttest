import nextcord
from nextcord import SlashApplicationSubcommand, ApplicationCommandOptionType
from nextcord.ext import commands


class ValidCog(commands.Cog):
    @nextcord.slash_command()
    async def valid(self, interaction):
        ...

    @valid.subcommand()
    async def two(self, inter):
        ...


async def test_cog_decor(bot: commands.Bot):
    bot.add_cog(ValidCog())


async def test_decor(bot: commands.Bot):
    @nextcord.slash_command()
    async def top_level(inter):
        ...

    @top_level.subcommand()
    async def down(inter):
        ...

    @top_level.subcommand(name="test", description="bighger test")
    async def down_two(inter):
        ...

    @down.subcommand()
    async def more_nesting(inter):
        ...


async def test_raw():
    SlashApplicationSubcommand(cmd_type=ApplicationCommandOptionType.sub_command_group)
    SlashApplicationSubcommand(cmd_type=ApplicationCommandOptionType.sub_command)
