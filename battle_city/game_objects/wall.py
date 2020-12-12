import pygame

from battle_city.config import CELL_SIZE
from battle_city.game_objects.game_object import GameObject


class Wall(GameObject):

    def __init__(self, position, *args, **kwars):
        super().__init__(position, *args, **kwars)
        self.image = pygame.image.load("battle_city/media/images/wall.png")
        self.image = pygame.transform.scale(self.image, CELL_SIZE)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position.x, position.y
