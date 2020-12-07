from collections.abc import Sequence
from typing import Dict, Iterator, List
import os

from battle_city.config import Coords
from battle_city.game_objects import GameObject, Tank, Player, Wall

import logging

logger = logging.getLogger(__name__)


class LevelsRepository(Sequence):
    CHAR_MAP = {
        ".": GameObject,
        "T": Wall,
        "X": Tank,
        "P": Player,
    }

    def __init__(self, levels_dir: str):
        self.current_level = 0
        self.levels_dir = levels_dir
        self.latest_level = None

        assert os.path.exists(levels_dir), "Path should exists"
        self.levels = self._listdir_fullpath(levels_dir)
        logger.debug("LevelsRepository was created")

    def __len__(self) -> int:
        return len(self.levels)

    def __getitem__(self, index: int) -> "Level":
        if self.current_level != index or self.latest_level is None:
            self.latest_level = self.load_level(index)

        return self.latest_level

    def load_level(self, num: int) -> "Level":
        path = self.levels[num]
        with open(path) as file:
            lines = file.readlines()

        logger.debug(f"loaded level {num}")
        return Level(self._parse_to_map(lines))

    @staticmethod
    def _parse_to_map(lines: List[str]) -> Dict[Coords, GameObject]:
        game_map = {}
        for y, line in enumerate(lines):
            for x, symbol in enumerate(line.strip()):
                game_map[(x, y)] = LevelsRepository._get_from_symbol(symbol, (x, y))

        return game_map

    @staticmethod
    def _listdir_fullpath(path: str) -> list:
        return sorted([os.path.join(path, file) for file in os.listdir(path)])

    @staticmethod
    def _get_from_symbol(s: str, position: Coords) -> GameObject:
        return LevelsRepository.CHAR_MAP[s](position)


class Level:

    def __init__(self, game_map: Dict[Coords, GameObject]):
        self.game_map = game_map
        self.max_x = max(game_map.keys(), key=lambda t: t[0])[0]
        self.max_y = max(game_map.keys(), key=lambda t: t[1])[1]
        self.updated = []
        logger.debug("Level was created")

    def __getitem__(self, key: Coords) -> GameObject:
        return self.game_map.get(key)

    def __setitem__(self, key: Coords, value: GameObject):
        if key in self.game_map:
            self.updated.append(key)
            self.game_map[key] = value

    def __iter__(self) -> Iterator[Coords]:
        return iter(self.game_map.keys())

    def update(self):
        for key in self.game_map:
            obj_pos = self.game_map[key].position
            if obj_pos != key:
                self.game_map[obj_pos] = self.game_map[key]
                self.game_map[key] = GameObject(key)

    def remove(self, position: Coords):
        if position in self.game_map:
            logger.debug(f"Del obj:{self.game_map[position]} pos:{position}")
            self.game_map[position] = GameObject(position)
