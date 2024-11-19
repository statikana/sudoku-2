import numpy as np
from typing import Any, Optional
from itertools import product
from puzzles import *


class Sudoku:
    def __init__(self, board: np.ndarray, symbols: tuple[int, ...] = (1, 2, 3, 4, 5, 6, 7, 8, 9), box_height: int = 3, box_width: int = 3):
        self.board = board
        self.symbols = symbols
        self.height, self.width = self.board.shape
        self.depth = len(symbols)

        self.box_height = box_height
        self.box_width = box_width

        if self.height % self.box_height != 0 or self.width % self.box_width != 0:
            raise ValueError("Square height and width must fit evenly into the board's height and width")
    
    def positions(self) -> list[tuple[int, int]]:
        """Gets all positions (combinations of rows and columns) on the board"""
        return list(product(range(self.height), range(self.width)))

    def get_connected_positions(self, position: tuple[int, int]) -> set[tuple[int, int]]:
        """Gets all positions which influence the possible values of the position given (i.e., all positions in the same row, column, and box)"""
        row = [(row, position[1]) for row in range(self.width)]
        col = [(position[0], col) for col in range(self.height)]

        box_top = position[0] - position[0] % self.box_height
        box_left = position[1] - position[1] % self.box_width

        box = product(range(box_top, box_top + self.box_height), range(box_left, box_left + self.box_width))
        
        return set(row) | set(col) | set(box) - {position}
        
    
    def create_simple_possible(self) -> np.ndarray:
        """Creates a 3D array which represents all possible symbols which could exist in an area, using guarenteed information (no problem-solving heuristics)"""
        slate = np.ones((self.height, self.width, self.depth))  # every symbol is possible in every position
        for row, col in self.positions():
            connected = self.get_connected_positions((row, col))
            for c_row, c_col in connected:
                c_symbol = self.board[c_row, c_col]
                try:
                    slate[row, col][self.symbols.index(c_symbol)] = 0
                except ValueError:
                    continue  # the value is empty
        return slate

    def create_reverse_possible_key(self) -> dict[tuple[int, ...], set[tuple[int, int]]]:
        """Creates a dictionary which matches each unique "possible" key to the positions on the board which contain that specific possible key"""
        primary_map = {}
        possible_map = self.create_simple_possible()
        for position in self.positions():
            possible_values = tuple(map(int, tuple(possible_map[position])))
            primary_map.setdefault(possible_values, set())
            primary_map[possible_values].add(position)
        
        return primary_map


    def solve(self):
        rpk = self.create_reverse_possible_key()

        # using rpk, solve ones

        for possible, positions in rpk.items():
            n = sum(possible)
            print(n, possible, positions)


board = easy_1

sudoku = Sudoku(np.array(board), tuple(range(1, 10)), 3, 3)
print(sudoku.solve())