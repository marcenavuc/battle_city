import pygame

from battle_city.level import LevelsRepository
from battle_city.view import Display
from battle_city.config import DISPLAY_SIZE, FPS


pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

display = Display(pygame.display.set_mode(DISPLAY_SIZE, pygame.RESIZABLE),
                  font=pygame.font.Font("battle_city/media/batle_font.ttf", 30))
levels_repository = LevelsRepository("battle_city/media/levels")


is_start = True
is_game = True
current_level = 0

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.VIDEORESIZE:
            display.width, display.height = event.size

    if is_start:
        is_start = display.main_screen()
    elif is_game:
        is_game = display.game_screen(levels_repository[current_level], event)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
quit()
