from collections.abc import Sequence
from enum import Enum
from typing import Dict, List, Tuple
import os
import logging

from pygame.sprite import Group

from battle_city.config import CELL_WIDTH, CELL_HEIGHT
from battle_city.game_objects.blocks import Leaves, Water, Iron, \
    Base, Walls
from battle_city.game_objects.tank import SpeedTank
from battle_city.utils import Vector
from battle_city.game_objects import GameObject, EnemyTank, Player, Missile

logger = logging.getLogger(__name__)


class CharMapEnum(Enum):
    WALL = Walls
    AQUA = Water
    IRON = Iron
    BASE = Base
    PLAYER = Player
    LEAVES = Leaves
    TANK = EnemyTank
    SPEEDTANK = SpeedTank
    MISSILE = Missile

    @staticmethod
    def get_from_symbol(symbol: str):
        for item in CharMapEnum:
            if item.name[0] == symbol:
                return item.value

    @staticmethod
    def find_name_by_symbol(symbol: str):
        for item in CharMapEnum:
            if item.name[0] == symbol:
                return item.name


class LevelsRepository(Sequence):
    # CHAR_MAP = {
    #     "W": wall_generator,
    #     "A": Water,
    #     "I": Iron,
    #     "B": Base,
    #     "T": EnemyTank,
    #     "S": SpeedTank,
    #     "P": Player,
    #     "M": Missile,
    #     "L": Leaves,
    # }

    def __init__(self, levels_dir: str):
        self.current_num_of_level = 0
        self.levels_dir = levels_dir
        self.latest_level = None

        assert os.path.exists(levels_dir), "Path should exists"
        self.levels_paths = self._listdir_fullpath(levels_dir)
        logger.debug("LevelsRepository was created")

    def __len__(self) -> int:
        return len(self.levels_paths)

    def __getitem__(self, index: int) -> "Level":
        if self.current_num_of_level != index or self.latest_level is None:
            self.latest_level = self.load_level(index)

        return self.latest_level

    def load_level(self, num: int) -> "Level":
        path = self.levels_paths[num]
        with open(path) as file:
            lines = file.readlines()

        logger.debug(f"loaded level {num}")
        return Level(*self._parse_to_map(lines))

    @staticmethod
    def _parse_to_map(lines: List[str]) -> Tuple[dict, int, int]:
        groups = {group_type.name: Group() for group_type in CharMapEnum}
        # groups = {group_type: Group() for group_type in LevelsRepository.CHAR_MAP}
        # game_env = {}
        for y, line in enumerate(lines):
            for x, symbol in enumerate(line.strip()):
                position = Vector(x * CELL_WIDTH, y * CELL_HEIGHT)
                game_obj = LevelsRepository._get_from_symbol(symbol, position)
                if game_obj is None:
                    continue
                groups[CharMapEnum.find_name_by_symbol(symbol)].add(game_obj)

        return groups, x, y

    @staticmethod
    def _listdir_fullpath(path: str) -> list:
        return sorted([os.path.join(path, file) for file in os.listdir(path)])

    @staticmethod
    def _get_from_symbol(key: str, position: Vector) -> GameObject:
        # obj = LevelsRepository.CHAR_MAP.get(key)
        obj = CharMapEnum.get_from_symbol(key)
        return None if obj is None else obj(position)


class Level:

    def __init__(self, groups: Dict[str, Group], max_x: int, max_y: int):
        self.groups = groups
        self.max_x = max_x * CELL_WIDTH
        self.max_y = max_y * CELL_HEIGHT
        logger.debug("Level was created")

    def __getitem__(self, group_name: str) -> Group:
        print(self.groups)
        return self.groups.get(group_name)

    def __iter__(self) -> List[Group]:
        return iter(self.groups.values())
