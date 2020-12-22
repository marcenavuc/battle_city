import pytest

from battle_city.game_objects.blocks import Walls, Iron
from battle_city.game_objects.bonuses import HealthBonus, SpeedBonus
from battle_city.level import CharMapEnum


@pytest.mark.parametrize("symbol, result", [
    ("W", Walls),
    ("B", HealthBonus),
    ("I", Iron),
    ("V", SpeedBonus)
])
def test_get_from_symbol(symbol, result):
    assert CharMapEnum.get_from_symbol(symbol) is result


@pytest.mark.parametrize("symbol, result", [
    ("W", "WALL"),
    ("B", "BONUS"),
    ("I", "IRON"),
    ("V", "VELOCITYBONUS")
])
def test_find_name_by_symbol(symbol, result):
    assert CharMapEnum.find_name_by_symbol(symbol) == result
