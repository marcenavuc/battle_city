import json
import logging
import os
from datetime import datetime
from enum import Enum
from typing import Dict, List, Tuple, Iterator

from pygame.sprite import Group

from battle_city.config import CELL_HEIGHT, CELL_WIDTH, LEVELS_PATH
from battle_city.game_objects import GameObject, Missile, Player
from battle_city.game_objects.blocks import (Base, Iron, Leaves, Wall, Walls,
                                             Water, Floor)
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
    FLOOR = Floor
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

    @classmethod
    def get_from_symbol(cls, symbol: str):
        for item in cls:
            if item.name[0] == symbol:
                return item

    # @staticmethod
    # def find_name_by_symbol(symbol: str):
    #     for item in CharMapEnum:
    #         if item.name[0] == symbol:
    #             return item.name


class LevelsRepository:
    def __init__(self):
        self.current_num_of_level = 0
        self.levels_dir = LEVELS_PATH
        self.latest_level = None

        assert os.path.exists(self.levels_dir), "Path should exists"
        self.levels_paths = self._listdir_fullpath(self.levels_dir)
        logger.debug("LevelsRepository was created")

    def __len__(self) -> int:
        return len(self.levels_paths)

    def __getitem__(self, index: int) -> "Level":
        if self.current_num_of_level != index or self.latest_level is None:
            self.latest_level = self.load_level(index)
            self.current_num_of_level = index

        return self.latest_level

    def load_level(self, index: int) -> "Level":
        path = self.levels_paths[index]
        with open(path) as file:
            lines = file.readlines()

        logger.debug(f"loaded level {index}")
        return Level(*self._parse_to_map(lines))

    def reload(self, index: int):
        logger.debug(f"reloading level {index}")
        if self.latest_level is not None:
            self.latest_level = self.load_level(index)

    @classmethod
    def _parse_to_map(cls, lines: List[str]) -> Tuple[dict, int, int]:
        groups = {group_type.name: Group() for group_type in CharMapEnum}
        for y, line in enumerate(lines):
            for x, symbol in enumerate(line.strip()):
                position = Vector(x * CELL_WIDTH, y * CELL_HEIGHT)
                game_obj = cls._get_from_symbol(symbol, position)
                if game_obj is None:
                    continue
                groups[CharMapEnum.get_from_symbol(symbol).name].add(game_obj)

        return groups, x * CELL_WIDTH, y * CELL_HEIGHT

    @staticmethod
    def _listdir_fullpath(path: str) -> list:
        return sorted([os.path.join(path, file) for file in os.listdir(path)])

    @staticmethod
    def _get_from_symbol(key: str, position: Vector) -> GameObject:
        obj = CharMapEnum.get_from_symbol(key)
        return None if obj is None else obj.value(position)

    def serialize(self):
        if self.latest_level:
            date = datetime.now().strftime('%d:%m:%y %H:%M')
            save_name = f"level:{self.current_num_of_level} {date}.json"
            level = self.latest_level
            serialize_obj = {"width": level.width, "heigth": level.height}
            for group_name, group in level.groups.items():
                serialize_obj[group_name] = group.sprites()
            with open(os.path.join("saves/", save_name), "w") as file:
                json.dump(serialize_obj, file,
                          default=lambda x: x.__dict__(), indent=4)
            logger.debug("Level was serialized")


class Level:
    def __init__(self, groups: Dict[str, Group], width: int, height: int):
        self.groups = groups
        self.width = width
        self.height = height

        self.groups["TANKS"] = Group()
        for tank_type in ["TANK", "SPEEDTANK", "HEAVYTANK", "RUSHTANK"]:
            self.groups["TANKS"].add(self.groups[tank_type].sprites())
            self.groups[tank_type].empty()

        self.groups["BONUSES"] = Group()
        for tank_type in ["BONUS", "VELOCITYBONUS", "KILLBONUS"]:
            self.groups["BONUSES"].add(self.groups[tank_type].sprites())

        leaves_group = self.groups.pop("LEAVES", Group())
        self.groups["LEAVES"] = leaves_group
        logger.debug("Level was created")
        logger.debug(self.groups)

    def __getitem__(self, group_name: str) -> Group:
        return self.groups.get(group_name)

    def __iter__(self) -> Iterator[Group]:
        return iter(self.groups.values())

    def serialize(self, text: str):
        serialize_obj = {"max_x": self.width, "max_y": self.height}
        for group_name, group in self.groups.items():
            serialize_obj[group_name] = group.sprites()
        with open(f"saves/{text}.txt", "w") as file:
            json.dump(serialize_obj, file, default=lambda x: x.__dict__(), indent=4)
        logger.debug("Level was serialized")

    @classmethod
    def unserialize(cls, file_path: str) -> "Level":
        logger.debug("Started unserialization")
        with open(file_path) as json_file:
            serialize_obj = json.load(json_file)

        width = serialize_obj["width"]
        height = serialize_obj["height"]
        groups = {}
        for group_symbol, values in serialize_obj.items():
            group = CharMapEnum.get_from_symbol(group_symbol)
            if group:
                groups[group.name] = Group()
                objs = []
                logger.debug(f"Started process group {group.name}")
                for json_obj in values:
                    game_obj = cls.get_object_from_json(json_obj, group.name)
                    objs.append(game_obj)
                groups[group.name].add(*objs)
        return cls(groups, width, height)

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
