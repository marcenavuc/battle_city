import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Iterator

from battle_city.config import CELL_HEIGHT, CELL_WIDTH, LEVELS_PATH
from battle_city.game_objects import GameObject, Missile, Player
from battle_city.game_objects.blocks import (CENTER, GreenBrush, Wall,
                                             Floor, Block)
from battle_city.game_objects.bonuses import Bonus
from battle_city.game_objects.tanks import EnemyTank
from battle_city.utils import Vector

logger = logging.getLogger(__name__)


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
        return self._parse_level(lines)

    def reload(self, index: int):
        logger.debug(f"reloading level {index}")
        if self.latest_level is not None:
            self.latest_level = self.load_level(index)

    @classmethod
    def _parse_level(cls, lines: List[str]) -> "Level":
        objects = {name: [] for name in GameObject.registry.keys()}
        for y, line in enumerate(lines):
            for x, symbol in enumerate(line.strip()):
                position = Vector(x * CELL_WIDTH, y * CELL_HEIGHT)
                game_obj = cls._get_from_symbol(symbol, position)
                if game_obj is None:
                    continue
                objects[game_obj.__class__.__name__].append(game_obj)

        return Level(objects, x * CELL_WIDTH, y * CELL_HEIGHT)

    @staticmethod
    def _listdir_fullpath(path: str) -> list:
        return sorted([os.path.join(path, file) for file in os.listdir(path)])

    @staticmethod
    def _get_from_symbol(symbol: str, position: Vector) -> GameObject:
        game_class = list(filter(lambda name: name.startswith(symbol),
                                 GameObject.registry.keys()))
        return None if game_class == [] else GameObject.registry[
            game_class[0]](position)

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
    def __init__(self, game_objs: Dict[str, List["GameObject"]],
                 width: int, height: int):
        self.game_objs = game_objs
        self.width = width
        self.height = height
        # GameObjects

        self.tanks = game_objs[EnemyTank.__name__]
        for tank_cls in EnemyTank.__subclasses__():
            self.tanks.extend(game_objs[tank_cls.__name__])

        self.blocks = []
        for block_cls in Block.__subclasses__():
            self.blocks.extend(game_objs[block_cls.__name__])

        self.bonuses = []
        for bonus_cls in Bonus.__subclasses__():
            self.bonuses.extend(game_objs[bonus_cls.__name__])

        self.floor = game_objs[Floor.__name__]
        self.player = game_objs[Player.__name__][0]
        self.command_center = game_objs[CENTER.__name__][0]
        self.missiles = game_objs[Missile.__name__]
        self.walls = game_objs[Wall.__name__]
        self.brush = game_objs[GreenBrush.__name__]
        logger.debug("Level was created")
        logger.debug(f"Loaded this objects {self.game_objs}")

    def __iter__(self) -> Iterator["GameObject"]:
        collection = []
        for objs in [self.blocks, self.tanks, self.missiles, self.bonuses,
                     self.floor, self.brush]:
            collection.extend(objs)
        collection.append(self.player)
        collection.append(self.command_center)
        return iter(collection)

    # def serialize(self, text: str):
    #     serialize_obj = {"max_x": self.width, "max_y": self.height}
    #     for group_name, group in self.groups.items():
    #         serialize_obj[group_name] = group.sprites()
    #     with open(f"saves/{text}.txt", "w") as file:
    #         json.dump(serialize_obj, file, default=lambda x: x.__dict__(),
    #                   indent=4)
    #     logger.debug("Level was serialized")

    # @classmethod
    # def unserialize(cls, file_path: str) -> "Level":
    #     logger.debug("Started unserialization")
    #     with open(file_path) as json_file:
    #         serialize_obj = json.load(json_file)
    #
    #     width = serialize_obj["width"]
    #     height = serialize_obj["height"]
    #     groups = {}
    #     for group_symbol, values in serialize_obj.items():
    #         group = CharMapEnum.get_from_symbol(group_symbol)
    #         if group:
    #             groups[group.name] = Group()
    #             objs = []
    #             logger.debug(f"Started process group {group.name}")
    #             for json_obj in values:
    #                 game_obj = cls.get_object_from_json(json_obj, group.name)
    #                 objs.append(game_obj)
    #             groups[group.name].add(*objs)
    #     return cls(groups, width, height)
    #
    # @staticmethod
    # def get_object_from_json(json_obj: Dict, group_name: str):
    #     cls = CharMapEnum[group_name].value
    #     position = Vector(json_obj["x"], json_obj["y"])
    #     if not issubclass(cls, GameObject):  # In case of WALLS
    #         cls = Wall
    #     if issubclass(cls, Missile):
    #         logger.debug(f"Founded Missile on pos: {position}")
    #         return cls(position, json_obj.get("direction"))
    #     return cls(position)
