from enum import Enum
from typing import Dict, List, Tuple
import os
import logging

from pygame.sprite import Group

from battle_city.config import CELL_WIDTH, CELL_HEIGHT
from battle_city.game_objects.blocks import Leaves, Water, Iron, \
    Base, Walls
from battle_city.game_objects.bonuses import SpeedBonus, HealthBonus, RandomKill
from battle_city.game_objects.tanks import EnemyTank, SpeedTank, HeavyTank, \
    RushTank
from battle_city.utils import Vector
from battle_city.game_objects import GameObject, Player, Missile

logger = logging.getLogger(__name__)


class CharMapEnum(Enum):
    WALL = Walls
    AQUA = Water
    IRON = Iron
    COMANDCENTER = Base
    PLAYER = Player
    TANK = EnemyTank
    SPEEDTANK = SpeedTank
    HEAVYTANK = HeavyTank
    RUSHTANK = RushTank
    MISSILE = Missile
    BONUS = HealthBonus
    VELOCITYBONUS = SpeedBonus
    KILLBONUS = RandomKill
    LEAVES = Leaves

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


class LevelsRepository:

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
            self.current_num_of_level = index

        return self.latest_level

    def load_level(self, num: int) -> "Level":
        path = self.levels_paths[num]
        with open(path) as file:
            lines = file.readlines()

        logger.debug(f"loaded level {num}")
        return Level(*self._parse_to_map(lines))

    def refresh(self, current_level: int):
        if not self.latest_level is None:
            self.latest_level = self.load_level(current_level)

    @staticmethod
    def _parse_to_map(lines: List[str]) -> Tuple[dict, int, int]:
        groups = {group_type.name: Group() for group_type in CharMapEnum}
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
        obj = CharMapEnum.get_from_symbol(key)
        return None if obj is None else obj(position)


class Level:

    def __init__(self, groups: Dict[str, Group], max_x: int, max_y: int):
        self.groups = groups
        self.max_x = max_x * CELL_WIDTH
        self.max_y = max_y * CELL_HEIGHT

        self.groups["TANKS"] = Group()
        for tank_type in ["TANK", "SPEEDTANK", "HEAVYTANK", "RUSHTANK"]:
            self.groups["TANKS"].add(self.groups[tank_type].sprites())
            self.groups[tank_type].empty()

        self.groups["BONUSES"] = Group()
        for tank_type in ["BONUS", "VELOCITYBONUS", "KILLBONUS"]:
            self.groups["BONUSES"].add(self.groups[tank_type].sprites())

        logger.debug("Level was created")

    def __getitem__(self, group_name: str) -> Group:
        return self.groups.get(group_name)

    def __iter__(self) -> List[Group]:
        return iter(self.groups.values())
