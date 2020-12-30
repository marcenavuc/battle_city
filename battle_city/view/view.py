import logging

import pygame

from battle_city.config import GAME_MUSIC_PATH, MENU_MUSIC_PATH
from battle_city.config import FPS
from battle_city.controller import GameStates
from battle_city.view.components import Display

logger = logging.getLogger(__name__)


class View:

    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        logger.debug("Initialized pygame modules")

        self.display = Display()
        logger.debug("Initialized display")

        self.menu_music = pygame.mixer.Sound(MENU_MUSIC_PATH)
        self.game_music = pygame.mixer.Sound(GAME_MUSIC_PATH)
        self.menu_music.set_volume(0)
        self.game_music.set_volume(0)
        self.menu_music.play()
        self.game_music.play()
        logger.debug("Initialized music")

        self.clock = pygame.time.Clock()
        logger.debug("Initialized clock")

    def show(self, state: GameStates, level):
        if state == GameStates.GAME:
            self.menu_music.set_volume(0)
            self.game_music.set_volume(1)
            self.display.game_screen(level)
        elif state == GameStates.START:
            self.menu_music.set_volume(1)
            self.game_music.set_volume(0)
            is_game, is_save = self.display.main_screen()
            if is_game:
                return GameStates.GAME
            if is_save:
                return GameStates.LOAD_SAVE
        elif state == GameStates.DIE:
            is_start, is_game = self.display.die_screen()
            if is_game:
                return GameStates.RELOAD_LEVEL
            if is_start:
                return GameStates.START
        elif state == GameStates.PAUSE:
            is_save = self.display.pause_screen()
            if is_save:
                return GameStates.SAVE_LEVEL

        pygame.display.update()
        self.clock.tick(FPS)
        return state
