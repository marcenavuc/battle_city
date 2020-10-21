import pytest
from pytest_mock import mocker

from battle_city import Level, GameObject
from battle_city.game_objects import Tank, Wall


@pytest.mark.parametrize("game_map, max_x, max_y", [
    ({(0, 0): GameObject((0, 0))}, 0, 0),
    ({(0, 100): GameObject((0, 100)),
      (100, 0): GameObject((100, 0))}, 100, 100),
])
def test_level_init(game_map, max_x, max_y):
    level = Level(game_map)
    assert level.max_x == max_x
    assert level.max_y == max_y


@pytest.mark.parametrize("key, result", [
    ((100, 100), None)
])
def test_level_get_item(simple_level, key, result):
    assert simple_level[key] is result


@pytest.mark.parametrize("key, result", [
    ((0, 0), GameObject((0, 0))),
    ((100, 100), Tank((100, 100)))
])
def test_level_set_item(simple_level, key, result):
    simple_level[key] = result


@pytest.mark.parametrize("position, result", [
    ((0, 0), GameObject),
    ((50, 50), None)
])
def test_level_remove(simple_level, position, result):
    simple_level.remove(position)
    if result:
        assert isinstance(simple_level[position], result)
    else:
        assert simple_level[position] is result


@pytest.mark.parametrize("position, new_position, game_obj", [
    ((0, 0), (0, 1), Wall),
])
def test_level_update(simple_level, position, new_position, game_obj):
    simple_level[position] = game_obj(new_position)
    simple_level.update()
    assert isinstance(simple_level[position], GameObject) \
            and isinstance(simple_level[new_position], game_obj) \
            and simple_level[new_position].position == new_position
