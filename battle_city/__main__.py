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
logger.debug("Game started")

pygame.init()
pygame.font.init()
pygame.mixer.init()
logger.debug("Initialized pygame things")

BACKGROUND_MUSIC = pygame.mixer.Sound('battle_city/media/sounds/DOOM.ogg')
MENU_MUSIC = pygame.mixer.Sound('battle_city/media/sounds/ANewMorning.ogg')
FIRE_MUSIC = pygame.mixer.Sound('battle_city/media/sounds/fire.ogg')
BACKGROUND_MUSIC.set_volume(0)
MENU_MUSIC.set_volume(0)
FIRE_MUSIC.set_volume(0)
BACKGROUND_MUSIC.play()
MENU_MUSIC.play()
FIRE_MUSIC.play()
logger.debug("Initialized music")

clock = pygame.time.Clock()
logger.debug("main parameters was initialized")

display = Display(pygame.display.set_mode(DISPLAY_SIZE, pygame.RESIZABLE),
                  font=pygame.font.Font(fonts_path, FONT_SIZE))
logger.debug("display initialized")

levels_repository = LevelsRepository(levels_path)

is_start = True
is_game = True
is_die = True
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
        MENU_MUSIC.set_volume(1)
        BACKGROUND_MUSIC.set_volume(0)
        current_level = 0
        is_start = display.main_screen()
    elif is_game:
        MENU_MUSIC.set_volume(0)
        BACKGROUND_MUSIC.set_volume(1)
        level = levels_repository[current_level]
        if len(level["PLAYER"]) == 0:
            logger.info("Player was die")
            is_game = False
        elif len(level["COMANDCENTER"]) == 0:
            logger.info("Command center was destroyed")
            is_game = False
        elif len(level["TANKS"]) == 0:
            logger.info("Player wins")
            current_level += 1
        else:
            is_game = display.game_screen(level, event)
    elif is_die:
        BACKGROUND_MUSIC.set_volume(0)
        MENU_MUSIC.set_volume(1)
        is_start, is_game = display.die_screen()
        if is_game:
            levels_repository.refresh(current_level)

    pygame.display.update()
    clock.tick(FPS)

logger.debug("game ended")
pygame.quit()
quit()
