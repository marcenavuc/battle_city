import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Iterator

from dataclasses import dataclass, field

from battle_city.config import CELL_HEIGHT, CELL_WIDTH, LEVELS_PATH
from battle_city.game_objects import GameObject, Missile, Player
from battle_city.game_objects.blocks import (Center, GreenBrush, Wall,
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
        self.latest_save_path = None

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
            self.current_num_of_level = index

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
        return cls.create_level(x * CELL_WIDTH, y * CELL_HEIGHT, objects)

    @staticmethod
    def _listdir_fullpath(path: str) -> list:
        return sorted([os.path.join(path, file) for file in os.listdir(path)])

    @staticmethod
    def _get_from_symbol(symbol: str, position: Vector) -> GameObject:
        game_class = list(filter(lambda name: name.startswith(symbol),
                                 GameObject.registry.keys()))
        return None if game_class == [] else GameObject.registry[
            game_class[0]](position)

    @staticmethod
    def create_level(width: int, height: int,
                     game_objs: Dict[str, List["GameObject"]]):
        level = Level(width, height)
        for key in game_objs:
            if key == "Player":
                level.player = game_objs[key][0]
            elif key.endswith("Bonus"):
                level.bonuses.extend(game_objs[key])
            elif key == "Floor":
                level.floor.extend(game_objs[key])
            elif key == "Wall":
                level.walls.extend(game_objs[key])
            elif key == "GreenBrush":
                level.brushes.extend(game_objs[key])
            elif key == "Missile":
                level.missiles.extend(game_objs[key])
            elif key == "Center":
                level.command_center = game_objs[key][0]
            elif key.endswith("Tank"):
                level.tanks.extend(game_objs[key])
            else:
                level.blocks.extend(game_objs[key])
        print(level)
        return level

    def save_level(self):
        if self.latest_level:
            date = datetime.now().strftime('%d:%m:%y %H:%M')
            save_name = f"level:{self.current_num_of_level} {date}.json"
            if not os.path.exists("saves/"):
                os.mkdir("saves/")
            path = os.path.join("saves/", save_name)
            self.latest_save_path = path

            level = self.latest_level
            serialize_obj = {name: [] for name in GameObject.registry.keys()}
            serialize_obj["width"] = level.width
            serialize_obj["height"] = level.height
            for game_obj in level:
                serialize_obj[game_obj.__class__.__name__].append(game_obj)
            with open(path, "w") as file:
                json.dump(serialize_obj, file,
                          default=lambda x: x.__dict__(), indent=4)
            logger.debug("Level was serialized")

    def load_latest_save(self):
        if self.latest_save_path is None:
            return

        logger.debug("Started unserialization")
        with open(self.latest_save_path) as json_file:
            serialize_obj = json.load(json_file)

        width = serialize_obj.pop("width")
        height = serialize_obj.pop("height")
        objects = {}
        for class_name, values in serialize_obj.items():
            objects[class_name] = []
            logger.debug(f"Started process group {class_name}")
            for json_obj in values:
                position = Vector(json_obj["x"], json_obj["y"])
                direction = json_obj.get("direction")
                if direction:
                    game_obj = GameObject.registry[class_name](position,
                                                               direction)
                else:
                    game_obj = GameObject.registry[class_name](position)
                objects[class_name].append(game_obj)
        self.latest_level = self.create_level(width, height, objects)


@dataclass(init=True, repr=True)
class Level:
    width: int
    height: int
    blocks: List[Block] = field(default_factory=list)
    bonuses: List[Bonus] = field(default_factory=list)
    floor: List[Floor] = field(default_factory=list)
    missiles: List[Missile] = field(default_factory=list)
    walls: List[Wall] = field(default_factory=list)
    brushes: List[GreenBrush] = field(default_factory=list)
    tanks: List[EnemyTank] = field(default_factory=list)
    player: Player = None
    command_center: Center = None

    def __iter__(self) -> Iterator["GameObject"]:
        collection = []
        for objs in [self.blocks, self.walls, self.tanks, self.missiles,
                     self.bonuses, self.floor, self.brushes]:
            collection.extend(objs)
        collection.append(self.player)
        collection.append(self.command_center)
        return iter(collection)
