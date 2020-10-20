import pygame

from battle_city.config import Coords
from battle_city.game_objects import Wall, Missile
from battle_city.game_objects.game_object import GameObject, Directions


class Tank(GameObject):

    def __init__(self, *args, **kwars):
        super().__init__(*args, **kwars)
        self.image = pygame.image.load("battle_city/media/images/enemy.png")
        self.direction = Directions.DOWN
        self.is_shot = True

    def on_event(self, event: pygame.event, level):
        if self.is_shot:
            self.shot(level)
        self.is_shot = False

    def go_right(self):
        self.image = pygame.transform.rotate(self.image, 270)
        self.direction = self.direction.next()

    def go_left(self):
        self.image = pygame.transform.rotate(self.image, 90)
        self.direction = self.direction.previous()

    def go_forward(self) -> Coords:
        return (self.position[0] + self.direction.value[0],
                self.position[1] - self.direction.value[1])

    def go_back(self) -> Coords:
        return (self.position[0] - self.direction.value[0],
                self.position[1] + self.direction.value[1])

    def set_position(self, position: Coords, level) -> Coords:
        if not isinstance(level[position], Wall) \
                and self.in_borders(position, level):
            return position
        return self.position

    def shot(self, level):
        missile_position = self.set_position(self.go_forward(), level)
        if missile_position != self.position:
            level[missile_position] = Missile(self.direction, missile_position)
