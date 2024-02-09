# queens.py
#
# ICS 33 Winter 2023
# Project 0: History of Modern
#
# A module containing tools that could assist in solving variants of the
# well-known "n-queens" problem.  Note that we're only implementing one part
# of the problem: immutably managing the "state" of the board (i.e., which
# queens are arranged in which cells).  The rest of the problem -- determining
# a valid solution for it -- is not our focus here.
#
# Your goal is to complete the QueensState class described below, though
# you'll need to build it incrementally, as well as test it incrementally by
# writing unit tests in test_queens.py.  Make sure you've read the project
# write-up before you proceed, as it will explain the requirements around
# following (and documenting) an incremental process of solving this problem.
#
# DO NOT MODIFY THE Position NAMEDTUPLE OR THE PROVIDED EXCEPTION CLASSES.

from collections import namedtuple
from typing import Self



Position = namedtuple('Position', ['row', 'column'])

# Ordinarily, we would write docstrings within classes or their methods.
# Since a namedtuple builds those classes and methods for us, we instead
# add the documentation by hand afterward.
Position.__doc__ = 'A position on a chessboard, specified by zero-based row and column numbers.'
Position.row.__doc__ = 'A zero-based row number'
Position.column.__doc__ = 'A zero-based column number'



class DuplicateQueenError(Exception):
    """An exception indicating an attempt to add a queen where one is already present."""

    def __init__(self, position: Position):
        """Initializes the exception, given a position where the duplicate queen exists."""
        self._position = position


    def __str__(self) -> str:
        return f'duplicate queen in row {self._position.row} column {self._position.column}'



class MissingQueenError(Exception):
    """An exception indicating an attempt to remove a queen where one is not present."""

    def __init__(self, position: Position):
        """Initializes the exception, given a position where a queen is missing."""
        self._position = position


    def __str__(self) -> str:
        return f'missing queen in row {self._position.row} column {self._position.column}'

class QueensState:
    """Immutably represents the state of a chessboard being used to assist in
    solving the n-queens problem."""

    def __init__(self, rows: int, columns: int):
        """Initializes the chessboard to have the given numbers of rows and columns,
        with no queens occupying any of its cells."""
        self._rows = rows
        self._columns = columns
        if rows <= 0 or columns <= 0:
            raise ValueError
        self._board = []
        for r in range(rows):
            row = []
            for c in range(columns):
                row.append(0)
            self._board.append(row)


    def queen_count(self) -> int:
        """Returns the number of queens on the chessboard."""
        count = 0
        for r in range(self._rows):
            for c in range(self._columns):
                if self._board[r][c] == 1:
                    count += 1
        return count


    def queens(self) -> list[Position]:
        """Returns a list of the positions in which queens appear on the chessboard,
        arranged in no particular order."""
        ans = []
        for row in range(self._rows):
            for col in range(self._columns):
                if self._board[row][col] == 1:
                    ans.append(Position(row, col))
        return ans


    def has_queen(self, position: Position) -> bool:
        """Returns True if a queen occupies the given position on the chessboard, or
        False otherwise."""
        row = position.row
        col = position.column
        if row < 0 or col < 0:
            return False
        try:
            if self._board[row][col] == 1:
                return True
        except IndexError:
            pass
        return False


    def any_queens_unsafe(self) -> bool:
        """Returns True if any queens on the chessboard are unsafe (i.e., they can
        be captured by at least one other queen on the chessboard), or False otherwise."""
        queen_positions = self.queens()
        if len(queen_positions) <= 1:
            return False
        for queen_position in queen_positions:
            row = queen_position.row
            col = queen_position.column
            safe1 = self._check_horizontal_unsafe(row)
            safe2 = self._check_vertical_unsafe(col)
            safe3 = self._check_diagonal_left_unsafe(row, col)
            safe4 = self._check_diagonal_right_unsafe(row, col)
            if safe1 or safe2 or safe3 or safe4:
                return True
        return False


    def with_queens_added(self, positions: list[Position]) -> Self:
        """Builds a new QueensState with queens added in the given positions.
        Raises a DuplicateQueenException when there is already a queen in at
        least one of the given positions."""
        current_queen_positions = self.queens()
        for position in positions:
            if not ((0 <= position.row < self._rows) and (0 <= position.column < self._columns)):
                raise ValueError
            if position not in current_queen_positions:
                current_queen_positions.append(position)
            else:
                raise DuplicateQueenError(position)
        new_queen_state = QueensState(self._rows, self._columns)
        for position in current_queen_positions:
            row = position.row
            col = position.column
            new_queen_state._board[row][col] = 1
        return new_queen_state



    def with_queens_removed(self, positions: list[Position]) -> Self:
        """Builds a new QueensState with queens removed from the given positions.
        Raises a MissingQueenException when there is no queen in at least one of
        the given positions."""
        current_queen_positions = self.queens()
        for position in positions:
            if not ((0 <= position.row < self._rows) and (0 <= position.column < self._columns)):
                raise ValueError
            if position not in current_queen_positions:
                raise MissingQueenError(position)
            current_queen_positions.remove(position)
        new_queen_state = QueensState(self._rows, self._columns)
        current_board = self._board[::]
        for position in positions:
            row = position.row
            col = position.column
            current_board[row][col] = 0
        new_queen_state._board = current_board
        return new_queen_state

    def _check_horizontal_unsafe(self, row: int) -> bool:
        """Takes a provided row and checks if there are multiple queens in it
        returning True if there are and False if not"""
        specified_row = self._board[row]
        return sum(specified_row) >= 2

    def _check_vertical_unsafe(self, col: int) -> bool:
        """Takes a provided column and checks if there are multiple queens in it
        returning True if there are and False if not"""
        specified_column = []
        for i in range(self._rows):
            specified_column.append(self._board[i][col])
        return sum(specified_column) >= 2

    def _check_diagonal_left_unsafe(self, row: int, col: int) -> bool:
        """Takes a provided row and column and checks if there are multiple queens in
        a left to right diagonal returning True if there are and False if not"""
        specified_diagonal = []
        moves_back = min(row, col)
        new_row = row - moves_back
        new_col = col - moves_back
        while True:
            try:
                specified_diagonal.append(self._board[new_row][new_col])
                new_row += 1
                new_col += 1
            except IndexError:
                break
        if sum(specified_diagonal) >= 2:
            return True
        return False

    def _check_diagonal_right_unsafe(self, row: int, col: int) -> bool:
        """Takes a provided row and column and checks if there are multiple queens in
        a right to left diagonal returning True if there are and False if not"""
        specified_diagonal = []
        moves_back = min(row, self._columns-1-col)
        new_row = row - moves_back
        new_col = col + moves_back
        while True:
            try:
                specified_diagonal.append(self._board[new_row][new_col])
                new_row += 1
                new_col -= 1
                if new_col < 0:
                    break
            except IndexError:
                break
        if sum(specified_diagonal) >= 2:
            return True
        return False