import logging
from enum import Enum, auto
from typing import Tuple

import pygame

from battle_city import GameObject, Level
from battle_city.config import CELL_SIZE

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
        self.x_center = self.width / 2
        logger.debug("Display was created")

    def _message_to_screen(
        self, text: str, position: Tuple[float, float], color=pygame.Color("red")
    ) -> Tuple[pygame.Rect, pygame.Rect]:
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = position
        self.screen.blit(text_surface, text_rect)
        return text_surface, text_rect

    def _show_game_obj(self, game_obj: GameObject):
        if game_obj.image:
            position = game_obj.position
            img = pygame.transform.scale(game_obj.image, CELL_SIZE)
            self.screen.blit(img, position)

    def main_screen(self):
        self.screen.fill(pygame.Color("black"))

        self._message_to_screen("BATTLE CITY", (self.x_center, self.height / 3))

        play_button = Button(
            self._message_to_screen("PLAY", (self.x_center, self.height / 2))[1]
        )

        save_button = Button(
            self._message_to_screen("LOAD SAVE", (self.x_center, self.height / 3 * 2))[
                1
            ]
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
        self._message_to_screen("WASTED", (self.x_center, self.height / 3))

        level_button = Button(
            self._message_to_screen("PLAY AGAIN", (self.x_center, self.height / 2))[1]
        )

        menu_button = Button(
            self._message_to_screen("MENU", (self.x_center, self.height / 3 * 2))[1]
        )
        if menu_button.is_clicked():
            logger.debug("Main screen was ended")
        if level_button.is_clicked():
            logger.debug("Rerun previous level")

        return menu_button.is_clicked(), level_button.is_clicked()

    def save_screen(self, save_names):
        height = self.height / 5
        self.screen.fill(pygame.Color("black"))
        return_button = Button(
            self._message_to_screen(
                "RETURN", (self.width / 8, self.height - self.height / 8)
            )[1]
        )
        buttons = []
        for i, save_name in enumerate(save_names):
            buttons.append(
                Button(
                    self._message_to_screen(
                        save_name[: save_name.find(".txt")],
                        (self.x_center, height * (i + 1)),
                    )[1]
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
        self._message_to_screen("PAUSE", (self.x_center, self.height / 3))
        save_button = Button(
            self._message_to_screen("SAVE GAME", (self.x_center, self.height / 3 * 2))[
                1
            ]
        )
        return save_button.is_clicked()
