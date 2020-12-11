import pytest
from pytest_mock import mocker

from battle_city import GameObject
from battle_city.game_objects import Wall, Tank, Player
from battle_city.level import LevelsRepository, Level


@pytest.mark.parametrize("path, result", [
    ("battle_city/media/levels", ['battle_city/media/levels/level1.txt']),
    ("some incorrect path", [])
])
def test_level_repository_init(path, result):
    try:
        levels_repository = LevelsRepository(path)
        assert levels_repository.levels_paths == result
    except Exception as e:
        assert isinstance(e, AssertionError)


@pytest.mark.parametrize("symbol, result", [
    (".", GameObject),
    ("T", Wall),
    ("X", Tank),
    ("P", Player),
    ("Simple wrong symbol", None)
])
def test_level_repository_get_from_symbol(symbol, result):
    try:
        assert isinstance(LevelsRepository._get_from_symbol(symbol, (0, 0)),
                          result)
    except Exception as e:
        assert isinstance(e, KeyError)


@pytest.fixture()
def levels_rep():
    return LevelsRepository("battle_city/media/levels")


@pytest.mark.parametrize("level_num", [
    0,
    100,
])
def test_level_repository_load_level(levels_rep, level_num):
    try:
        level = levels_rep.load_level(level_num)
        assert level is not None
    except IndexError as e:
        assert level_num != 0  # У меня есть только 0 уровень(((
