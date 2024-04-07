from .abstractions import (
    Pos, Piece, MoveData, BaseGameType, BasePlayerType, BaseGameManagerType, BasePlayerManagerType
)


class MoveError(BaseException): ...


class BaseGame(BaseGameType):
    def __init__(self, id: int) -> None:
        self.id = id
        self.side = None
        self.board = None
        self.started = False
        self.players = []

    def join(self, player: BasePlayerType) -> None:
        player.game = self
        
        self.players.append(player)

    def start(self) -> None:
        self.side = False
        self.started = True

        self.create_board()

    def parse_piece(self, piece_id: int) -> bool:
        return divmod(piece_id - 1, 6)

    def get_piece(self, pos: Pos) -> Piece:
        x, y = pos
        
        if x < 0 or y < 0 or x > 7 or y > 7:
            return None
        
        piece_side, piece_id = self.parse_piece(self.board[y][x])
        
        return piece_side, piece_id, pos

    def process_piece(
        self, piece: Piece, opos: Pos, i: int, line: list[Pos], enemy: bool, kill: bool
    ) -> bool:
        piece_side, _, piece_pos = piece
        x, y = piece_pos
        ox, oy = opos

        if piece_side:
            oy *= -1

        ix, iy = x + ox * i, y + oy * i
        ipiece = self.get_piece((ix, iy))

        if ipiece is None:
            return False

        ipiece_side = ipiece[0]

        if ipiece_side != -1:
            if ipiece_side != piece_side and kill:
                line.append((ix, iy))
            
            return False
        if enemy:
            return True    
            
        line.append((ix, iy))

        return True

    def create_lines(self, piece: Piece, dirs: list[Pos], limit: int, kill: bool = True) -> list[Pos]:        
        line = []

        for dir in dirs:
            for i in range(1, limit + 1):
                if not self.process_piece(piece, dir, i, line, False, kill):
                    break

        return line
    
    def create_pawn_attacks(self, piece: Piece) -> list[Pos]:
        poss = []

        for pos in [(-1, 1), (1, 1)]:
            self.process_piece(piece, pos, 1, poss, True, True)

        return poss

    def get_moves(self, piece: Piece) -> list[Pos]:
        piece_side, piece_id, piece_pos = piece
        _, y = piece_pos

        if piece_id == 0:
            return self.create_lines(piece, [
                ( 0,  1)
            ], (y == 6 if piece_side else y == 1) + 1, False) + self.create_pawn_attacks(piece)
        elif piece_id == 1:
            return self.create_lines(piece, [
                ( 0,  1), ( 1,  0), ( 0, -1), (-1,  0)
            ], 7)
        elif piece_id == 2:
            return self.create_lines(piece, [
                ( 1,  2), ( 2,  1), ( 2, -1), ( 1, -2), 
                (-1, -2), (-2, -1), (-2,  1), (-1,  2)
            ], 1)
        elif piece_id == 3:
            return self.create_lines(piece, [
                ( 1,  1), ( 1, -1), (-1, -1), (-1,  1)
            ], 7)
        elif piece_id == 4:
            return self.create_lines(piece, [
                ( 0,  1), ( 1,  0), ( 0, -1), (-1,  0),
                ( 1,  1), ( 1, -1), (-1, -1), (-1,  1)
            ], 7)
        elif piece_id == 5:
            return self.create_lines(piece, [
                ( 0,  1), ( 1,  1), ( 1,  0), ( 1, -1),
                ( 0, -1), (-1, -1), (-1,  0), (-1,  1)
            ], 1)

    def move(self, from_pos: Pos, to_pos: Pos) -> MoveData:
        fx, fy = from_pos
        tx, ty = to_pos

        if fx < 0 or fy < 0 or fx > 7 or fy > 7:
            raise MoveError(f"From position x={fx}, y={fy} is out of range.")
        
        if tx < 0 or ty < 0 or tx > 7 or ty > 7:
            raise MoveError(f"To position x={tx}, y={ty} is out of range.")

        from_piece = self.get_piece(from_pos)
        to_piece = self.get_piece(to_pos)
        
        if from_piece[0] == -1:
            raise MoveError("Empty cell can't move.")

        if from_piece[0] != self.side:
            raise MoveError("Other step.")

        if from_piece[0] == to_piece[0]:
            raise MoveError("Sides can't be same.")

        if to_pos not in self.get_moves(from_piece):
            print(from_piece, self.get_moves(from_piece))

            raise MoveError(f"Can't move from x={fx}, y={fy} to x={tx}, y={ty}.")

        self.side = not self.side
        self.board[ty][tx] = self.board[fy][fx]
        self.board[fy][fx] = 0

    def create_board(self, board: list[list[int]] | None = None) -> list[list[int]]:
        if board:
            self.board = board
        else:
            self.board = [
                [ 2,  3,  4,  5,  6,  4,  3,  2],
                [ 1,  1,  1,  1,  1,  1,  1,  1],
                [ 0,  0,  0,  0,  0,  0,  0,  0],
                [ 0,  0,  0,  0,  0,  0,  0,  0],
                [ 0,  0,  0,  0,  0,  0,  0,  0],
                [ 0,  0,  0,  0,  0,  0,  0,  0],
                [ 7,  7,  7,  7,  7,  7,  7,  7],
                [ 8,  9, 10, 11, 12, 10,  9,  8]
            ]

        return self.board


class BasePlayer(BasePlayerType):
    def __init__(self, id: int) -> None:
        self.id = id
        self.game = None

    def start(self, game: BaseGameType) -> None:
        self.game = game


class BaseGameManager(BaseGameManagerType):
    def __init__(self) -> None:
        self.games = []

    def get_game_by_id(self, id: int) -> BaseGameType:
        return [game for game in self.games if game.id == id][0]


class BasePlayerManager(BasePlayerManagerType):
    def __init__(self) -> None:
        self.players = []

    def get_player_by_id(self, id: int) -> BasePlayerType:
        return [player for player in self.players if player.id == id][0]
