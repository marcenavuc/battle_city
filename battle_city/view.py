import logging
from enum import Enum, auto
from typing import Tuple

import pygame

from battle_city import Level

logger = logging.getLogger(__name__)


class ViewStates(Enum):
    GAME = auto()
    START = auto()
    DIE = auto()
    SAVE = auto()
    PAUSE = auto()


class Button:
    def __init__(self, *args, **kwargs):
        self.rect = pygame.Rect(*args, **kwargs)

    def is_clicked(self) -> bool:
        left_button = pygame.mouse.get_pressed()[0]
        return self.is_moused() and left_button

    def is_moused(self) -> bool:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return (
            self.rect.x < mouse_x < self.rect.bottomright[0]
            and self.rect.y < mouse_y < self.rect.y + self.rect.height
        )


class Display:
    def __init__(self, screen: pygame.display, font=None):
        self.screen = screen
        self.width, self.height = self.screen.get_size()
        self.font = font
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
            "LOAD SAVE", self.width_center, 2 / 3 * self.height
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

    def save_screen(self, save_names):
        height = self.height / 5
        self.screen.fill(pygame.Color("black"))
        return_button = self._draw_button(
            "RETURN", self.width / 8, self.height - self.height / 8
        )
        buttons = []
        for i, save_name in enumerate(save_names):
            buttons.append(
                self._draw_button(
                    save_name, self.width_center, height * (i + 1)
                )
            )
        index = -1
        for i, button in enumerate(buttons):
            if button.is_clicked():
                index = i
                break
        return return_button.is_clicked(), index

    def pause_screen(self):
        self.screen.fill(pygame.Color("black"))
        self._draw_text("PAUSE", self.width_center, self.height / 3)
        save_button = self._draw_button(
            "SAVE GAME", self.width_center, 2 / 3 * self.height
        )
        return save_button.is_clicked()

