from __future__ import annotations

import collections as c, flask as f, sdk

app = f.Flask(__name__)


class GameType(sdk.BaseGameType):
    players: list[PlayerType]

    def to_json(self) -> dict:
        ...


class PlayerType(sdk.BasePlayerType):
    def to_json(self) -> dict:
        ...


class GameManagerType(sdk.BaseGameManagerType):
    games: list[GameType]
    
    def to_json(self) -> dict:
        ...


class PlayerManagerType(sdk.BasePlayerManagerType):
    players: list[PlayerType]

    def to_json(self) -> dict:
        ...


class Game(sdk.BaseGame, GameType):    
    def join(self, player: PlayerType) -> None:
        for _player in self.players:
            updates[_player.id].append({
                "type": "player_joined",
                "player": player.to_json()
            })

        super().join(player)

        if len(self.players) == 2:
            self.start()

    def start(self) -> None:
        super().start()
        
        for player in self.players:
            updates[player.id].append({
                "type": "game_start",
                "game": self.to_json()
            })

    def move(self, player: PlayerType, poss: str) -> str:
        if player is not self.players[self.side]:
            return "Other step."
        
        try:
            from_pos, to_pos = poss.split(";")

            super().move(
                tuple(map(int, from_pos)), tuple(map(int, to_pos))
            )

            message = "ok"
        except sdk.MoveError as error:
            message = error.args[0]
        
        if message == "ok":
            for player in self.players:
                updates[player.id].append({
                    "type": "game_move",
                    "poss": poss
                })
            
        return message

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "players": [player.to_json() for player in self.players]
        }


class Player(sdk.BasePlayer, PlayerType):
    def to_json(self) -> dict:
        return {
            "id": self.id
        }


class GameManager(sdk.BaseGameManager, GameManagerType):
    def create_game(self) -> GameType:
        game = Game(len(self.games))
        
        self.games[game.id] = game

        return game


class PlayerManager(sdk.BasePlayerManager, PlayerManagerType):
    def create_player(self) -> PlayerType:
        player = Player(len(self.players))
        
        self.players[player.id] = player

        return player


@app.route("/api/create_game")
def create_game() -> f.Response:
    game = game_manager.create_game()
    
    return f.jsonify({
        "status": "ok",
        "data": {
            "game": game.to_json()
        }
    })


@app.route("/api/create_player")
def create_player() -> f.Response:
    player = player_manager.create_player()
    
    return f.jsonify({
        "status": "ok",
        "data": {
            "player": player.to_json()
        }
    })


@app.route("/api/join_game")
def join_game() -> f.Response:
    game_id = int(f.request.args["game_id"])
    player_id = int(f.request.args["player_id"])

    game = game_manager.games[game_id]
    player = player_manager.players[player_id]

    game.join(player)

    return f.jsonify({
        "status": "ok",
        "data": {
            "game": game.to_json()
        }
    })


@app.route("/api/game_move")
def game_move() -> f.Response:
    game_id = int(f.request.args["game_id"])
    player_id = int(f.request.args["player_id"])
    poss = f.request.args["poss"]
    
    game = game_manager.games[game_id]
    player = player_manager.players[player_id]

    message = game.move(player, poss)
    
    return f.jsonify({
        "status": "ok",
        "data": {
            "message": message,
        }
    })


@app.route("/api/load_game")
def load_game() -> f.Response:
    game_id = int(f.request.args["game_id"])
    
    game = game_manager.games[game_id]

    return f.jsonify({
        "status": "ok",
        "data": {
            "game": {
                **game.to_json(),
                "board": game.board
            }
        }
    })


@app.route("/api/get_updates")
def get_updates() -> f.Response:
    player_id = int(f.request.args["player_id"])

    _updates = updates[player_id]

    updates[player_id] = []
    
    return f.jsonify({
        "status": "ok",
        "data": {
            "updates": _updates
        }
    })


updates = c.defaultdict(list)
game_manager = GameManager()
player_manager = PlayerManager()
