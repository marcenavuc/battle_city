import pytest
from pytest_mock import mocker

from battle_city import GameObject
from battle_city.utils import Vector


@pytest.mark.parametrize("position, result", [
    (Vector(0, 1), True),
    (Vector(-100, -100), False)
])
def test_game_object_in_borders(level, position, result):
    assert GameObject.in_borders(position, level) is result
