class ChessController {
    constructor (board, player) {
        this.game = undefined;
        this.board = board;
        this.player = player;
    }

    setGame(gameData) {
        this.game = new Game(
            gameData.id, 
            gameData.started, 
            gameData.players, 
            gameData.side, 
            gameData.board
        );
    }

    getSide() {
        return Number(this.player.id != this.game.players[0].id);
    }

    parse(poss) {
        let [fromPos, toPos] = poss.split(";");

        let fx = Number(fromPos[0]);
        let fy = Number(fromPos[1]);
        let tx = Number(toPos[0]);
        let ty = Number(toPos[1]);

        return [[fx, fy], [tx, ty]];
    }

    format(poss) {
        let [[fx, fy], [tx, ty]] = poss;
        
        return `${fx}${fy};${tx}${ty}`;
    }
}
