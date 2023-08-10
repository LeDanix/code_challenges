import random
import math
import numpy as np
import matplotlib as plt

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
    _g: int
    _f: int
    _coord: Coord
    _last: Coord
    _visited: bool

    def __init__(self, coord: Coord, g: int, f: int, last: Coord, visited: bool = False):
        self._coord, self._g, self._f, self._last, self._visited = coord, g, f, last, visited
    
    @property
    def coord(self):
        return self._coord
    
    @property
    def g(self):
        return self._g
    
    @g.setter
    def g(self, g):
        self._g = g

    @property
    def f(self):
        return self._f
    
    @f.setter
    def f(self, f):
        self._f = f

    @property
    def last(self):
        self._last
    
    @last.setter
    def last(self, last):
        self._last = last

    @property
    def visited(self):
        self._visited
    
    @visited.setter
    def visited(self, visited):
        self._visited = visited

        
class Map:
    _rows: int
    _colums: int
    _start_cell: Coord
    _final_cell: Coord

    OPEN: int = 0
    WALL: int = 1
    WEIGHTS: list = [0.8, 0.2]

    def __init__(self, rows: int, colums: int, start_cell: Coord, final_cell: Coord):
        self._rows = rows
        self._colums = colums
        self._start_cell = start_cell
        self._final_cell = final_cell
        # 0 -> Open way, 1 -> Wall
        self._wall_map = np.array([[random.choices([0, 1], weights=Map.WEIGHTS) if Coord(i, j).into_list([start_cell, final_cell]) else 0 for j in range(colums)] for i in range(rows)])
        self._map = np.empty((rows, colums), dtype=Cell)
        for i in range(rows):
            for j in range(colums):
                self._map[i, j] = Cell(coord=Coord(i, j), g=9999, f=9999, last=None, visited=False)

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
        return self._wall_map[coord.X, coord.Y] == Map.WALL

    @property
    def map(self):
        return self._map
    
    def set_cell_vis(self, cell: Cell, coord: Coord):
        self._map[coord.X, coord.Y] = cell

    def get_cell_vis(self, coord: Coord) -> Cell:
        return self._map[coord.X, coord.Y]
    
    @staticmethod
    def _euc_dist(coord_1: Coord, coord_2: Coord) ->float:
        return math.hypot(coord_1.X - coord_2.X, coord_1.Y - coord_2.Y)

    @staticmethod
    def _f_calc(act_cell: Cell, f_cell: Coord) -> float:
        # Heuristic calculation f = g + h
        return act_cell.g + Map._euc_dist(act_cell.coord, f_cell)

    def less_f_neights(self, coord: Coord) -> Cell:
        aux = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)]
        less_f_cell: Cell
        less_f = 9999
        for mov in aux:  # Iterate over neight to the actual Cell
            if (self._rows < coord.X + mov[0]) or (coord.X + mov[0] < 0) or \
               (self._colums < coord.Y + mov[1]) or (coord.Y + mov[1] < 0):  # Cell exists
                continue
            neight_coord = Coord(coord.X + mov[0], coord.Y + mov[1])
            selected_cell = self.get_cell_vis(neight_coord)
            if selected_cell.visited:  # If cell already visited, do not take into account
                continue
            if selected_cell.f < less_f and not self.is_wall(neight_coord): # If f is less than the previous and cell is not a wall
                less_f = selected_cell.f
                less_f_cell = selected_cell
        return less_f_cell

    def recalculate_neight_params(self, coord: Coord):
        aux = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)]
        for mov in aux:  # Iterate over neight to the actual Cell
            if self._rows < coord.X + mov[0] or coord.X + mov[0] < 0 or self._colums < coord.Y + mov[1] or coord.Y + mov[1] < 0:  # Cell exists
                continue
            neight_coord = Coord(coord.X + mov[0], coord.Y + mov[1])
            selected_cell = self.get_cell_vis(neight_coord)
            if selected_cell.visited:  # If cell already visited, do not recalculate
                continue
            # Update neight values
            cost_from_init = np.sum([self.get_cell_vis(Coord(x, y)).visited == True for x, y in np.ndindex(self.map.shape)])
            selected_cell.g = cost_from_init if cost_from_init < selected_cell.g else selected_cell.g
            selected_cell.f = Map._f_calc(selected_cell, self.f_cell)
            selected_cell.last = self.get_cell_vis(coord)

    def print_matrix(self):
        plt.imshow(self._wall_map.astype(float), cmap='Greys', interpolation='nearest')
        plt.draw()
        plt.pause(0.00001)
        plt.clf()

def resolve_a_star(map: Map):
    # Initialize visited list first cell
    map.set_cell_vis(
        cell=Cell(
            coord=map.s_cell.coord,
            g=0,
            f=Map.euc_dist(map.s_cell.coord, map.f_cell.coord),
            last=None,
            visited=True),
        coord=map.s_cell.coord
        )
    # "Remove" cell from the nonvisited list
    map.set_cell_non_vis(
        cell=Cell(
            coord=map.s_cell.coord,
            g=10000,
            f=10000,
            last=None),
        coord=map.s_cell.coord
    )
    act_cell = map.s_cell
    while not map.get_cell_vis(map.f_cell.coord).visited:  # While the f_cell was not visited -> Continue
        map.recalculate_neight_params(act_cell.coord)
        act_cell = map.less_f_neights(act_cell)
        map.get_cell_vis(act_cell.coord).visited = True

def main():
    s_cell = Coord(0, 0)
    f_cell = Coord(40, 40)
    map = Map(40, 40, s_cell, f_cell)


if __name__ == '__main__':
    main()