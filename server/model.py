from sdk import MoveError, BaseGame, BasePlayer, BaseGameManager, BasePlayerManager
from .abstractions import GameType, PlayerType, GameManagerType, PlayerManagerType
from .api import api


class Game(BaseGame, GameType):    
    def join(self, player: PlayerType) -> None:
        for _player in self.players:
            api.player_joined_event(_player, player)

        super().join(player)

        if len(self.players) == 2:
            self.start()

    def start(self) -> None:
        super().start()
        
        for player in self.players:
            api.game_started_event(player, self)

    def move(self, player: PlayerType, from_pos: tuple[int, int], to_pos: tuple[int, int]) -> str:
        if player is not self.players[self.side]:
            return "Other step."
        
        try:
            super().move(from_pos, to_pos)

            message = "ok"
        except MoveError as error:
            message = error.args[0]
            
        return message

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "side": self.side,
            "board": self.board,
            "started": self.started,
            "players": [player.to_json() for player in self.players]
        }


class Player(BasePlayer, PlayerType):
    def __init__(self, id: int, username: str) -> None:
        super().__init__(id)

        self.username = username

    def to_json(self) -> dict:
        return {
            "id": self.id
        }


class GameManager(BaseGameManager, GameManagerType):
    def create_game(self) -> GameType:
        game = Game(len(self.games))
        
        self.games.append(game)

        return game

    def get_game_by_id(self, id: int) -> GameType:
        return super().get_game_by_id(id)


class PlayerManager(BasePlayerManager, PlayerManagerType):
    def create_player(self, username: str) -> PlayerType:
        player = Player(len(self.players), username)
        
        self.players.append(player)

        return player

    def get_player_by_id(self, id: int) -> PlayerType:
        return super().get_player_by_id(id)

    def get_player_by_username(self, username: str) -> PlayerType:
        player = [player for player in self.players if player.username == username]
        
        if len(player) == 1:
            return player[0]
        else:
            return None
