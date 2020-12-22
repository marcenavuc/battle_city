import json
import logging
import os
from enum import Enum
from typing import Dict, List, Tuple

from pygame.sprite import Group

from battle_city.config import CELL_HEIGHT, CELL_WIDTH
from battle_city.game_objects import GameObject, Missile, Player
from battle_city.game_objects.blocks import (Base, Iron, Leaves, Wall, Walls,
                                             Water)
from battle_city.game_objects.bonuses import (HealthBonus, RandomKill,
                                              SpeedBonus)
from battle_city.game_objects.tanks import (EnemyTank, HeavyTank, RushTank,
                                            SpeedTank)
from battle_city.utils import Vector

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
        if self.latest_level is not None:
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

    def serialize(self, text: str):
        serialize_obj = {"max_x": self.max_x, "max_y": self.max_y}
        for group_name, group in self.groups.items():
            serialize_obj[group_name[0]] = group.sprites()
        with open(f"saves/{text}.txt", "w") as file:
            json.dump(serialize_obj, file, default=lambda x: x.__dict__(), indent=4)
        logger.debug("Level was serialized")

    @staticmethod
    def unserialize(file_path: str) -> "Level":
        logger.debug("Started unserialization")
        with open(file_path) as json_file:
            serialize_obj = json.load(json_file)

        max_x = serialize_obj["max_x"]
        max_y = serialize_obj["max_y"]
        groups = {}
        for group_symbol, values in serialize_obj.items():
            group_name = CharMapEnum.find_name_by_symbol(group_symbol)
            if group_name:
                groups[group_name] = Group()
                objs = []
                logger.debug(f"Started process group {group_name}")
                for json_obj in values:
                    game_obj = Level.get_object_from_json(json_obj, group_name)
                    objs.append(game_obj)
                groups[group_name].add(*objs)
        return Level(groups, max_x, max_y)

    @staticmethod
    def get_object_from_json(json_obj: Dict, group_name: str):
        cls = CharMapEnum[group_name].value
        position = Vector(json_obj["x"], json_obj["y"])
        if not issubclass(cls, GameObject):  # In case of WALLS
            cls = Wall
        if issubclass(cls, Missile):
            logger.debug(f"Founded Missile on pos: {position}")
            return cls(position, json_obj.get("direction"))
        return cls(position)
