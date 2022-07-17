import pytest
from nextcord.ext.commands import GroupMixin, Group


async def test_load_known_gm():
    gm: GroupMixin = GroupMixin(
        case_insensitive=True,
        # Forward ref to Group init should just work
        invoke_without_command=True,
    )
    assert gm.case_insensitive is True

    gm_2: GroupMixin = GroupMixin(
        case_insensitive=True,
    )
    assert gm_2.case_insensitive is True

    gm_3: GroupMixin = GroupMixin()
    assert gm_3.case_insensitive is False


async def test_group_mixin_back_ref():
    """Tests changes propagate back up to GroupMixin"""
    with pytest.raises(TypeError):
        Group(
            case_insensitive=True,
            invoke_without_command=True,
        )

    with pytest.raises(TypeError):
        Group(
            func=lambda: True,
            case_insensitive=True,
            invoke_without_command=True,
        )

    async def func():
        ...

    g: Group = Group(
        func=func,
        case_insensitive=True,
        invoke_without_command=True,
    )
    assert g.case_insensitive is True
    assert g.invoke_without_command is True

    assert g.name == "func"
    assert g.callback is func


async def test_inheritance():
    """Tests changes propagate back up to Command"""

    async def func():
        ...

    g: Group = Group(func=func, extras={"hello": "world"})
    assert g.extras == {"hello": "world"}
    assert g.qualified_name == "func"  # Tests a property instead of attr
