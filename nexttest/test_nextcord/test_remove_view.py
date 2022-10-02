from nextcord.ext.commands import Bot
from nextcord.ui import View, Button


async def test_intial(bot: Bot):
    assert not bot._connection._view_store._views


async def test_add(bot: Bot):
    view_one = View(timeout=None)
    view_one.add_item(Button(label="test", custom_id="test"))

    view_two = View(timeout=None)
    view_two.add_item(Button(label="test", custom_id="test"))
    assert not bot._connection._view_store._views

    bot.add_view(view_one)
    assert len(bot._connection._view_store._views) == 1

    bot.add_view(view_two)
    assert len(bot._connection._view_store._views) == 1

    view_three = View(timeout=None)
    view_three.add_item(Button(label="test", custom_id="test_2"))
    bot.add_view(view_three)
    assert len(bot._connection._view_store._views) == 2


async def test_simple_remove(bot: Bot):
    """Tests view removal without a message id"""
    view_one = View(timeout=None)
    view_one.add_item(Button(label="test", custom_id="test"))
    assert not bot._connection._view_store._views

    bot.add_view(view_one)
    assert len(bot._connection._view_store._views) == 1

    bot.remove_view(view_one)
    assert len(bot._connection._view_store._views) == 0


async def test_remove(bot: Bot):
    """Tests view removal without a message id"""
    view_one = View(timeout=None)
    view_one.add_item(Button(label="test", custom_id="test"))

    view_two = View(timeout=None)
    view_two.add_item(Button(label="test", custom_id="test"))
    assert not bot._connection._view_store._views

    bot.add_view(view_one)
    assert len(bot._connection._view_store._views) == 1

    bot.remove_view(view_two)
    assert len(bot._connection._view_store._views) == 0

    bot.add_view(view_two)
    assert len(bot._connection._view_store._views) == 1

    bot.remove_view(view_two)
    assert len(bot._connection._view_store._views) == 0

    view_three = View(timeout=None)
    view_three.add_item(Button(label="test", custom_id="test_2"))
    bot.add_view(view_three)
    assert len(bot._connection._view_store._views) == 1

    bot.remove_view(view_one)
    assert len(bot._connection._view_store._views) == 1
    bot.remove_view(view_two)
    assert len(bot._connection._view_store._views) == 1


async def test_add_with_id(bot: Bot):
    view_one = View(timeout=None)
    view_one.add_item(Button(label="test", custom_id="test"))

    view_two = View(timeout=None)
    view_two.add_item(Button(label="test", custom_id="test"))
    assert not bot._connection._view_store._views

    bot.add_view(view_one, message_id=1)
    assert len(bot._connection._view_store._views) == 1

    bot.add_view(view_two)
    assert len(bot._connection._view_store._views) == 2

    view_three = View(timeout=None)
    view_three.add_item(Button(label="test", custom_id="test_2"))
    bot.add_view(view_three)
    assert len(bot._connection._view_store._views) == 3


async def test_simple_remove_with_id(bot: Bot):
    view_one = View(timeout=None)
    view_one.add_item(Button(label="test", custom_id="test"))
    assert not bot._connection._view_store._views

    bot.add_view(view_one, message_id=1)
    assert len(bot._connection._view_store._views) == 1

    bot.remove_view(view_one)
    assert len(bot._connection._view_store._views) == 1

    bot.remove_view(view_one, message_id=1)
    assert len(bot._connection._view_store._views) == 0


async def test_mismatched_id_removal(bot: Bot):
    view_one = View(timeout=None)
    view_one.add_item(Button(label="test", custom_id="test"))
    assert not bot._connection._view_store._views
    bot.add_view(view_one, message_id=1)
    assert len(bot._connection._view_store._views) == 1
    bot.remove_view(view_one, message_id=2)
    assert len(bot._connection._view_store._views) == 1
    bot.remove_view(view_one, message_id=1)
    assert len(bot._connection._view_store._views) == 0


async def test_remove_with_id(bot: Bot):
    view_one = View(timeout=None)
    view_one.add_item(Button(label="test", custom_id="test"))

    view_two = View(timeout=None)
    view_two.add_item(Button(label="test", custom_id="test"))
    assert not bot._connection._view_store._views

    bot.add_view(view_one, message_id=1)
    assert len(bot._connection._view_store._views) == 1

    bot.remove_view(view_one)
    assert len(bot._connection._view_store._views) == 1
    bot.remove_view(view_two)
    assert len(bot._connection._view_store._views) == 1

    bot.add_view(view_two)
    assert len(bot._connection._view_store._views) == 2

    view_three = View(timeout=None)
    view_three.add_item(Button(label="test", custom_id="test_2"))
    bot.add_view(view_three)
    assert len(bot._connection._view_store._views) == 3
    bot.remove_view(view_three, message_id=2)
    assert len(bot._connection._view_store._views) == 3
    bot.remove_view(view_three)
    assert len(bot._connection._view_store._views) == 2

    # Different to id stored under
    bot.remove_view(view_one, message_id=2)
    assert len(bot._connection._view_store._views) == 2


async def test_different_args(bot: Bot):
    view_one = View(timeout=None)
    view_one.add_item(Button(label="test", custom_id="hello"))

    view_two = View(timeout=None)
    view_two.add_item(Button(label="test", custom_id="world"))

    bot.add_view(view_one)
    assert len(bot._connection._view_store._views) == 1

    bot.remove_view(view_two)
    assert len(bot._connection._view_store._views) == 1
