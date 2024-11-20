import numpy as np
from typing import Any, Iterable, Optional, Sequence
from itertools import product
from puzzles import *


class Sudoku:
    def __init__(self, board: np.ndarray, symbols: Sequence[int] = (1, 2, 3, 4, 5, 6, 7, 8, 9), box_height: int = 3, box_width: int = 3):
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
        
    
    def create_possible_map(self) -> np.ndarray:
        """Creates a 3D array which represents all possible symbols which could exist in an area, using guarenteed information (no problem-solving heuristics)"""
        slate = np.ones((self.height, self.width, self.depth), dtype=bool)  # every symbol is possible in every position
        for pos in self.positions():
            if self.board[pos] in self.symbols:
                slate[pos] = np.zeros((self.depth,))
                continue
            connected = self.get_connected_positions(pos)
            for connected_pos in connected:
                symbol = self.board[connected_pos]
                try:
                    slate[pos][self.symbols.index(symbol)] = 0
                except ValueError:
                    continue  # the value is empty
        return slate

    def chunk_possible_map(self, possible_map: Optional[np.ndarray] = None) -> dict[tuple[int, ...], set[tuple[int, int]]]:
        """Creates a dictionary which matches each unique "possible" map to the positions on the board which contain that specific possible map"""
        if possible_map is None:
            possible_map = self.create_possible_map()

        primary_map = {}

        for position in self.positions():
            possible_values = tuple(map(int, tuple(possible_map[position])))
            primary_map.setdefault(possible_values, set())
            primary_map[possible_values].add(position)
        
        return primary_map


    def solve_iteration(self):
        rpk = self.chunk_possible_map()
        possible_map = self.create_possible_map()
        # print(possible_map)

        for possible, positions in rpk.items():
            positions = list(positions)
            n_possible = sum(possible)
            n_existing = len(positions)

            # print(possible, positions)
            
            if n_possible != n_existing:
                # print("skip")
                continue
            
            connected = self.get_connected_positions(positions[0])
            if not all([p in connected for p in positions[1:]]):
                # print("skip 2")
                continue
                
            for position in connected:
                if position in positions:
                    continue  # the connected pos is part of the group we just created
                # print("\t rem", position)
                # print(possible_map[position])
                possible_map[position] &= ~np.array(possible, dtype=bool)
                # print(possible_map[position])
            
        # print(possible_map)
        
        self.replace_singles(possible_map=possible_map)


    def replace_singles(self, possible_map: Optional[np.ndarray] = None) -> None:
        # replace all single possible map keys with the value
        if possible_map is None:
            possible_map = self.create_possible_map()

        for pos in self.positions():
            if self.board[pos] not in self.symbols and sum(possible_map[pos]) == 1:
                self.board[pos] = self.symbols[list(possible_map[pos]).index(1)]


board = solved_1

sudoku = Sudoku(np.array(board), range(1, 10), 3, 3)
import pprint
print(sudoku.board)
sudoku.solve_iteration()
print(sudoku.board)