import pytest
import pygame

from battle_city import GameObject, Level
from battle_city.game_objects import Tank


@pytest.fixture(scope="session")
def set_pygame():
    pygame.init()


@pytest.fixture()
def simple_level():
    game_map = {
        (0, 0): GameObject((0, 0)),
        (1, 0): GameObject((1, 0)),
        (0, 1): GameObject((0, 1)),
        (1, 1): Tank((1, 1)),
    }
    return Level(game_map)
