import pytest
from pytest_mock import mocker

from battle_city import Level, GameObject
from battle_city.game_objects import Tank, Wall
from battle_city.level import LevelsRepository
from tests.conftest import is_same_levels


def test_moving(hard_level):
    tank_position = 1, 1
    tank = hard_level[tank_position]

    assert tank.go_forward() == (1, 2)
    assert tank.go_back() == (1, 0)

    tank.go_left()

    assert tank.go_forward() == (2, 1)
    assert tank.go_back() == (0, 1)

    tank.go_right()
    tank.go_right()

    assert tank.go_forward() == (0, 1)
    assert tank.go_back() == (2, 1)


@pytest.mark.parametrize("before_map, after_map, tank_pos", [
    (["X", "T"], ["X", "T"], (0, 0)),
    (["X", ".", "T"], ["X", ".", "."], (0, 0)),
    (["X", ".", "T", "T"], ["X", ".", ".", "T"], (0, 0))
])
def test_shot(before_map, after_map, tank_pos):
    level_before = Level(LevelsRepository._parse_to_map(before_map))
    tank = level_before[tank_pos]
    tank.shot(level_before)

    for i in range(10):
        for pos in level_before:
            level_before[pos].on_event(None, level_before)

        level_before.update()

    level_after = Level(LevelsRepository._parse_to_map(after_map))
    assert is_same_levels(level_before, level_after)
