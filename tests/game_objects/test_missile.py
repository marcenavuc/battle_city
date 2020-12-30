import pytest

from battle_city import Level
from battle_city.game_objects import Missile, Directions
from battle_city.game_objects.blocks import Wall
from battle_city.utils import Vector


@pytest.mark.parametrize("position, direction", [
    (Vector(0, 0), Directions.UP)
])
def test_missile_init(position, direction):
    missile = Missile(position, direction)
    assert True


def test_missile_kill(level):
    missile = Missile(Vector(10, 10), Directions.DOWN)
    level.missiles.append(missile)
    missile.kill(level)
    assert len(level.missiles) == 0


def test_missile_update(level):
    missile = Missile(Vector(10, 10), Directions.DOWN)
    missile.update(None, level)


def test_missile_update_wall(level):
    level.walls = [Wall(Vector(10, 10))]
    health = level.walls[0].health
    level.missiles = [Missile(Vector(10, 10), Directions.DOWN)]
    level.missiles[0].update(None, level)
    assert health != level.walls[0]
