import numpy as np
from typing import Any, Container, Generator, Iterable, Optional, Sequence
from itertools import product
from puzzles import *
from pprint import pprint


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
                if symbol in self.symbols:
                    slate[pos][self.symbols.index(symbol)] = 0
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

    def solve(self) -> None:
        possible_map = self.create_possible_map()
        presum = possible_map[:,:,].sum()
        for k in (1, 2, 3, 4):
            k_matches = list(self.find_n_possible(possible_map, k))
            # print(k_matches)
            # pprint([possible_map[b] for b in k_matches])
            groups: list[list[tuple[int, int]]] = []

            for k_match in k_matches:
                # print(k_match)
                if k_match in flatten(groups):
                    continue
                def is_similar(base: tuple[int, int], test: tuple[int, int]):
                    return test in k_matches and all(possible_map[test] == possible_map[base]) and test != base

                group = list(filter(lambda k_connected: is_similar(k_match, k_connected), self.get_connected_positions(k_match)))
                group.append(k_match)
                groups.append(group)

                # print(group)

            # print(groups)

            for group in groups:
                # all positions in group are in the same connected region and have the same possible valuesc
                common_possible = possible_map[group[0]]  # via .is_similar(), these are guarenteeed to have not only the same n, but also just the same values too
                for element in group:
                    connected = self.get_connected_positions(element)
                    for con in connected:
                        if con not in group:
                            possible_map[con] &= ~common_possible
            
        print(presum)
        print(possible_map[:,:,].sum())
            
                
                

    
    def find_n_possible(self, possible_map: np.ndarray, n: int) -> Generator[tuple[int, int], None, None]:
        for pos in self.positions():
            if sum(possible_map[pos]) == n:
                yield pos
    
    def is_solved(self):
        return self.is_filled() and self.is_valid()

    def is_filled(self) -> bool:
        return bool(self.board.nonzero())
    
    def is_valid(self) -> bool:
        for pos in self.positions():
            symbol = self.board[pos]
            for c in self.get_connected_positions(pos):
                if self.board[c] == symbol and pos != c:
                    print("oops", pos, c, symbol)
                    return False
        return True


def flatten(l):
    for b in l:
        for a in b:
            yield a


board = medium_1

sudoku = Sudoku(np.array(board))

print(sudoku.board)
sudoku.solve()
print(sudoku.board)