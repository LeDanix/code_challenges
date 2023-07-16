import random
import math
import numpy as np
import matplotlib as plt

class Coord:
    X: bytes = 0
    Y: bytes = 0

    def __init__(self, X: int, Y: int):
        self.coord = (X, Y)

    @property
    def X(self):
        return self.coord[0]

    @property
    def Y(self):
        return self.coord[1]

class Cell:
    _g: int
    _f: int
    _coord: Coord
    last: Coord

    def __init__(self, coord: Coord, g: int, f: int, last: Coord):
        self._coord, self._g, self._f, self._last = coord, g, f, last
    
    @property
    def coord(self):
        return self._coord
    
    @property
    def g(self):
        return self._g

    @property
    def f(self):
        return self._f
    
    @property
    def last(self):
        self._last

        
class Map:
    _rows: int
    _colums: int
    _start_cell: Coord
    _final_cell: Coord
    _map: list
    _non_visited: list
    _visited: list

    def __init__(self, rows: int, colums: int, start_cell: Coord, final_cell: Coord):
        self._rows = rows
        self._colums = colums
        self._start_cell = start_cell
        self._final_cell = final_cell
        # 1 -> Open way, 2 -> Wall
        self._map = np.array([[random.choice([0, 1]) if Coord(i, j) not in [start_cell, final_cell] else 0 for j in range(colums)] for i in range(rows)])
        self._non_visited = np.array(np.array() * rows) * colums
        for i in range(rows):
            for j in range(colums):
                self._non_visited[i][j] = Cell(Coord(i, j), 9999, 9999, None)
        self._visited = np.array(np.array() * rows) * colums

    @property
    def s_cell(self):
        return self._start_cell
    
    @property
    def f_cell(self):
        return self._final_cell
    
    @property
    def map(self) -> np.array:
        return self._map

    def get_cell_state(self, coord: Coord) -> int:
        return self._map[coord.X][coord.Y]
    
    @property
    def non_visited(self):
        return self._non_visited
    
    def get_cell_non_vis(self, coord: Coord) -> Cell:
        return self._non_visited[coord.X][coord.Y]
    
    def set_cell_non_vis(self, cell: Cell, coord: Coord):
        self._non_visited[coord.X][coord.Y] = cell

    @property
    def visited(self):
        return self._visited
    
    def set_cell_vis(self, cell: Cell, coord: Coord):
        self._non_visited[coord.X][coord.Y] = cell

    def get_cell_vis(self, coord: Coord) -> Cell:
        return self._non_visited[coord.X][coord.Y]
    
    def less_f_neight(self, coord: Coord):
        aux = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)]
        less_f = 9999
        for mov in aux:
            if self._rows < coord.X + mov[0] or coord.X + mov[0] < 0 or self._colums < coord.Y + mov[1] or coord.Y + mov[1] < 0:  # Existing cell
                continue
            neight_coord = Coord(coord.X + mov[0], coord.Y + mov[1])
            selected_cell = self.get_cell_non_vis(neight_coord)
            if selected_cell.f < less_f and self.get_cell_state(neight_coord): # If f is less than the previous and is cell is not a wall
                less_f = selected_cell.f
        return less_f


    def print_matrix(self):
        plt.imshow(self._map.astype(float), cmap='Greys', interpolation='nearest')
        plt.draw()
        plt.pause(0.00001)
        plt.clf()

def euc_dist(coord_1: Coord, coord_2: Coord):
        return math.sqrt((coord_2.X - coord_1.X) ** 2 + (coord_2.Y - coord_1.Y) ** 2)

def f_calc(act_cell: Cell, f_cell: Cell):
    # Heuristic calculation f = g + h
    return act_cell.g + euc_dist(act_cell.coord, f_cell.coord)

def resolve_a_star(map: Map):
    # Initialize non visited list first cell
    map.set_cell_non_vis(
        cell=Cell(
            coord=map.s_cell.coord,
            g=0,
            f=euc_dist(map.s_cell.coord, map.f_cell.coord),
            last=None),
        coord=map.s_cell.coord
        )
    




def main():
    s_cell = Coord(0, 0)
    f_cell = Coord(40, 40)
    map = Map(40, 40, s_cell, f_cell)


if __name__ == '__main__':
    main()