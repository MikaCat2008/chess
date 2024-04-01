class BaseGame {
    constructor (id, side, board, players, player) {
        this.id = id;
        this.side = side;
        this.board = board;
        this.players = players;

        this.player = player;
    }

    join(player) {
        this.players.push(player);
    }

    start(side, board) {
        this.side = side;
        this.board = board;
    }

    parse_piece(piece_id) {
        piece_id -= 1;

        return [Math.floor(piece_id / 6), piece_id % 6];
    }

    get_piece(pos) {
        let [x, y] = pos;
        
        if (x < 0 || y < 0 || x > 7 || y > 7) {
            return undefined;
        }
        
        let [piece_side, piece_id] = this.parse_piece(this.board[y][x]);
        
        return [piece_side, piece_id, pos];
    }

    process_piece(piece, opos, i, line, enemy, kill) {
        let [piece_side, _, piece_pos] = piece;
        let [x, y] = piece_pos;
        let [ox, oy] = opos;

        if (piece_side) {
            oy *= -1;
        }

        let ix = x + ox * i, iy = y + oy * i;
        let ipiece = this.get_piece([ix, iy]);

        if (ipiece == undefined) {
            return true;
        }

        let ipiece_side = ipiece[0];

        if (ipiece_side != -1) {
            if (ipiece_side != piece_side && kill) {
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

    create_lines(piece, dirs, limit, kill = true) {
        let line = [];

        dirs.forEach(dir => {
            for (let i = 1; i < limit + 1; i++) {
                if (!this.process_piece(piece, dir, i, line, false, kill)) {
                    break;
                }
            }
        })

        return line;
    }

    create_pawn_attacks(piece) {
        let poss = [];

        [[-1, 1], [1, 1]].forEach(pos => {
            this.process_piece(piece, pos, 1, poss, true, true)
        });

        return poss;
    }

    get_moves(piece) {
        let [piece_side, piece_id, piece_pos] = piece;
        let [_, y] = piece_pos;

        if (piece_id == 0) {
            return this.create_lines(piece, [
                [ 0,  1]
            ], (piece_side ? y == 6 : y == 1) + 1, false).concat(this.create_pawn_attacks(piece));
        }
        else if (piece_id == 1) {
            return this.create_lines(piece, [
                [ 0,  1], [ 1,  0], [ 0, -1], [-1, 0]
            ], 7);
        }
        else if (piece_id == 2) {
            return this.create_lines(piece, [
                [ 1,  2], [ 2,  1], [ 2, -1], [ 1, -2], 
                [-1, -2], [-2, -1], [-2,  1], [-1,  2]
            ], 1);
        }
        else if (piece_id == 3) {
            return this.create_lines(piece, [
                [ 1,  1], [ 1, -1], [-1, -1], [-1,  1]
            ], 7);
        }
        else if (piece_id == 4) {
            return this.create_lines(piece, [
                [ 0,  1], [ 1,  0], [ 0, -1], [-1,  0],
                [ 1,  1], [ 1, -1], [-1, -1], [-1,  1]
            ], 7);
        }
        else if (piece_id == 5) {
            return this.create_lines(piece, [
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

    static parse(poss) {
        let [from_pos, to_pos] = poss.split(";");

        let fx = Number(from_pos[0]);
        let fy = Number(from_pos[1]);
        let tx = Number(to_pos[0]);
        let ty = Number(to_pos[1]);

        return [[fx, fy], [tx, ty]];
    }

    static format(poss) {
        let [[fx, fy], [tx, ty]] = poss;
        
        return `${fx}${fy};${tx}${ty}`;
    }
}


class BasePlayer {
    constructor (id, game) {
        this.id = id;
        this.game = game;
        this.side = undefined;
    }

    async createGame() {        
        await api("create_game");
    }

    async joinGame(gameId) {
        let data = (await (await api("join_game", {
            game_id: gameId,
            player_id: this.id
        })).json()).data;

        let players = []
        data.game.players.forEach(_player => {
            let player;
            
            if (this.id == _player.id) {
                player = this;
            }
            else {
                player = new Player(_player.id, this.game);
            }

            players.push(player);
        });

        let game = new Game(
            data.game.id, data.game.side, data.game.board, players, this
        );

        this.game = game;

        return game;
    }

    async gameMove(poss) {
        let data = (await (await api("game_move", {
            game_id: this.game.id,
            player_id: this.id,
            poss: Game.format(poss)
        })).json()).data;

        return data.message;
    }
    
    async getUpdates() {
        await api("get_updates", {
            player_id: this.id
        }).then(async response => {
            let updates = (await response.json()).data.updates;

            updates.forEach(update => {
                let type = update.type;

                if (type == "player_joined") {
                    let player = new Player(
                        update.player.id, this.game
                    );
                    
                    this.game.join(player);
                }
                else if (type == "game_start") {
                    this.side = this.game.players[Number(update.game.side)] == this;

                    this.game.start(update.game.side, update.game.board);
                }
                else if (type == "game_move") {                    
                    this.game.move(Game.parse(update.poss))
                }
            });
        }) 
    }
}


class Game extends BaseGame {
    constructor (id, side, board, players, player) {
        super(id, side, board, players, player);

        this.boardElement = document.querySelector(".game-board");
        this.cellElements = document.querySelectorAll(".game-cell");
    }

    start(side, board) {
        super.start(side, board);

        for (let y = 0; y < 8; y++) {        
            for (let x = 0; x < 8; x++) {
                this.setPiece([x, y], board[y][x]);
            }
        }
    }

    move(poss) {
        let pieceId = this.board[poss[0][1]][poss[0][0]];

        this.setPiece(poss[1], pieceId);
        this.setPiece(poss[0], 0);

        super.move(poss);
    }

    setPiece(pos, pieceId) {
        let [x, y] = pos;

        if (this.player.side) {
            y = 7 - y;
        }

        if (pieceId == 0) {
            this.cellElements[y * 8 + x].innerHTML = ``;
        }
        else {
            this.cellElements[y * 8 + x].innerHTML = `<img src="static/media/${pieceId - 1}.png" />`;
        }
    }
}


class Player extends BasePlayer {}


let player = new Player(player_id);
let selectedPiece, placeElements = [];

document.querySelectorAll(".game-cell").forEach((element, index) => {
    element.onclick = async event => {    
        let x = index % 8, y = Math.floor(index / 8);

        if (player.side) {
            y = 7 - y;
        }
        
        if (selectedPiece) {
            let [fromElement, fpos] = selectedPiece;

            if (fromElement != element) {
                if (player.game.get_moves(player.game.get_piece(fpos)).some(pos => {
                    return pos[0] == x && pos[1] == y;
                })) {
                    console.log(await player.gameMove([fpos, [x, y]]));
                }
            }

            fromElement.classList.remove("selected");
            selectedPiece = undefined;

            placeElements.forEach(cellElement => {
                cellElement.classList.remove("place");
            });
            placeElements = [];
        }
        else {
            selectedPiece = [element, [x, y]];
            
            player.game.get_moves(player.game.get_piece([x, y])).forEach(pos => {
                let [px, py] = pos;

                if (player.side) {
                    py = 7 - py;
                }
                
                let cellElement = player.game.cellElements[py * 8 + px];
                cellElement.classList.add("place");
                placeElements.push(cellElement);
            })

            element.classList.add("selected");
        }
    }
})

setInterval(async () => {
    await player.getUpdates();
}, 500);
