class ListenersController extends ChessController {
    canUpPiece(piece) {
        let side = this.getSide();

        return piece.side == side && this.game.side == side;
    }

    upPiece(piece) {
        let moves = this.game.getMoves([piece.side, piece.id, piece.pos]);
    
        this.board.select(piece.pos, moves);
    }

    canDownPiece(pos, piece) {
        this.board.unselect();

        let moves = this.game.getMoves([piece.side, piece.id, piece.pos]);

        return moves.some(move => move[0] == pos[0] && move[1] == pos[1]);
    }

    downPiece(pos, piece) {
        let poss = [piece.pos, pos];
        pos = this.board.ipos(pos);
        
        if (this.board.getPiece(pos) != undefined) {
            this.board.killPiece(pos);
        }

        this.game.move(poss);
        this.gameMove(poss);
    }

    setBoardListeners() {
        this.board.on("canUpPiece", piece => this.canUpPiece(piece));
        this.board.on("upPiece", piece => this.upPiece(piece));
        this.board.on("canDownPiece", (pos, piece) => this.canDownPiece(pos, piece));
        this.board.on("downPiece", (pos, piece) => this.downPiece(pos, piece));
    }

    applyBoard() {
        if (this.board.applied) {
            return;
        }

        if (!this.getSide()) {
            this.board.inverse();
        }

        this.board.apply(this.game.board);
        this.setBoardListeners();
    }
}
