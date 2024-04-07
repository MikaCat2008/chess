from __future__ import annotations

from abc import ABC, abstractmethod

Pos = tuple[int, int]
Piece = tuple[bool, int, Pos]
MoveData = tuple[Piece, Piece]


class BaseGameType(ABC):
    id: int
    side: bool
    board: list[list[int]]
    started: bool
    players: list[BasePlayerType]

    @abstractmethod
    def join(self, player: BasePlayerType) -> None:
        ...

    @abstractmethod
    def start(self) -> None:
        ...

    @abstractmethod
    def parse_piece(self, piece_id: int) -> bool:
        ...

    @abstractmethod
    def get_piece(self, pos: Pos) -> Piece:
        ...

    @abstractmethod
    def process_piece(self, piece: Piece, opos: Pos, i: int, line: list[Pos], enemy: bool) -> bool:
        ...

    @abstractmethod
    def create_lines(
        self, piece: Piece, dirs: list[Pos], limit: int, attack_poss: list[Pos] | None = None
    ) -> list[Pos]:  
        ...

    @abstractmethod
    def get_moves(self, piece: Piece) -> list[Pos]:
        ...

    @abstractmethod
    def move(self, from_pos: Pos, to_pos: Pos) -> MoveData:
        ...

    @abstractmethod
    def create_board(self) -> list[list[int]]:
        ...


class BasePlayerType(ABC):
    id: int
    game: BaseGameType

    @abstractmethod
    def start(self, game: BaseGameType) -> None:
        ...


class BaseGameManagerType(ABC):
    games: list[BaseGameType]

    @abstractmethod
    def create_game(self) -> BaseGameType:
        ...
    
    @abstractmethod
    def get_game_by_id(self, id: int) -> BaseGameType:
        ...


class BasePlayerManagerType(ABC):
    players: list[BasePlayerType]

    @abstractmethod
    def create_player(self, id: int) -> BasePlayerType:
        ...

    @abstractmethod
    def get_player_by_id(self, id: int) -> BasePlayerType:
        ...
