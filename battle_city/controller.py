from enum import Enum, auto
import logging

import pygame

from battle_city.level import LevelsRepository
# from battle_city.view import ViewStates

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

    def __init__(self, levels_dir: str):
        self.levels_repository = LevelsRepository(levels_dir)
        self.current_level = 0

    def on_event(self, event: pygame.event, state: GameStates) \
            -> GameStates:
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if state == GameStates.GAME:
                return GameStates.PAUSE
            elif state == GameStates.PAUSE:
                return GameStates.GAME

        if state == GameStates.START:
            self.current_level = 0
        if state == GameStates.GAME:
            level = self.levels_repository[self.current_level]
            if len(level["PLAYER"]) == 0 or len(level["COMANDCENTER"]) == 0:
                logger.info("Player was loose")
                return GameStates.DIE
            elif len(level["TANKS"]) == 0:
                logger.info("Player wins")
                self.current_level += 1
        if state == GameStates.RELOAD_LEVEL:
            self.levels_repository.reload(self.current_level)
            return GameStates.GAME
        if state == GameStates.SAVE_LEVEL:
            logger.debug("Saving level")
            self.levels_repository.serialize()
            return GameStates.GAME
        if state == GameStates.LOAD_SAVE:
            self.levels_repository.unserialize()
            return GameStates.GAME
        return state
