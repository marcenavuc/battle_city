import pygame
import pytest

from battle_city.controller import Controller, GameStates
from tests.conftest import FakeEvent


def test_controller_init():
    Controller()
    assert True


@pytest.mark.parametrize("event, state, result", [
    (FakeEvent(type=pygame.KEYDOWN, key=pygame.K_ESCAPE),
     GameStates.GAME, GameStates.PAUSE),
    (FakeEvent(type=pygame.KEYDOWN, key=pygame.K_ESCAPE),
     GameStates.PAUSE, GameStates.GAME),
])
def test_controller_on_event(event, state, result):
    controller = Controller()
    assert controller.on_event([event], state)[0] == result
