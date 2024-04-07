import typing as t, functools as ft
import flask as f

from .abstractions import GameManagerType, PlayerManagerType
from .api import api

auths = {
    "a": "a",
    "b": "b"
}

game_manager: GameManagerType = None
player_manager: PlayerManagerType = None


def index() -> f.Response:
    player = player_manager.get_player_by_username(f.request.cookies["username"])

    if player.game:
        return f.redirect("/chess")
    else:    
        return f.render_template(
            "index.html",
            player_id = player.id
        )


def chess() -> f.Response:
    player = player_manager.get_player_by_username(f.request.cookies["username"])

    if player.game:
        return f.render_template(
            "chess.html", 
            game_id = player.game.id,
            player_id = player.id,
        )
    else:
        return f.redirect("/")


def login() -> f.Response:
    return f.render_template("login.html")


def register() -> f.Response:
    return f.render_template("register.html")


def _login() -> f.Response:
    username = f.request.args["username"]
    password = f.request.args["password"]
    
    if check_auth(username, password):
        response = f.redirect("/")
        
        response.set_cookie("username", username)
        response.set_cookie("password", password)

        return response
    else:
        return f.jsonify({
            "status": "Login failed."
        })


def _register() -> f.Response:
    username = f.request.args["username"]
    password = f.request.args["password"]
    
    if username not in auths:    
        auths[username] = password
        player_manager.create_player(username)
    
        return f.redirect("/login")
    else:
        return f.jsonify({
            "status": "Register failed."
        })


def get_games() -> f.Response:
    return f.jsonify({
        "status": "ok",
        "data": {
            "games": [{
                "id": game.id,
                "players": [{
                    "id": player.id,
                    "username": player.username
                } for player in game.players]
            } for game in game_manager.games]
        }
    })


def load_game() -> f.Response:
    game_id = int(f.request.args["game_id"])
    
    game = game_manager.get_game_by_id(game_id)

    return f.jsonify({
        "status": "ok",
        "data": {
            "game": game.to_json()
        }
    })


def create_game() -> f.Response:
    game = game_manager.create_game()
    
    return f.jsonify({
        "status": "ok",
        "data": {
            "game": game.to_json()
        }
    })


def join_game() -> f.Response:
    game_id = int(f.request.args["game_id"])
    player_id = int(f.request.args["player_id"])

    game = game_manager.get_game_by_id(game_id)
    player = player_manager.get_player_by_id(player_id)

    if player not in game.players:
        game.join(player)

    return f.jsonify({
        "status": "ok",
        "data": {
            "game": game.to_json()
        }
    })


def game_move() -> f.Response:
    game_id = int(f.request.args["game_id"])
    player_id = int(f.request.args["player_id"])
    poss = f.request.args["poss"]
    from_pos, to_pos = [(int(pos[0]), int(pos[1])) for pos in poss.split(";")]
    
    game = game_manager.get_game_by_id(game_id)
    player = player_manager.get_player_by_id(player_id)

    message = game.move(player, from_pos, to_pos)
    
    if message == "ok":
        for _player in game.players:
            api.game_move_event(_player, poss)

    return f.jsonify({
        "status": "ok",
        "data": {
            "message": message,
        }
    })


def get_updates() -> f.Response:
    player_id = int(f.request.args["player_id"])
    
    return f.jsonify({
        "status": "ok",
        "data": {
            "updates": api.get_updates(player_id)
        }
    })


def check_auth(username: str, password: str) -> bool:
    return None not in [username, password] and auths.get(username) == password


def check_auth_cookies(cookies: dict) -> bool:
    username = cookies.get("username")
    password = cookies.get("password")

    return check_auth(username, password)


def auth_route(app: f.Flask, url: str) -> t.Callable:
    def route(handler: t.Callable) -> None:
        @ft.wraps(handler)
        def wrapped_handler() -> f.Response:
            if check_auth_cookies(f.request.cookies):
                return handler()
            else:
                return f.redirect("/login")
        
        app.route(url)(wrapped_handler)

    return route


def init(app: f.Flask, _game_manager: GameManagerType, _player_manager: PlayerManagerType) -> None:
    global game_manager, player_manager

    game_manager = _game_manager
    player_manager = _player_manager

    app.route("/login")(login)
    app.route("/register")(register)
    app.route("/api/login")(_login)
    app.route("/api/register")(_register)
    auth_route(app, "/")(index)
    auth_route(app, "/chess")(chess)
    auth_route(app, "/api/get_games")(get_games)
    auth_route(app, "/api/load_game")(load_game)
    auth_route(app, "/api/create_game")(create_game)
    auth_route(app, "/api/join_game")(join_game)
    auth_route(app, "/api/game_move")(game_move)
    auth_route(app, "/api/get_updates")(get_updates)

    for username in auths:
        player_manager.create_player(username)
