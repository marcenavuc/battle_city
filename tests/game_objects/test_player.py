import pygame

from battle_city import Level
from battle_city.game_objects import Player
from battle_city.game_objects.bonuses import LifeBonus, SpeedBonus
from battle_city.utils import Vector
from tests.conftest import FakeEvent
import pytest


def test_player_init():
    Player(Vector(0, 0))
    assert True


@pytest.mark.parametrize("event", [
    (FakeEvent(type=pygame.KEYDOWN, key=pygame.K_UP)),
    (FakeEvent(type=pygame.KEYDOWN, key=pygame.K_RIGHT)),
    (FakeEvent(type=pygame.KEYDOWN, key=pygame.K_LEFT)),
    (FakeEvent(type=pygame.KEYDOWN, key=pygame.K_DOWN)),
])
def test_player_on_event(event):
    level = Level(100, 100)
    level.player = Player(Vector(50, 50))
    level.player.update(event, level)
    assert 0 != level.player.rect.x or 0 != level.player.rect.y


@pytest.mark.parametrize("bonus", [
    LifeBonus, SpeedBonus
])
def test_player_take_bonus(bonus):
    level = Level(100, 100)
    level.player = Player(Vector(50, 50))
    health, speed, = level.player.health, level.player.speed
    level.bonuses = [bonus(Vector(50, 50))]
    level.bonuses[0].update(None, level)
    assert health != level.player.health or speed != level.player.speed
