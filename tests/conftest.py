import pytest
import pygame

from battle_city import GameObject, Level
from battle_city.level import LevelsRepository
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


@pytest.fixture()
def hard_level():
    lines = [
        "...",
        ".X.",
        "...",
    ]
    return Level(LevelsRepository._parse_to_map(lines))


def is_same_levels(level1, level2):
    if level1.game_env.keys() != level2.game_env.keys():
        return False

    for key in level1.game_env:
        if type(level1[key]) != type(level2[key]):
            print(key)
            print(type(level1[key]), type(level2[key]))
            return False

    return True
