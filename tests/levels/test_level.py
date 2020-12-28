import os
import pytest

from battle_city import Level
from battle_city.game_objects import Missile, Directions
from battle_city.game_objects.blocks import Iron, Wall
from battle_city.game_objects.tanks import EnemyTank
from tests.conftest import is_same_levels


def test_level_initialization():
    Level
    assert True


def test_level_iter(level):
    iter(level)
    assert True

