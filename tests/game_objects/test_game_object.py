import pytest
from pytest_mock import mocker

from battle_city import Level, GameObject
from battle_city.game_objects import Tank, Wall


@pytest.mark.parametrize("position, result", [
    ((0, 1), True),
    ((-100, -100), False)
])
def test_game_object_in_borders(simple_level, position, result):
    assert GameObject.in_borders(position, simple_level) is result
