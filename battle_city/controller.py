from enum import Enum, auto
import logging
from typing import Tuple

import pygame

from battle_city.level import LevelsRepository

logger = logging.getLogger(__name__)


class GameStates(Enum):
    GAME = auto()
    START = auto()
    DIE = auto()
    RELOAD_LEVEL = auto()
    SAVE_LEVEL = auto()
    PAUSE = auto()
    SAVE = auto()
    LOAD_SAVE = auto()


class Controller:

    def __init__(self):
        self.levels_repository = LevelsRepository()
        self.current_level = 0

    def on_event(self, event: pygame.event, state: GameStates) \
            -> Tuple[GameStates, "Level"]:
        level = self.levels_repository[self.current_level]
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return self.switch_pause()

        if state == GameStates.START:
            self.current_level = 0
            return GameStates.START, level
        if state == GameStates.GAME:
            for game_group in level:
                game_group.update(event, level)
            if len(level["PLAYER"]) == 0 or len(level["COMANDCENTER"]) == 0:
                logger.info("Player was loose")
                return GameStates.DIE, level
            elif len(level["TANKS"]) == 0:
                logger.info("Player wins")
                self.current_level += 1
        else:
            if state == GameStates.RELOAD_LEVEL:
                self.levels_repository.reload(self.current_level)
            if state == GameStates.SAVE_LEVEL:
                self.levels_repository.serialize()
            if state == GameStates.LOAD_SAVE:
                self.levels_repository.unserialize()
            return GameStates.GAME, level
        return state, level

    def switch_pause(self, state, level):
        if state == GameStates.GAME:
            return GameStates.PAUSE, level
        elif state == GameStates.PAUSE:
            return GameStates.GAME, level
