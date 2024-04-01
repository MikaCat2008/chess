import flask as f

from . import routers
from .model import GameManager, PlayerManager

app = f.Flask(__name__)

game_manager = GameManager()
player_manager = PlayerManager()

routers.init(app, game_manager, player_manager)
