import pytest
import pygame

from battle_city import Level
from battle_city.level import LevelsRepository


@pytest.fixture(scope="session")
def set_pygame():
    pygame.init()


@pytest.fixture()
def levels_rep():
    return LevelsRepository()


@pytest.fixture()
def level():
    lines = [
        "...P",
        ".T.C",
        "....",
        "...I",
    ]
    return LevelsRepository._parse_level(lines)


def is_same_levels(level1, level2):
    for first_group, second_group in zip(level1, level2):
        if len(first_group) == len(second_group):
            return False
    return True
