from nextcord.ext.commands import Bot
from nextcord.ui import Modal, TextInput


async def test_initial(bot: Bot):
    assert not bot._connection._modal_store._modals


async def test_add(bot: Bot):
    modal_one = Modal(title="one", custom_id="one", timeout=None)
    modal_two = Modal(title="two", custom_id="one", timeout=None)
    assert not bot._connection._modal_store._modals

    bot.add_modal(modal_one)
    assert len(bot._connection._modal_store._modals) == 1

    bot.add_modal(modal_two)
    assert len(bot._connection._modal_store._modals) == 1

    modal_three = Modal(title="three", custom_id="three")
    bot.add_modal(modal_three)
    assert len(bot._connection._modal_store._modals) == 2


async def test_simple_remove(bot: Bot):
    """Tests modal removal without a message id"""
    modal_one = Modal(timeout=None, title="Test", custom_id="test")
    modal_one.add_item(TextInput("label", custom_id="modal_one_label"))
    assert not bot._connection._modal_store._modals

    bot.add_modal(modal_one)
    assert len(bot._connection._modal_store._modals) == 1

    bot.remove_modal(modal_one)
    assert len(bot._connection._modal_store._modals) == 0


async def test_with_user_id(bot: Bot):
    modal_one = Modal(timeout=None, title="Test", custom_id="test")
    modal_one.add_item(TextInput("label", custom_id="modal_one_label"))
    assert not bot._connection._modal_store._modals

    bot.add_modal(modal_one, user_id=12345)
    assert len(bot._connection._modal_store._modals) == 1

    bot.remove_modal(modal_one)
    assert len(bot._connection._modal_store._modals) == 0
