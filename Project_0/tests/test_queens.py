# test_queens.py
#
# ICS 33 Winter 2023
# Project 0: History of Modern
#
# Unit tests for the QueensState class in "queens.py".
#
# Docstrings are not required in your unit tests, though each test does need to have
# a name that clearly indicates its purpose.  Notice, for example, that the provided
# test method is named "test_zero_queen_count_initially" instead of something generic
# like "test_queen_count", since it doesn't entirely test the "queen_count" method,
# but instead focuses on just one aspect of how it behaves.  You'll want to do likewise.

from queens import *
import unittest



class TestQueensState(unittest.TestCase):
    def test_zero_queen_count_initially(self):
        state = QueensState(8, 8)
        self.assertEqual(state.queen_count(), 0)

    def test_initial_board_size(self):
        state = QueensState(8, 8)
        self.assertEqual(8, len(state._board))
        self.assertEqual(8, len(state._board[0]))
        for i in range(8):
            for j in range(8):
                self.assertEqual(0, state._board[i][j])

    def test_negative_initial_board_size(self):
        with self.assertRaises(ValueError):
            state = QueensState(-1, 1)
        with self.assertRaises(ValueError):
            state = QueensState(1, -1)

    def test_queen_count(self):
        state = QueensState(8, 8)
        for i in range(7):
            state._board[i][3] = 1
        self.assertEqual(state.queen_count(), 7)

    def test_row_and_column_attributes(self):
        state = QueensState(1,4)
        self.assertEqual(1, state._rows)
        self.assertEqual(4, state._columns)

    def test_queens_location_list(self):
        state = QueensState(8,4)
        state._board[0][3] = 1
        state._board[3][0] = 1
        state._board[7][1] = 1
        locations = state.queens()
        self.assertEqual(3, len(locations))
        self.assertEqual(0, locations[0].row)
        self.assertEqual(3, locations[0].column)
        self.assertEqual(3, locations[1].row)
        self.assertEqual(0, locations[1].column)
        self.assertEqual(7, locations[2].row)
        self.assertEqual(1, locations[2].column)

    def test_has_queen(self):
        state = QueensState(8,8)
        state._board[0][0] = 1
        self.assertTrue(state.has_queen(Position(0,0)))
        self.assertFalse(state.has_queen(Position(1,0)))
        self.assertFalse(state.has_queen(Position(9, 0)))
        self.assertFalse(state.has_queen(Position(-1, 0)))
        self.assertFalse(state.has_queen(Position(0, -1)))

    def test_horizontal_unsafe(self):
        state = QueensState(8,8)
        state._board[0][0] = 1
        state._board[0][7] = 1
        self.assertTrue(state._check_horizontal_unsafe(0))
        self.assertFalse(state._check_horizontal_unsafe(1))

    def test_vertical_unsafe(self):
        state = QueensState(8,8)
        state._board[0][0] = 1
        state._board[7][0] = 1
        self.assertTrue(state._check_vertical_unsafe(0))
        self.assertFalse(state._check_vertical_unsafe(1))

    def test_left_diagonal_unsafe(self):
        state = QueensState(8,8)
        self.assertFalse(state._check_diagonal_left_unsafe(0, 0))
        for i in range(8):
            state._board[i][i] = 1
        for i in range(8):
            self.assertTrue(state._check_diagonal_left_unsafe(i,i))
        state._board[0][0] = 0
        for i in range(8):
            self.assertTrue(state._check_diagonal_left_unsafe(i,i))
        state._board[1][0] = 1
        for i in range(7):
            self.assertFalse(state._check_diagonal_left_unsafe(1+i,i))
        state._board[2][1] = 1
        for i in range(7):
            self.assertTrue(state._check_diagonal_left_unsafe(1+i,i))

    def test_right_diagonal_unsafe(self):
        state = QueensState(8, 8)
        self.assertFalse(state._check_diagonal_right_unsafe(7, 0))
        for i in range(8):
            state._board[7-i][i] = 1
        for i in range(8):
            self.assertTrue(state._check_diagonal_right_unsafe(7-i,i))
        state._board[7][0] = 0
        for i in range(8):
            self.assertTrue(state._check_diagonal_right_unsafe(7-i,i))
        state._board[7][1] = 1
        for i in range(7):
            self.assertFalse(state._check_diagonal_right_unsafe(7-i,1+i))
        state._board[6][2] = 1
        for i in range(7):
            self.assertTrue(state._check_diagonal_right_unsafe(7 - i, 1 + i))

    def test_any_queens_unsafe_with_zero_or_one_queens(self):
        state = QueensState(8,8)
        self.assertFalse(state.any_queens_unsafe())
        state._board[0][0] = 1
        self.assertFalse(state.any_queens_unsafe())

    def test_has_queens(self):
        state = QueensState(8,8)
        state._board[0][0] = 1
        state._board[0][5] = 1
        self.assertTrue(state.any_queens_unsafe())
        state._board[0][5] = 0
        state._board[7][0] = 1
        self.assertTrue(state.any_queens_unsafe())
        state._board[7][0] = 0
        state._board[7][7] = 1
        self.assertTrue(state.any_queens_unsafe())
        state._board[7][7] = 0
        state._board[5][4] = 1
        state._board[4][5] = 1
        self.assertTrue(state.any_queens_unsafe())

    def test_has_queens_all_safe(self):
        state = QueensState(4,4)
        state._board[0][1] = 1
        state._board[1][3] = 1
        state._board[2][0] = 1
        state._board[3][2] = 1
        self.assertFalse(state.any_queens_unsafe())
        state = QueensState(8,8)
        state._board[0][3] = 1
        state._board[1][6] = 1
        state._board[2][2] = 1
        state._board[3][7] = 1
        state._board[4][1] = 1
        state._board[5][4] = 1
        state._board[6][0] = 1
        state._board[7][5] = 1
        self.assertFalse(state.any_queens_unsafe())

    def test_with_queens_added(self):
        orig = QueensState(8,8)
        temp = orig._board[::]
        pos = [Position(1,1), Position(3,2)]
        new = orig.with_queens_added(pos)
        self.assertEqual(orig._board, temp)
        self.assertEqual(1, new._board[1][1])
        self.assertEqual(1, new._board[3][2])
        with self.assertRaises(DuplicateQueenError):
            new2 = new.with_queens_added([Position(1,1)])
        self.assertEqual('duplicate queen in row 1 column 1', DuplicateQueenError(Position(1,1)).__str__())

    def test_with_queens_removed(self):
        orig = orig = QueensState(8,8)
        pos = [Position(1, 1), Position(3, 2)]
        new = orig.with_queens_added(pos)
        temp = new._board[::]
        new1 = new.with_queens_removed([Position(1,1)])
        self.assertEqual(new._board, temp)
        self.assertEqual(0, new1._board[1][1])
        with self.assertRaises(MissingQueenError):
            new1.with_queens_removed([Position(1,1)])
        self.assertEqual('missing queen in row 1 column 1', MissingQueenError(Position(1,1)).__str__())

    def test_invalid_positions_with_queens_added(self):
        state = QueensState(4,4)
        with self.assertRaises(ValueError):
            new = state.with_queens_added([Position(-1,-1)])
        with self.assertRaises(ValueError):
            new = state.with_queens_added([Position(5,1)])
        with self.assertRaises(ValueError):
            new = state.with_queens_added([Position(1,5)])
        with self.assertRaises(ValueError):
            new = state.with_queens_added([Position(-1,5)])


    def test_invalid_positions_with_queens_removed(self):
        state = QueensState(4, 4)
        with self.assertRaises(ValueError):
            new = state.with_queens_removed([Position(-1, -1)])
        with self.assertRaises(ValueError):
            new = state.with_queens_removed([Position(5,1)])
        with self.assertRaises(ValueError):
            new = state.with_queens_removed([Position(1,5)])
        with self.assertRaises(ValueError):
            new = state.with_queens_removed([Position(-1,5)])


    def test_duplicate_with_queens_added(self):
        state = QueensState(4,4)
        with self.assertRaises(DuplicateQueenError):
            new = state.with_queens_added([Position(1,1), Position(1,1)])

    def test_duplicate_with_queens_removed(self):
        state = QueensState(4,4)
        new = state.with_queens_added([Position(1,1)])
        with self.assertRaises(MissingQueenError):
            new1 = new.with_queens_removed([Position(1,1), Position(1,1)])



if __name__ == '__main__':
    unittest.main()
