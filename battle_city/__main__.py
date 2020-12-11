import pygame

from battle_city.level import LevelsRepository
from battle_city.view import Display
from battle_city.config import DISPLAY_SIZE, FPS, FONT_PATH, LEVELS_PATH, \
    FONT_SIZE

import logging
import sys
import os

application_folder = os.path.dirname(os.path.abspath(__file__))
fonts_path = os.path.join(application_folder, FONT_PATH)
levels_path = os.path.join(application_folder, LEVELS_PATH)

# Init logger
logging.basicConfig(
    level=logging.DEBUG,
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)
logger.debug("game started")
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

logger.debug("main parameters was initialized")

display = Display(pygame.display.set_mode(DISPLAY_SIZE, pygame.RESIZABLE),
                  font=pygame.font.Font(fonts_path, FONT_SIZE))
levels_repository = LevelsRepository(levels_path)


is_start = True
is_game = True
current_level = 0

logger.debug("main loop started")

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
        # levels_repository[current_level].update_gameobjs(event)
        is_game = display.game_screen(levels_repository[current_level], event)

    pygame.display.update()
    clock.tick(FPS)

logger.debug("game ended")
pygame.quit()
quit()
