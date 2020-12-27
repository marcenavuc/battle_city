import logging
from enum import Enum, auto
from typing import Tuple

import pygame

from battle_city import Level
from battle_city.config import GAME_MUSIC_PATH, MENU_MUSIC_PATH, FONTS_PATH
from battle_city.config import DISPLAY_SIZE, FONT_SIZE, FPS
from battle_city.controller import GameStates

logger = logging.getLogger(__name__)

#
# class ViewStates(Enum):
#     GAME = auto()
#     START = auto()
#     DIE = auto()
#     SAVE = auto()
#     PAUSE = auto()


class Button:
    def __init__(self, *args, **kwargs):
        self.rect = pygame.Rect(*args, **kwargs)

    def is_clicked(self) -> bool:
        left_button = pygame.mouse.get_pressed()[0]
        return self.is_moused() and left_button

    def is_moused(self) -> bool:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return (
                self.rect.x < mouse_x < self.rect.x + self.rect.width
                and self.rect.y < mouse_y < self.rect.y + self.rect.height
        )


class Display:

    def __init__(self):
        self.screen = pygame.display.set_mode(DISPLAY_SIZE, pygame.RESIZABLE)
        self.width, self.height = self.screen.get_size()
        self.font = pygame.font.Font(FONTS_PATH, FONT_SIZE)
        self.width_center = self.width / 2
        logger.debug("Display was created")

    def _draw_text(self, text: str, x: float, y: float) \
            -> Tuple[pygame.Rect, pygame.Rect]:
        text_surface = self.font.render(text, True, pygame.Color("red"))
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)
        return text_rect

    def _draw_button(self, text: str, x: float, y: float) -> Button:
        return Button(self._draw_text(text, x, y))

    def main_screen(self):
        self.screen.fill(pygame.Color("black"))

        self._draw_text("BATTLE CITY", self.width_center, self.height / 3)

        play_button = self._draw_button(
            "PLAY", self.width_center, self.height / 2
        )

        save_button = self._draw_button(
            "LOAD LATEST SAVE", self.width_center, 2 / 3 * self.height
        )

        if play_button.is_clicked() or save_button.is_clicked():
            logger.debug("Main screen was ended")

        return play_button.is_clicked(), save_button.is_clicked()

    def game_screen(self, level: Level, event: pygame.event):
        self.screen.fill(pygame.Color("black"))
        for game_group in level:
            game_group.update(event, level)
            game_group.draw(self.screen)

    def die_screen(self):
        self.screen.fill(pygame.Color("black"))
        self._draw_text("WASTED", self.width_center, self.height / 3)

        level_button = self._draw_button(
            "PLAY AGAIN", self.width_center, self.height / 2
        )

        menu_button = self._draw_button(
            "MENU", self.width_center, self.height / 3 * 2
        )

        if menu_button.is_clicked():
            logger.debug("Main screen was ended")
        if level_button.is_clicked():
            logger.debug("Rerun previous level")

        return menu_button.is_clicked(), level_button.is_clicked()

    # def save_screen(self, save_names):
    #     height = self.height / 5
    #     self.screen.fill(pygame.Color("black"))
    #     return_button = self._draw_button(
    #         "RETURN", self.width / 8, self.height - self.height / 8
    #     )
    #     buttons = []
    #     for i, save_name in enumerate(save_names):
    #         buttons.append(
    #             self._draw_button(
    #                 save_name, self.width_center, height * (i + 1)
    #             )
    #         )
    #     index = -1
    #     for i, button in enumerate(buttons):
    #         if button.is_clicked():
    #             index = i
    #             break
    #     return return_button.is_clicked(), index

    def pause_screen(self):
        self.screen.fill(pygame.Color("black"))
        self._draw_text("PAUSE", self.width_center, self.height / 3)
        save_button = self._draw_button(
            "SAVE GAME", self.width_center, 2 / 3 * self.height
        )
        return save_button.is_clicked()


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

    def show(self, state: GameStates, level, event):
        result_state = state
        if state == GameStates.GAME:
            self.menu_music.set_volume(0)
            self.game_music.set_volume(1)
            self.display.game_screen(level, event)
        if state == GameStates.START:
            self.menu_music.set_volume(1)
            self.game_music.set_volume(0)
            is_game, is_save = self.display.main_screen()
            if is_game:
                result_state = GameStates.GAME
            if is_save:
                result_state = GameStates.LOAD_SAVE
        if state == GameStates.DIE:
            is_start, is_game = self.display.die_screen()
            if is_game:
                result_state = GameStates.RELOAD_LEVEL
            if is_start:
                result_state = GameStates.START
        if state == GameStates.PAUSE:
            is_save = self.display.pause_screen()
            if is_save:
                result_state = GameStates.SAVE_LEVEL

        # pygame.display.update()
        self.clock.tick(FPS)
        return result_state
