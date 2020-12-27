import logging
import os
import sys

import pygame

# from battle_city.config import (DISPLAY_SIZE, FONT_PATH, FONT_SIZE, FPS,
#                                 LEVELS_PATH)
from battle_city.controller import Controller, GameStates
from battle_city.level import Level, LevelsRepository
from battle_city.view import Display, View

# application_folder = os.path.dirname(os.path.abspath(__file__))
# fonts_path = os.path.join(application_folder, FONT_PATH)
# levels_path = os.path.join(application_folder, LEVELS_PATH)

# Init logger
logging.basicConfig(level=logging.DEBUG,
                    handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)
logger.debug("Game started")

# pygame.init()
# pygame.font.init()
# pygame.mixer.init()
# logger.debug("Initialized pygame modules")

# BACKGROUND_MUSIC = pygame.mixer.Sound("media/sounds/DOOM.ogg")
# MENU_MUSIC = pygame.mixer.Sound("media/sounds/ANewMorning.ogg")
# BACKGROUND_MUSIC.set_volume(0)
# MENU_MUSIC.set_volume(0)
# BACKGROUND_MUSIC.play()
# MENU_MUSIC.play()
# logger.debug("Initialized music")

# clock = pygame.time.Clock()
logger.debug("main parameters was initialized")

# display = Display(fonts_path)
controller = Controller()
logger.debug("controller was initialized")
view = View()
logger.debug("view was initialized")



# levels_repository = LevelsRepository(levels_path)
# state = ViewStates.START
# current_level = 0
logger.debug("Main loop started")
game_state = GameStates.START
# Main loop
while True:
    for event in pygame.event.get():
        game_state, level = controller.on_event(event, game_state)
        game_state = view.show(game_state, level, event)
    #     if event.type == pygame.QUIT:
    #         exit()
    #     if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
    #         if state == ViewStates.GAME:
    #             state = ViewStates.PAUSE
    #         elif state == ViewStates.PAUSE:
    #             state = ViewStates.GAME
    #
    # if state == ViewStates.START:
    #     MENU_MUSIC.set_volume(1)
    #     BACKGROUND_MUSIC.set_volume(0)
    #     current_level = 0
    #     is_game, is_save = display.main_screen()
    #     if is_game:
    #         state = ViewStates.GAME
    #     if is_save:
    #         state = ViewStates.SAVE
    # if state == ViewStates.GAME:
    #     MENU_MUSIC.set_volume(0)
    #     BACKGROUND_MUSIC.set_volume(1)
    #     level = levels_repository[current_level]
    #     if len(level["PLAYER"]) == 0 or len(level["COMANDCENTER"]) == 0:
    #         logger.info("Player was loose")
    #         state = ViewStates.DIE
    #     elif len(level["TANKS"]) == 0:
    #         logger.info("Player wins")
    #         current_level += 1
    #     else:
    #         display.game_screen(level, event)
    # if state == ViewStates.DIE:
    #     BACKGROUND_MUSIC.set_volume(0)
    #     MENU_MUSIC.set_volume(1)
    #     is_start, is_game = display.die_screen()
    #     if is_game:
    #         state = ViewStates.GAME
    #         levels_repository.reload(current_level)
    #     if is_start:
    #         state = ViewStates.START
    # if state == ViewStates.SAVE:
    #     is_start, save_index = display.save_screen(os.listdir("saves"))
    #     if is_start and save_index == -1:
    #         state = ViewStates.START
    #     elif save_index != -1:
    #         save_path = levels_repository._listdir_fullpath("saves/")[save_index]
    #         level_num = int(save_path.split()[1])
    #         save = Level.unserialize(save_path)
    #         levels_repository.latest_level = save
    #         levels_repository.current_num_of_level = level_num
    #         current_level = level_num
    #         state = ViewStates.GAME
    #
    # if state == ViewStates.PAUSE:
    #     is_save = display.pause_screen()
    #     if is_save:
    #         logger.debug("Saving level")
    #         # date = datetime.now().strftime('%d:%m:%y %H:%M')
    #         # level.serialize(f"level:{current_level} {date}")
    #         levels_repository.serialize()
    #         state = ViewStates.GAME
    #
    # pygame.display.update()
    # clock.tick(FPS)

logger.debug("game ended")
pygame.quit()
quit()
