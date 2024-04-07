from collections import defaultdict

from .abstractions import GameType, PlayerType


class Api:
    updates: defaultdict[list]

    def __init__(self) -> None:
        self.updates = defaultdict(list)

    def emit(self, player: PlayerType, event: str, data: dict) -> None:
        self.updates[player.id].append({
            "type": event, **data
        })

    def get_updates(self, id: int) -> list[dict]:
        updates = self.updates[id]

        self.updates[id] = []
        
        return updates

    def player_joined_event(self, player: PlayerType, joined_player: PlayerType) -> None:
        self.emit(player, "player_joined", {
            "player": joined_player.to_json()
        })

    def game_started_event(self, player: PlayerType, game: GameType) -> None:
        self.emit(player, "game_started", {
            "game": game.to_json()
        })

    def game_move_event(self, player: PlayerType, poss: str) -> None:
        self.emit(player, "game_move", {
            "poss": poss
        })


api = Api()
