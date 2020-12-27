import logging
import sys

import pygame

from battle_city.controller import Controller, GameStates
from battle_city.view import View


# Init logger
logging.basicConfig(level=logging.DEBUG,
                    handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)
logger.debug("Game started")


controller = Controller()
logger.debug("controller was initialized")
view = View()
logger.debug("view was initialized")

logger.debug("Main loop started")
game_state = GameStates.START
# Main loop
while True:
    for event in pygame.event.get():
        pass
    game_state, level = controller.on_event(event, game_state)
    game_state = view.show(game_state, level)

logger.debug("game ended")
pygame.quit()
quit()
