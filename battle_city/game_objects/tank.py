import pygame

from battle_city.utils import Vector
from battle_city.game_objects import Wall, Missile
from battle_city.game_objects.game_object import GameObject, Directions


class Tank(GameObject):

    def __init__(self, *args, **kwars):
        super().__init__(*args, **kwars)
        self.sprite = pygame.image.load("battle_city/media/images/enemy.png")
        self.direction = Directions.DOWN
        self.image = pygame.transform.rotate(self.sprite, 0)
        self.is_shot = True
        self.speed = 5

    def on_event(self, event: pygame.event, level):
        # if self.is_shot:
        #     self.shot(level)
        self.is_shot = False

    def move(self, direction: Directions):
        if self.direction != direction:
            angle = direction.get_angle()
            self.image = pygame.transform.rotate(self.sprite, angle)
            self.direction = direction
        return self.position + direction.value * self.speed

    def set_position(self, position: Vector, level) -> Vector:
        if not isinstance(level[position], Wall) \
                and self.in_borders(position, level):
            return position
        return self.position

    def shot(self, level):
        missile_position = self.set_position(self.go_forward(), level)
        if missile_position != self.position:
            level[missile_position] = Missile(self.direction, missile_position)
