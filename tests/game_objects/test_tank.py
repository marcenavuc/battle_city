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
    tank = level["TANKS"].sprites()[0]
    new_position = tank.move(direction)
    assert new_position.x == tank.rect.x + delta_x
    assert new_position.y == tank.rect.y + delta_y


@pytest.mark.parametrize("before_map, after_map", [
    (["T", "W"], ["T", "."]),
    (["T", ".", "W"], ["T", ".", "."]),
    (["T", ".", "W", "W"], ["T", ".", ".", "."])
])
def test_shot(before_map, after_map):
    level_before = Level(*LevelsRepository._parse_to_map(before_map))
    tank = level_before["TANKS"].sprites()[0]

    for i in range(10):
        tank.shot(level_before)

    level_after = Level(*LevelsRepository._parse_to_map(after_map))
    assert not is_same_levels(level_before, level_after)


@pytest.mark.parametrize("map, key", [
    (["T", ".", ".", "P"], "PLAYER"),
])
def test_move_to_obj(map, key):
    level = Level(*LevelsRepository._parse_to_map(map))
    tank = level["TANKS"].sprites()[0]
    old_x, old_y = tank.rect.x, tank.rect.y
    tank.move_to_obj("PLAYER", level)
    assert old_x != tank.rect.x or old_y != tank.rect.y


def test_random_move(level):
    tank = level["TANKS"].sprites()[0]
    old_x, old_y = tank.rect.x, tank.rect.y
    tank.random_walk(level)
    assert old_x != tank.rect.x or old_y != tank.rect.y
