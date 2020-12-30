import pytest

from battle_city import Level
from battle_city.game_objects import Directions
from battle_city.level import LevelsRepository
from tests.conftest import is_same_levels


@pytest.mark.parametrize("direction, delta_x, delta_y", [
    (Directions.UP, 0, -5),
    (Directions.DOWN, 0, 5),
    (Directions.LEFT, -5, 0),
    (Directions.RIGHT, 5, 0)
])
def test_moving(level, direction, delta_x, delta_y):
    tank = level.tanks[0]
    new_position = tank.move(direction)
    assert new_position.x == tank.rect.x + delta_x
    assert new_position.y == tank.rect.y + delta_y


@pytest.mark.parametrize("before_map, after_map, is_same", [
    (["E", "W", "I", "P", "C"], ["T", ".", "I", "P", "C"], False),
    (["E", ".", "W", "I", "P", "C"], ["T", ".", ".", "I", "P", "C"], False),
    (["E", ".", "W", "W", "I", "P", "C"],
     ["T", ".", ".", ".", "I", "P", "C"], False),
    (["E", ".", "I", "P", "C"], ["T", ".", "I", "P", "C"], True),
    (["E", "A", "I", "P", "C"], ["T", "A", "I", "P", "C"], True),
    (["E", "G", "I", "P", "C"], ["T", "G", "I", "P", "C"], True),
    (["E", "F", "I", "P", "C"], ["T", "F", "I", "P", "C"], True),
])
def test_shot(before_map, after_map, is_same):
    level_before = LevelsRepository._parse_level(before_map)
    tank = level_before.tanks[0]

    for i in range(10):
        tank.shot(level_before)

    level_after = LevelsRepository._parse_level(after_map)
    assert is_same_levels(level_before, level_after) is is_same


def test_move_to_obj(level):
    tank = level.tanks[0]
    old_x, old_y = tank.rect.x, tank.rect.y
    tank.move_to_obj(level.player, level)
    assert old_x != tank.rect.x or old_y != tank.rect.y


def test_random_move(level):
    tank = level.tanks[0]
    old_x, old_y = tank.rect.x, tank.rect.y
    tank.random_walk(level)
    assert old_x != tank.rect.x or old_y != tank.rect.y
