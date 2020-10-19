from typing import Tuple

import pygame

from battle_city.config import CELL_SIZE
from battle_city import Level, GameObject


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

    def _message_to_screen(self, text: str, color,
                           position: Tuple[float, float])\
            -> Tuple[pygame.Rect, pygame.Rect]:

        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = position
        self.screen.blit(text_surface, text_rect)
        return text_surface, text_rect

    def _show_game_obj(self, game_obj: GameObject):
        if game_obj.image:
            img = pygame.transform.scale(game_obj.image, CELL_SIZE)
            self.screen.blit(img, game_obj.position)

    def main_screen(self):
        self.screen.fill(pygame.Color("black"))

        self._message_to_screen("BATTLE CITY",
                                pygame.Color("red"),
                                (self.width / 2, self.height / 3))

        play_button = Button(self._message_to_screen("PLAY",
                                                     pygame.Color("red"),
                                                     (self.width / 2,
                                                      self.height / 2))[1])
        return not play_button.is_clicked()

    def game_screen(self, level: Level, event: pygame.event):
        self.screen.fill(pygame.Color("black"))

        for position in level:
            pygame.time.delay(5)
            if event.type == pygame.KEYDOWN:
                level[position].on_event(event, level)
            self._show_game_obj(level[position])

        level.update()

        return True
