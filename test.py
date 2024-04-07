import unittest

from sdk import BaseGame


class TestGameLogic(unittest.TestCase):
    def test_pawn_moves(self) -> None:
        game = BaseGame(0)
        game.create_board([
            [ 0,  0,  1,  1,  0,  0,  0,  0],
            [ 1,  7,  0,  7,  7,  0,  0,  0],
            [ 0,  1,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 1,  1,  0,  0,  0,  0,  0,  0],
            [ 7,  7,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  0]
        ])
        
        self.assertEqual(game.get_moves(game.get_piece((0, 1))), [
            (0, 2), (0, 3)
        ])
        self.assertEqual(game.get_moves(game.get_piece((1, 2))), [
            (1, 3)
        ])
        self.assertEqual(game.get_moves(game.get_piece((2, 0))), [
            (2, 1), (1, 1), (3, 1)
        ])
        self.assertEqual(game.get_moves(game.get_piece((3, 0))), [
            (4, 1)
        ])
        self.assertEqual(game.get_moves(game.get_piece((0, 4))), [
            (1, 5)
        ])

    def test_rock_moves(self) -> None:
        game = BaseGame(0)
        game.create_board([
            [ 0,  0,  0,  0,  0,  1,  0,  0],
            [ 0,  2,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  7,  0,  0,  0,  0],
            [ 7,  0,  0,  2,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  1,  0,  0,  2,  7,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  7,  0,  0,  0,  0]
        ])
        
        self.assertEqual(game.get_moves(game.get_piece((1, 1))), [
            (1, 2), (1, 3), (1, 4), (1, 5), 
            (1, 6), (1, 7), (2, 1), (3, 1), 
            (4, 1), (5, 1), (6, 1), (7, 1), 
            (1, 0), (0, 1)
        ])
        self.assertEqual(game.get_moves(game.get_piece((3, 3))), [
            (3, 4), (3, 5), (3, 6), (3, 7), 
            (4, 3), (5, 3), (6, 3), (7, 3), 
            (3, 2), (2, 3), (1, 3), (0, 3)
        ])
        self.assertEqual(game.get_moves(game.get_piece((5, 5))), [
            (5, 6), (5, 7), (6, 5), (5, 4), 
            (5, 3), (5, 2), (5, 1), (4, 5), 
            (3, 5)
        ])

    def test_knight_moves(self) -> None:
        game = BaseGame(0)
        game.create_board([
            [ 0,  0,  0,  7,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  1,  0,  0,  0],
            [ 0,  0,  3,  0,  0,  0,  0,  0],
            [ 1,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  1,  0,  7,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  0]
        ])
        
        self.assertEqual(game.get_moves(game.get_piece((2, 2))), [
            (3, 4), (4, 3), (3, 0), (1, 0), 
            (0, 1)
        ])

    def test_bishop_moves(self) -> None:
        game = BaseGame(0)
        game.create_board([
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  7,  0,  1,  0,  0],
            [ 7,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  4,  0,  4,  0,  4,  0,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  7,  0,  1,  0,  0,  0,  1],
            [ 0,  0,  0,  0,  0,  0,  7,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  0]
        ])
        
        self.assertEqual(game.get_moves(game.get_piece((1, 3))), [
            (2, 4), (2, 2), (3, 1), (0, 2), 
            (0, 4)
        ])
        self.assertEqual(game.get_moves(game.get_piece((3, 3))), [
            (4, 4), (5, 5), (6, 6), (4, 2), 
            (2, 2), (1, 1), (0, 0), (2, 4), 
            (1, 5)
        ])
        self.assertEqual(game.get_moves(game.get_piece((5, 3))), [
            (6, 4), (6, 2), (7, 1), (4, 2), 
            (3, 1), (4, 4)
        ])

    def test_queen(self) -> None:
        game = BaseGame(0)
        game.create_board([
            [ 1,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  1,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  7,  0,  5,  0,  7,  0,  0],
            [ 0,  0,  0,  0,  7,  0,  0,  0],
            [ 0,  1,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  1,  0,  0,  0,  0]
        ])

        self.assertEqual(game.get_moves(game.get_piece((3, 3))), [
            (3, 4), (3, 5), (3, 6), (4, 3), 
            (5, 3), (3, 2), (2, 3), (1, 3), 
            (4, 4), (4, 2), (5, 1), (6, 0), 
            (2, 2), (1, 1), (2, 4)
        ])


if __name__ == "__main__":
    unittest.main()
