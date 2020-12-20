from typing import Tuple

import pygame

from battle_city.config import CELL_SIZE, CELL_WIDTH, CELL_HEIGHT
from battle_city import Level, GameObject

import logging

logger = logging.getLogger(__name__)


class Button:

    def __init__(self, *args, **kwargs):
        self.rect = pygame.Rect(*args, **kwargs)

    def is_clicked(self) -> bool:
        left_button = pygame.mouse.get_pressed()[0]
        return self.is_moused() and left_button

    def is_moused(self) -> bool:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return self.rect.x < mouse_x < self.rect.bottomright[0] \
               and self.rect.y < mouse_y < self.rect.y + self.rect.height


class Display:

    def __init__(self, screen: pygame.display, font=None):
        self.screen = screen
        self.width, self.height = self.screen.get_size()
        self.font = font
        logger.debug("Display was created")

    def _message_to_screen(self, text: str, color,
                           position: Tuple[float, float]) \
            -> Tuple[pygame.Rect, pygame.Rect]:

        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = position
        self.screen.blit(text_surface, text_rect)
        return text_surface, text_rect

    def _show_game_obj(self, game_obj: GameObject):
        if game_obj.image:
            # position = game_obj.position[0] * CELL_WIDTH,\
            #            game_obj.position[1] * CELL_HEIGHT
            position = game_obj.position
            img = pygame.transform.scale(game_obj.image, CELL_SIZE)
            self.screen.blit(img, position)

    def main_screen(self):
        self.screen.fill(pygame.Color("black"))

        self._message_to_screen("BATTLE CITY",
                                pygame.Color("red"),
                                (self.width / 2, self.height / 3))

        play_button = Button(self._message_to_screen("PLAY",
                                                     pygame.Color("red"),
                                                     (self.width / 2,
                                                      self.height / 2))[1])
        if play_button.is_clicked():
            logger.debug("Main screen was ended")

        return not play_button.is_clicked()

    def game_screen(self, level: Level, event: pygame.event):
        self.screen.fill(pygame.Color("black"))
        for game_group in level:
            game_group.update(event, level)
            game_group.draw(self.screen)
        return True

    def die_screen(self):
        self.screen.fill(pygame.Color("black"))
        self._message_to_screen("WASTED",
                                pygame.Color("red"),
                                (self.width / 2, self.height / 3))

        level_button = Button(self._message_to_screen("PLAY AGAIN",
                                                      pygame.Color("red"),
                                                      (self.width / 2,
                                                       self.height / 2))[1])

        menu_button = Button(self._message_to_screen("MENU",
                                                     pygame.Color("red"),
                                                     (self.width / 2,
                                                      self.height / 3 * 2))[1])
        if menu_button.is_clicked():
            logger.debug("Main screen was ended")
        if level_button.is_clicked():
            logger.debug("Rerun previous level")

        return menu_button.is_clicked(), level_button.is_clicked()
