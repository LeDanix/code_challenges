import random
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

class Coord:
    _X: bytes
    _Y: bytes

    def __init__(self, X: int, Y: int):
        self.coord = (X, Y)

    @property
    def X(self):
        return self.coord[0]

    @property
    def Y(self):
        return self.coord[1]

    def into_list(self, coord_list: list):
        for coord in coord_list:
            if coord.X == self.X and coord.Y == self.Y:
                return True
        return False


class Cell:
    _coord: Coord
    _g_value: float
    _f_value: float
    _last_coord: Coord
    _visited_status: bool

    def __init__(self, coord: Coord, g: float, f: float, last: Coord, visited: bool = False):
        self._coord, self._g_value, self._f_value, self._last_coord, self._visited_status = coord, g, f, last, visited
    
    @property
    def coord(self):
        return self._coord
    
    @property
    def g(self):
        return self._g_value
    
    @g.setter
    def g(self, g):
        self._g_value = g

    @property
    def f(self):
        return self._f_value
    
    @f.setter
    def f(self, f):
        self._f_value = f

    @property
    def last(self):
        return self._last_coord
    
    @last.setter
    def last(self, last):
        self._last_coord = last

    @property
    def visited(self):
        return self._visited_status
    
    @visited.setter
    def visited(self, visited):
        self._visited_status = visited
     

class Map:
    _rows: int
    _colums: int
    _start_cell: Coord
    _final_cell: Coord

    OPEN: int = 0
    WALL: int = 1
    WEIGHTS: list = [0.8, 0.2]
    DIRECTIONS = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)]  # Diagonal movement
    # DIRECTIONS = [(0, 1), (-1, 0), (1, 0), (0, -1)]  # Non diagonal movement
    COLOR_MAP = ListedColormap(['white', 'black', 'red'], [0, 1, 2], N=3)

    def __init__(self, rows: int, colums: int, start_cell: Coord, final_cell: Coord):
        self._rows = rows
        self._colums = colums
        self._start_cell = start_cell
        self._final_cell = final_cell
        self._map = np.empty(shape=(self._rows, self._colums), dtype=Cell)
        self._wall_map = np.empty(shape=(self._rows, self._colums), dtype=int)
        for i in range(self._rows):
            for j in range(self._colums):
                self._map[i][j] = Cell(coord=Coord(i, j), g=9999, f=9999, last=None, visited=False)
                self._wall_map[i][j] = random.choices([0, 1], weights=Map.WEIGHTS)[0] if not Coord(i, j).into_list([start_cell, final_cell]) else 0

    @property
    def s_cell(self) -> Coord:
        return self._start_cell
    
    @property
    def f_cell(self) -> Coord:
        return self._final_cell
    
    @property
    def wall_map(self):
        return self._wall_map

    def is_wall(self, coord: Coord) -> int:
        return self._wall_map[coord.X][coord.Y] == Map.WALL

    @property
    def map(self):
        return self._map
    
    def set_cell(self, cell: Cell, coord: Coord):
        self._map[coord.X][coord.Y] = cell

    def get_cell(self, coord: Coord) -> Cell:
        return self._map[coord.X][coord.Y]
    
    @staticmethod
    def euc_dist(coord_1: Coord, coord_2: Coord) -> float:
        return math.hypot(coord_1.X - coord_2.X, coord_1.Y - coord_2.Y)

    @staticmethod
    def _f_calc(act_cell: Cell, f_cell: Coord) -> float:
        # Heuristic calculation f = g + h
        return act_cell.g + Map.euc_dist(act_cell.coord, f_cell)

    def less_f_neights(self, coord: Coord) -> Cell:
        less_f_cell: Cell
        less_f = 9999
        for mov in Map.DIRECTIONS:  # Iterate over neight to the actual Cell
            if (self._rows - 1 < coord.X + mov[0]) or (coord.X + mov[0] < 0) or \
               (self._colums - 1 < coord.Y + mov[1]) or (coord.Y + mov[1] < 0):  # Cell exists
                continue
            neight_coord = Coord(coord.X + mov[0], coord.Y + mov[1])
            selected_cell = self.get_cell(neight_coord)
            """if selected_cell.visited:  # If cell already visited, do not take into account
                continue"""
            if selected_cell.f < less_f and not self.is_wall(neight_coord): # If f is less than the previous and cell is not a wall
                less_f = selected_cell.f
                less_f_cell = selected_cell
        return less_f_cell

    def recalculate_neight_params(self, coord: Coord):
        for mov in Map.DIRECTIONS:  # Iterate over neight to the actual Cell
            if (self._rows - 1 < coord.X + mov[0]) or (coord.X + mov[0] < 0) or \
               (self._colums - 1 < coord.Y + mov[1]) or (coord.Y + mov[1] < 0):  # Cell exists
                continue
            selected_cell = self.get_cell(Coord(coord.X + mov[0], coord.Y + mov[1]))
            """if selected_cell.visited:  # If cell already visited, do not recalculate
                continue"""
            # Update neight values
            cost_from_init = np.sum([self.get_cell(Coord(x, y)).visited == True for x, y in np.ndindex(self.map.shape)])
            selected_cell.g = cost_from_init if cost_from_init < selected_cell.g else selected_cell.g
            selected_cell.f = Map._f_calc(selected_cell, self.f_cell)
            selected_cell.last = coord

    def print_matrix(self):
        aux_map = np.array(self._wall_map) + np.array([[2 if cell.visited else 0 for cell in row] for row in self._map])
        plt.imshow(aux_map, cmap=Map.COLOR_MAP)
        plt.draw()
        plt.pause(0.2)
        plt.clf()


def resolve_a_star(map: Map):
    # Initialize visited list first cell
    map.set_cell(
        cell=Cell(
            coord=map.s_cell,
            g=0,
            f=Map.euc_dist(map.s_cell, map.f_cell),
            last=None,
            visited=True),
        coord=map.s_cell
        )
    act_cell_coord = map.s_cell
    while not map.get_cell(map.f_cell).visited:  # While the f_cell was not visited -> Continue
        map.recalculate_neight_params(act_cell_coord)
        less_f_cell = map.less_f_neights(act_cell_coord)
        map.get_cell(less_f_cell.coord).visited = True
        map.print_matrix()
        act_cell_coord = less_f_cell.coord

def main():
    s_cell, f_cell = Coord(0, 0), Coord(39, 39)
    map = Map(40, 40, s_cell, f_cell)
    resolve_a_star(map)


if __name__ == '__main__':
    main()