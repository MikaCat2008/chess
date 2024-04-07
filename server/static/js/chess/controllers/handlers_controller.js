class HandlersController extends ListenersController {
    playerJoinedEvent(playerData) {
        let player = new Player(playerData.id);

        this.game.join(player);
    }

    gameStartedEvent(gameData) {
        this.game.start(gameData.board);
        this.applyBoard();
    }

    gameMoveEvent(possData) {
        if (this.game.side != this.getSide()) {
            let poss = this.parse(possData),
                fpos = this.board.ipos(poss[0]),
                tpos = this.board.ipos(poss[1]);

            if (this.board.getPiece(tpos) != undefined) {
                this.board.killPiece(tpos);
            }

            this.game.move(poss);
            this.board.movePiece([fpos, tpos]);
        }

        this.game.side = !this.game.side;
    }

    handleUpdate(update) {
        if (update.type == "player_joined") {
            this.playerJoinedEvent(update.player);
        }
        else if (update.type == "game_started") {
            this.gameStartedEvent(update.game);
        }
        else if (update.type == "game_move") {
            this.gameMoveEvent(update.poss);
        }
    }
}
