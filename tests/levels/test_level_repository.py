import pytest

from battle_city.game_objects import Player
from battle_city.game_objects.blocks import Iron, GreenBrush, Aqua, Center
from battle_city.game_objects.tanks import Tank
from battle_city.level import LevelsRepository
from battle_city.utils import Vector


@pytest.mark.parametrize("symbol, result", [
    (".", None),
    ("I", Iron),
    ("G", GreenBrush),
    ("A", Aqua),
    ("C", Center),
    ("T", Tank),
    ("P", Player),
    ("Simple wrong symbol", None)
])
def test_level_repository_get_from_symbol(symbol, result):
    obj = LevelsRepository._get_from_symbol(symbol, Vector(0, 0))
    if obj is None:
        assert obj is result
    elif isinstance(obj, list):
        assert obj[0] is result
    else:
        assert isinstance(obj, result)


@pytest.mark.parametrize("level_num", [
    0,
    1,
    2,
    100,
])
def test_level_repository_load_level(levels_rep, level_num):
    try:
        level = levels_rep.load_level(level_num)
        assert level is not None
    except IndexError as e:
        assert level_num != 0


def test_level_serialize():
    LevelsRepository().save_level()


# def test_level_unserilize(level, fake_file):
#     level.save_level("test")
#     serialized_level = Level.unserialize("saves/test.txt")
#     is_same_levels(level, serialized_level)