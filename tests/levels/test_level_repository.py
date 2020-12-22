import pytest

from battle_city.game_objects import Player
from battle_city.game_objects.blocks import Iron, Leaves, Water, Base
from battle_city.game_objects.tanks import Tank
from battle_city.level import LevelsRepository
from battle_city.utils import Vector


@pytest.mark.parametrize("path, result", [
    ("battle_city/media/levels", ['battle_city/media/levels/level3.txt']),
    ("some incorrect path", [])
])
def test_level_repository_init(path, result):
    try:
        levels_repository = LevelsRepository(path)
        assert levels_repository.levels_paths == result
    except Exception as e:
        assert isinstance(e, AssertionError)


@pytest.mark.parametrize("symbol, result", [
    (".", None),
    ("I", Iron),
    ("L", Leaves),
    ("A", Water),
    ("C", Base),
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


@pytest.fixture()
def levels_rep():
    return LevelsRepository("battle_city/media/levels")


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
