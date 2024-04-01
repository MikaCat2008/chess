from __future__ import annotations

from abc import ABC, abstractmethod

from sdk import BaseGameType, BasePlayerType, BaseGameManagerType, BasePlayerManagerType


class Jsonable(ABC):
    @abstractmethod
    def to_json(self) -> dict:
        ...


class GameType(BaseGameType, Jsonable):
    players: list[PlayerType]


class PlayerType(BasePlayerType, Jsonable):
    username: str


class GameManagerType(BaseGameManagerType):
    games: list[GameType]


class PlayerManagerType(BasePlayerManagerType):
    players: list[PlayerType]

    @abstractmethod
    def create_player(self, id: int, username: str) -> BasePlayerType:
        ...

    @abstractmethod
    def get_player_by_username(self, username: str) -> PlayerType:
        ...
