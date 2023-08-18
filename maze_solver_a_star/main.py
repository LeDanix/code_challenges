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
    # DIRECTIONS = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)]  # Diagonal movement
    DIRECTIONS = [(0, 1), (-1, 0), (1, 0), (0, -1)]  # Non diagonal movement
    COLOR_MAP = ListedColormap(['white', 'black', 'red', 'green'], [0, 1, 2, 3], N=4)

    def __init__(self, rows: int, colums: int, start_cell: Coord, final_cell: Coord):
        self._rows = rows
        self._colums = colums
        self._start_cell = start_cell
        self._final_cell = final_cell
        self._cell_map = np.empty(shape=(self._rows, self._colums), dtype=Cell)
        self._wall_map = np.empty(shape=(self._rows, self._colums), dtype=int)
        for i in range(self._rows):
            for j in range(self._colums):
                self._cell_map[i][j] = Cell(coord=Coord(i, j), g=9999, f=9999, last=None, visited=False)
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
        return self._cell_map
    
    def set_cell(self, cell: Cell, coord: Coord):
        self._cell_map[coord.X][coord.Y] = cell

    def get_cell(self, coord: Coord) -> Cell:
        return self._cell_map[coord.X][coord.Y]
    
    """@staticmethod
    def euc_dist(coord_1: Coord, coord_2: Coord) -> float:
        return math.sqrt((coord_1.X - coord_2.X)**2 + (coord_1.Y - coord_2.Y)**2)"""

    @staticmethod
    def euc_dist(coord_1: Coord, coord_2: Coord) -> float:
        return (coord_1.X - coord_2.X) + (coord_1.Y - coord_2.Y)

    @staticmethod
    def _f_calc(act_cell: Coord, f_cell: Coord, g_value: float) -> float:
        # Heuristic calculation f = g + h
        return g_value + Map.euc_dist(f_cell, act_cell)

    def less_f_neights(self) -> Cell:
        less_f = 9999
        less_f_cell = None
        for i, j in np.ndindex(self.map.shape):
            selected_cell = self.get_cell(Coord(i, j))
            if selected_cell.visited:  # If cell already visited, ignore
                continue
            if selected_cell.f <= less_f and not self.is_wall(selected_cell.coord): # If f is less than the previous and cell is not a wall
                less_f = selected_cell.f
                less_f_cell = selected_cell
        if less_f_cell is None:
            import sys
            print("No maze possible")
            sys.exit()
        return less_f_cell

    def recalculate_neight_params(self, coord: Coord):
        for mov in Map.DIRECTIONS:  # Iterate over neight to the actual Cell
            if (self._rows - 1 < coord.X + mov[0]) or (coord.X + mov[0] < 0) or \
               (self._colums - 1 < coord.Y + mov[1]) or (coord.Y + mov[1] < 0):  # Cell exists
                continue
            selected_cell = self.get_cell(Coord(coord.X + mov[0], coord.Y + mov[1]))
            if self.is_wall(selected_cell.coord):
                continue
            # Update neight values
            g = self.get_cell(coord).g + 1
            f = Map._f_calc(selected_cell.coord, self.f_cell, g)
            if f < selected_cell.f:
                selected_cell.g = g
                selected_cell.f = f
                selected_cell.last = coord
    
    def backtracking(self):
        cell = self.get_cell(self.s_cell)
        path = [cell.coord]
        current_f = cell.f
        while not cell.coord.into_list([self.f_cell]):
            for mov in Map.DIRECTIONS:
                if (self._rows - 1 < cell.coord.X + mov[0]) or (cell.coord.X + mov[0] < 0) or \
                   (self._colums - 1 < cell.coord.Y + mov[1]) or (cell.coord.Y + mov[1] < 0):  # Cell exists
                    continue
                neight_cell = self.get_cell(Coord(cell.coord.X + mov[1], cell.coord.Y + mov[0]))
                if neight_cell.f < current_f and not self.is_wall(neight_cell.coord):
                    current_f = neight_cell.f
                    current_neight_cell = neight_cell
            cell = current_neight_cell
            path.append(cell.coord)
        return np.array([path[i].coord for i in range(len(path))])
            
    def print_matrix(self, path_map: np.ndarray):
        aux_map = np.array(self._wall_map) + np.array([[2 if cell.visited else 0 for cell in row] for row in self._cell_map]) + path_map
        plt.imshow(aux_map, cmap=Map.COLOR_MAP)
        plt.draw()
        plt.pause(0.2)
    
    def print_f_matrix(self):
        """DEBUG"""
        a = np.zeros((5, 5), dtype=float)
        for i in range(self.map.shape[0]):
            for j in range(self.map.shape[1]):
                a[i][j] = self.get_cell(Coord(i, j)).f
    

def resolve_a_star(map: Map):
    path_map = np.zeros(shape=(map.wall_map.shape[0], map.wall_map.shape[1]), dtype=int)
    # Initialize visited list first cell
    map.set_cell(
        cell=Cell(
            coord=map.s_cell,
            g=0,
            f=Map.euc_dist(map.f_cell, map.s_cell),
            last=None,
            visited=True),
        coord=map.s_cell
        )
    
    # Fill the map
    act_cell_coord = map.s_cell
    while not map.get_cell(map.f_cell).visited:  # While the f_cell was not visited -> Continue
        map.recalculate_neight_params(act_cell_coord)
        less_f_cell = map.less_f_neights()
        map.get_cell(less_f_cell.coord).visited = True
        map.print_matrix(path_map)
        act_cell_coord = less_f_cell.coord

    # Backtracking
    path = map.backtracking()

    # DEBUG
    for i in range(len(path)):
        print(f"{path[i]}")
    
    # Print path
    path_map[path[:, 0], path[:, 1]] = 1
    map.print_matrix(path_map)

def main():
    # TODO
    # Organize classes into different folders
    # Document all code
    # Fix Bugs - Ufffff
    # PR and README.md
    rows, columns = 5, 5
    map = Map(rows, columns, Coord(0, 0), Coord(rows - 1, columns - 1))
    resolve_a_star(map)


if __name__ == '__main__':
    main()