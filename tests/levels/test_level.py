import os
import pytest

from battle_city import Level
from battle_city.game_objects import Missile, Directions
from battle_city.game_objects.blocks import Iron, Wall
from battle_city.game_objects.tanks import EnemyTank
from tests.conftest import is_same_levels


@pytest.mark.parametrize("key, result", [
    ("Some unknown group", None),
    ("IRON", Iron),
    ("TANKS", EnemyTank),
])
def test_level_get_item(level, key, result):
    if level[key] is None:
        assert level[key] is result
    else:
        print(level[key].sprites())
        assert isinstance(level[key].sprites()[0], result)


def test_level_iter(level):
    iter(level)
    assert True


@pytest.fixture()
def fake_file():
    yield "test"
    if os.path.exists("saves/test.txt"):
        os.remove("saves/test.txt")


def test_level_serialize(level, fake_file):
    level.serialize("test")


@pytest.mark.parametrize("json_obj, group_name, result", [
    ({"x": 0, "y": 0}, "IRON", Iron),
    ({"x": 0, "y": 0}, "WALL", Wall),  # Important test
    ({"x": 0, "y": 0, "direction": Directions.UP}, "MISSILE", Missile)
])
def test_level_get_object_from_json(level, json_obj, group_name, result):
    assert isinstance(Level.get_object_from_json(json_obj, group_name), result)


def test_level_unserilize(level, fake_file):
    level.serialize("test")
    serialized_level = Level.unserialize("saves/test.txt")
    is_same_levels(level, serialized_level)
