import shutil
import sys
from os.path import join, dirname
from pathlib import Path

import pytest
from nextcord.ext.commands import (
    Bot,
    BadArgument,
    ExtensionFailed,
)

CogLike = str  # String format of cog


def build_cog_dir_with_cogs():
    # Funkiness purely because tests live in weird places
    sys.path.insert(0, join(dirname(__file__)))
    initial_path = join(
        dirname(__file__),
        "cog",
    )
    valid_cog = Path(join(initial_path, "valid.py"))
    valid_cog.parent.mkdir(exist_ok=True, parents=True)
    with valid_cog.open("w", encoding="utf-8") as f:
        f.write(
            "from nextcord.ext import commands\nclass Valid(commands.Cog):\n"
            "    def __init__(self, bot):\n        self.bot=bot\n"
            "def setup(bot):\n    bot.add_cog(Valid(bot))"
        )

    valid_cog = Path(join(initial_path, "valid_two.py"))
    valid_cog.parent.mkdir(exist_ok=True, parents=True)
    with valid_cog.open("w", encoding="utf-8") as f:
        f.write(
            "from nextcord.ext import commands\nclass ValidTwo(commands.Cog):\n"
            "    ..."
            "def setup(bot):\n    bot.add_cog(ValidTwo())"
        )

    invalid_cog = Path(join(initial_path, "invalid_init_args.py"))
    invalid_cog.parent.mkdir(exist_ok=True, parents=True)
    with invalid_cog.open("w", encoding="utf-8") as f:
        f.write(
            "from nextcord.ext import commands\nclass InvalidArgs(commands.Cog):\n"
            "    def __init__(self):\n        self.bot=bot\n"
            "def setup(bot):\n    bot.add_cog(InvalidArgs(bot))"
        )

    invalid_cog = Path(join(initial_path, "no_setup.py"))
    invalid_cog.parent.mkdir(exist_ok=True, parents=True)
    with invalid_cog.open("w", encoding="utf-8") as f:
        f.write(
            "from nextcord.ext import commands\nclass NoSetup(commands.Cog):\n"
            "    def __init__(self):\n        self.bot=bot"
        )


def teardown_cogs():
    initial_path = join(
        dirname(__file__),
        "cog",
    )
    path = Path(initial_path)
    shutil.rmtree(path)


async def test_one_cog(bot: Bot):
    build_cog_dir_with_cogs()
    # ---
    loaded = bot.load_extensions(["cog.valid"])
    assert loaded == ["cog.valid"]

    # ---
    teardown_cogs()


async def test_not_found(capsys, bot: Bot):
    build_cog_dir_with_cogs()

    loaded = bot.load_extensions(["cog.invalid"])
    assert len(loaded) == 0

    captured = capsys.readouterr()
    assert "ExtensionNotFound" in captured.err

    teardown_cogs()


async def test_invalid_setup(capsys, bot: Bot):
    build_cog_dir_with_cogs()
    loaded = bot.load_extensions(["cog.no_setup"])
    assert len(loaded) == 0

    captured = capsys.readouterr()
    assert "NoEntryPointError" in captured.err
    teardown_cogs()


async def test_invalid_args(capsys, bot: Bot):
    build_cog_dir_with_cogs()
    loaded = bot.load_extensions(["cog.invalid_init_args"])
    assert len(loaded) == 0

    captured = capsys.readouterr()
    assert "ExtensionFailed" in captured.err
    teardown_cogs()


async def test_method_args(bot: Bot):
    with pytest.raises(ValueError):
        bot.load_extensions(list(range(5)), packages=[str(i) for i in range(10)])

    with pytest.raises(ValueError):
        bot.load_extensions(list(range(5)), extras=[{}, {}])

    with pytest.raises(ValueError):
        bot.load_extensions(
            ["1.2"], extras=[{}, {}], packages=[str(i) for i in range(3)]
        )

    with pytest.raises(BadArgument):
        bot.load_extensions([""], package="hi", packages=["again"])


async def test_finder(bot: Bot):
    build_cog_dir_with_cogs()

    with pytest.raises(ValueError):
        bot.load_extensions_from_module("dsadwa")

    loaded = bot.load_extensions_from_module("cog")
    assert len(loaded) == 1
    assert loaded == ["cog.valid"]

    teardown_cogs()


async def test_finder_ignore(bot: Bot):
    build_cog_dir_with_cogs()

    loaded = bot.load_extensions_from_module("cog", ignore=["valid"])
    assert len(loaded) == 1
    assert loaded == ["cog.valid"]

    loaded_2 = bot.load_extensions_from_module("cog", ignore=["valid.py"])
    assert len(loaded_2) == 0

    teardown_cogs()


async def test_raise_on_error(bot: Bot):
    build_cog_dir_with_cogs()

    with pytest.raises(ExtensionFailed):
        bot.load_extensions(["cog.invalid_init_args"], stop_at_error=True)

    with pytest.raises(ExtensionFailed):
        bot.load_extensions_from_module("cog", stop_at_error=True)

    loaded = bot.load_extensions_from_module("cog")
    assert len(loaded) == 1

    teardown_cogs()
