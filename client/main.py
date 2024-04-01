import requests

api = "http://localhost:8080/api/"


def join_game(game_id: int, player_id: int) -> dict:
    return requests.get(
        api + f"join_game?game_id={game_id}&player_id={player_id}"
    ).json()["data"]


def game_move(game_id: int, player_id: int, poss: str) -> dict:
    return requests.get(
        api + f"game_move?game_id={game_id}&player_id={player_id}&poss={poss}"
    ).json()["data"]


requests.get("http://localhost:8080/api/create_game")

requests.get("http://localhost:8080/api/create_player")
requests.get("http://localhost:8080/api/create_player")

join_game(0, 0)
join_game(0, 1)

game_move(0, 0, "01;03")
game_move(0, 1, "06;04")
