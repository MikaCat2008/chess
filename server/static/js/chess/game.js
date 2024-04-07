class Game extends BaseGame {
    constructor (id, started, players, side, board) {
        super(id, started, players);
        
        this.side = side;
        this.board = board;
    }

    join(player) {
        this.players.push(player);
    }

    start(board) {
        super.start();

        this.side = false;
        this.board = board;
    }

    getPiece(pos) {
        let [x, y] = pos;
        
        if (x < 0 || y < 0 || x > 7 || y > 7) {
            return undefined;
        }
        
        let [pieceSide, pieceId] = this.parsePiece(this.board[y][x]);
        
        return [pieceSide, pieceId, pos];
    }

    processPiece(piece, opos, i, line, enemy, kill) {
        let [pieceSide, _, piecePos] = piece;
        let [x, y] = piecePos;
        let [ox, oy] = opos;

        if (pieceSide) {
            oy *= -1;
        }

        let ix = x + ox * i, iy = y + oy * i;
        let ipiece = this.getPiece([ix, iy]);

        if (ipiece == undefined) {
            return true;
        }

        let ipieceSide = ipiece[0];

        if (ipieceSide != -1) {
            if (ipieceSide != pieceSide && kill) {
                line.push([ix, iy]);
            }
            
            return false;
        }
        if (enemy) {
            return true;
        }

        line.push([ix, iy]);

        return true;
    }

    createLines(piece, dirs, limit, kill = true) {
        let line = [];

        dirs.forEach(dir => {
            for (let i = 1; i < limit + 1; i++) {
                if (!this.processPiece(piece, dir, i, line, false, kill)) {
                    break;
                }
            }
        })

        return line;
    }

    createPawnAttacks(piece) {
        let poss = [];

        [[-1, 1], [1, 1]].forEach(pos => {
            this.processPiece(piece, pos, 1, poss, true, true);
        });

        return poss;
    }

    getMoves(piece) {
        let [pieceSide, pieceId, piecePos] = piece;
        let [_, y] = piecePos;

        if (pieceId == 0) {
            return this.createLines(piece, [
                [ 0,  1]
            ], (pieceSide ? y == 6 : y == 1) + 1, false).concat(this.createPawnAttacks(piece));
        }
        else if (pieceId == 1) {
            return this.createLines(piece, [
                [ 0,  1], [ 1,  0], [ 0, -1], [-1, 0]
            ], 7);
        }
        else if (pieceId == 2) {
            return this.createLines(piece, [
                [ 1,  2], [ 2,  1], [ 2, -1], [ 1, -2], 
                [-1, -2], [-2, -1], [-2,  1], [-1,  2]
            ], 1);
        }
        else if (pieceId == 3) {
            return this.createLines(piece, [
                [ 1,  1], [ 1, -1], [-1, -1], [-1,  1]
            ], 7);
        }
        else if (pieceId == 4) {
            return this.createLines(piece, [
                [ 0,  1], [ 1,  0], [ 0, -1], [-1,  0],
                [ 1,  1], [ 1, -1], [-1, -1], [-1,  1]
            ], 7);
        }
        else if (pieceId == 5) {
            return this.createLines(piece, [
                [ 0,  1], [ 1,  1], [ 1,  0], [ 1, -1],
                [ 0, -1], [-1, -1], [-1,  0], [-1,  1]
            ], 1);
        }
    }

    move(poss) {
        let [[fx, fy], [tx, ty]] = poss;

        this.board[ty][tx] = this.board[fy][fx];
        this.board[fy][fx] = 0;
    }

    parsePiece(pieceId) {
        pieceId -= 1;

        return [Math.floor(pieceId / 6), pieceId % 6];
    }
}
