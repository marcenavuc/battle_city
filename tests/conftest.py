from collections import namedtuple

import pytest
import pygame

from battle_city import Level
from battle_city.level import LevelsRepository


FakeEvent = namedtuple("Event", ["type", "key"])


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
        "...C",
        ".E..",
        "...I",
    ]
    return LevelsRepository._parse_level(lines)


def is_same_levels(level1, level2):
    return len(list(level1)) == len(list(level2))
