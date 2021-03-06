import pygame

from battle_city.config import CELL_SIZE
from battle_city.game_objects import Directions
from battle_city.game_objects.tanks import Tank


class Player(Tank):
    image = "media/images/player.png"
    KEY_MAP = {
        pygame.K_RIGHT: Directions.RIGHT,
        pygame.K_LEFT: Directions.LEFT,
        pygame.K_UP: Directions.UP,
        pygame.K_DOWN: Directions.DOWN,
    }

    def __init__(self, position, *args, **kwars):
        super().__init__(position, *args, **kwars)
        self.sprite = pygame.image.load(Player.image)
        self.sprite = pygame.transform.scale(self.sprite, CELL_SIZE)
        self.image = pygame.transform.rotate(self.sprite, 0)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position.x, position.y
        self.direction = Directions.UP
        self.speed = 5
        self.health = 2

    def update(self, event: pygame.event, level, *args):
        if event.type == pygame.KEYUP:
            self.is_shot = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.shot(level)
                self.is_shot = False
            else:
                direction = Player.KEY_MAP.get(event.key)
                if direction:
                    new_position = self.move(direction)
                    self.rect = self.set_position(new_position, level)

    def set_position(self, position: pygame.rect.Rect, level) \
            -> pygame.rect.Rect:
        new_position = super().set_position(position, level)
        if self.is_collidelist(new_position, level.tanks) >= 0:
            level.player = None
        return new_position
