from .abstractions import (
    Pos, Piece, MoveData, BaseGameType, BasePlayerType, BaseGameManagerType, BasePlayerManagerType
)


class MoveError(BaseException): ...


class BaseGame(BaseGameType):
    def __init__(self, id: int) -> None:
        self.id = id
        self.side = None
        self.players = []

    def join(self, player: BasePlayerType) -> None:
        self.players.append(player)

    def start(self) -> None:
        self.side = False

        self.create_board()

    def parse_piece(self, piece_id: int) -> bool:
        return divmod(piece_id - 1, 6)

    def get_piece(self, pos: Pos) -> Piece:
        x, y = pos
        
        if x < 0 or y < 0 or x > 7 or y > 7:
            return None
        
        piece_side, piece_id = self.parse_piece(self.board[y][x])
        
        return piece_side, piece_id, pos

    def process_piece(self, piece: Piece, opos: Pos, i: int, line: list[Pos], enemy: bool) -> bool:
        piece_side, _, piece_pos = piece
        x, y = piece_pos
        ox, oy = opos

        if not piece_side:
            oy *= -1

        ix, iy = x + ox * i, y + oy * i
        ipiece = self.get_piece((ix, iy))

        if ipiece is None:
            return False

        ipiece_side = ipiece[0]

        if ipiece_side != -1:
            if ipiece_side != piece_side and enemy:
                line.append((ix, iy))
            
            return False
        if enemy:
            return True

        line.append((ix, iy))

        return True

    def create_lines(
        self, piece: Piece, dirs: list[Pos], limit: int, attack_poss: list[Pos] | None = None
    ) -> list[Pos]:        
        line = []

        for dir in dirs:
            for i in range(1, limit + 1):
                if not self.process_piece(piece, dir, i, line, attack_poss is None):
                    break

        if attack_poss:
            for apos in attack_poss:
                self.process_piece(piece, apos, 1, line, True)

        return line

    def get_moves(self, piece: Piece) -> list[Pos]:
        piece_side, piece_id, piece_pos = piece
        _, y = piece_pos

        if piece_id == 0:
            return self.create_lines(piece, [
                ( 0,  1)
            ], (y == 1 if piece_side else y == 6) + 1, [
                (-1,  1), ( 1,  1)
            ])
        elif piece_id == 1:
            return self.create_lines(piece, [
                ( 0,  1), ( 1,  0), ( 0, -1), (-1, 0)
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
            ], 7)

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
            raise MoveError(f"Can't move from x={fx}, y={fy} to x={tx}, y={ty}.")

        self.side = not self.side
        self.board[ty][tx] = self.board[fy][fx]
        self.board[fy][fx] = 0

    def create_board(self) -> list[list[int]]:
        self.board = [
            [ 8,  9, 10, 11, 12, 10,  9,  8],
            [ 7,  7,  7,  7,  7,  7,  7,  7],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 1,  1,  1,  1,  1,  1,  1,  1],
            [ 2,  3,  4,  5,  6,  4,  3,  2]
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
        self.games = {}


class BasePlayerManager(BasePlayerManagerType):
    def __init__(self) -> None:
        self.players = {}
