import logging
from typing import Tuple

import pygame

from battle_city import Level
from battle_city.config import FONTS_PATH
from battle_city.config import DISPLAY_SIZE, FONT_SIZE


logger = logging.getLogger(__name__)


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

    def _draw_gameobject(self, game_obj: "GameObject"):
        # game_obj.draw(self.screen)
        self.screen.blit(game_obj.image, game_obj.rect)


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

    def game_screen(self, level: Level):
        self.screen.fill(pygame.Color("black"))
        for game_obj in level:
            # game_group.image.draw(self.screen)
            self._draw_gameobject(game_obj)

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

    def pause_screen(self):
        self.screen.fill(pygame.Color("black"))
        self._draw_text("PAUSE", self.width_center, self.height / 3)
        save_button = self._draw_button(
            "SAVE GAME", self.width_center, 2 / 3 * self.height
        )
        return save_button.is_clicked()
