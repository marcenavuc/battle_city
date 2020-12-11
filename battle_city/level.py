from collections.abc import Sequence
from typing import Dict, Iterator, List
import os
import logging

import pygame

from battle_city.config import CELL_WIDTH, CELL_HEIGHT
from battle_city.utils import Vector
from battle_city.game_objects import GameObject, Empty, Tank, Player, Wall

logger = logging.getLogger(__name__)


class LevelsRepository(Sequence):
    CHAR_MAP = {
        ".": Empty,
        "W": Wall,
        "T": Tank,
        "P": Player,
    }

    CHAR_OBJ = ["T", "P"]

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
        return Level(self._parse_to_map(lines))

    @staticmethod
    def _parse_to_map(lines: List[str]) -> Dict[Vector, GameObject]:
        # game_objs = []  # Игровые объекты (Танки)
        # game_env = {}  # Окружение (Стенки)
        game_env = {}
        for y, line in enumerate(lines):
            for x, symbol in enumerate(line.strip()):
                position = Vector(x * CELL_WIDTH, y * CELL_HEIGHT)
                obj = LevelsRepository._get_from_symbol(symbol, position)
                game_env[position] = obj
                # game_env[(x, y)] = obj
                # if symbol in LevelsRepository.CHAR_OBJ:
                #     game_objs.append(obj)

        # return game_env, game_objs
        return game_env

    @staticmethod
    def _listdir_fullpath(path: str) -> list:
        return sorted([os.path.join(path, file) for file in os.listdir(path)])

    @staticmethod
    def _get_from_symbol(key: str, position: Vector) -> GameObject:
        return LevelsRepository.CHAR_MAP[key](position)


class Level:

    def __init__(self, game_env: Dict[Vector, GameObject],
                 # game_objs: List[GameObject]):
                 ):
        self.game_env = game_env
        # self.game_objs = game_objs
        self.max_x = max(game_env.keys(), key=lambda t: t[0])[0]
        self.max_y = max(game_env.keys(), key=lambda t: t[1])[1]

        logger.debug("Level was created")

    def __getitem__(self, key: Vector) -> GameObject:
        return self.game_env.get(key)

    def __setitem__(self, key: Vector, value: GameObject):
        if key in self.game_env:
            self.game_env[key] = value

    def __iter__(self) -> Iterator[Vector]:
        return iter(self.game_env.keys())

    def update(self):
        for key in self.game_env:
            obj_pos = self.game_env[key].position
            if obj_pos != key:
                self.game_env[obj_pos] = self.game_env[key]
                self.game_env[key] = GameObject(key)

    # def update_gameobjs(self, event):
    #     for game_obj in self.game_objs:
    #         game_obj.on_event(event, self)

    def remove(self, position: Vector):
        if position in self.game_env:
            logger.debug(f"Del obj:{self.game_env[position]} pos:{position}")
            self.game_env[position] = GameObject(position)
