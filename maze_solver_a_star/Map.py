import random
import math
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from Coord import Coord
from Cell import Cell

class Map:
    _rows: int
    _colums: int
    _start_cell: Coord
    _final_cell: Coord

    OPEN: int = 0
    WALL: int = 1
    WEIGHTS: list = [0.7, 0.3]
    DIRECTIONS = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)]  # Diagonal movement
    # DIRECTIONS = [(-1, 0), (0, -1), (1, 0), (0, 1)]  # Non diagonal movement
    COLOR_MAP_1 = ListedColormap(['white', 'black', 'red'], [0, 1, 2], N=3)
    COLOR_MAP_2 = ListedColormap(['white', 'black', 'red', 'green'], [0, 1, 2, 3], N=4)

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
        return (coord_1.X - coord_2.X) + (coord_1.Y - coord_2.Y)"""
    
    @staticmethod
    def euc_dist(coord_1: Coord, coord_2: Coord) -> float:
        """
        This method lets calculate the movement cost between two cells

        Args:
            coord_1 (Coord)
            coord_2 (Coord)

        Returns:
            float: movement cost value
        """
        return math.sqrt((coord_1.X - coord_2.X)**2 + (coord_1.Y - coord_2.Y)**2)

    @staticmethod
    def _f_calc(act_cell: Coord, f_cell: Coord, g_value: float) -> float:
        # Heuristic calculation f = g + h
        return g_value + Map.euc_dist(f_cell, act_cell)

    def less_f_neights(self) -> Cell:
        """
        This method gets the cell with the smaller f(x) value.

        Returns:
            Cell: the cell with the smaller f(x) value
        """
        less_f = 10000
        less_f_cell = None
        for i, j in np.ndindex(self.map.shape):
            selected_cell = self.get_cell(Coord(i, j))
            if selected_cell.visited:  # If cell already visited, ignore
                continue
            if selected_cell.f <= less_f and not self.is_wall(selected_cell.coord): # If f is less than the previous and cell is not a wall
                less_f = selected_cell.f
                less_f_cell = selected_cell
        if less_f_cell is None:
            sys.exit("No maze possible")
        return less_f_cell

    def recalculate_neight_params(self, coord: Coord):
        """
        This method lets fill the costs of the neight cells around the cell located into coord

        Args:
            coord (Coord): Location of the cell to iterate over.
        """
        for mov in Map.DIRECTIONS:  # Iterate over neight to the actual Cell
            if (self._rows - 1 < coord.X + mov[0]) or (coord.X + mov[0] < 0) or \
               (self._colums - 1 < coord.Y + mov[1]) or (coord.Y + mov[1] < 0):  # Cell exists
                continue
            selected_cell = self.get_cell(Coord(coord.X + mov[0], coord.Y + mov[1]))
            if self.is_wall(selected_cell.coord):
                continue
            # Update neight values
            g = self.get_cell(coord).g + 0.001
            f = Map._f_calc(selected_cell.coord, self.f_cell, g)
            if f < selected_cell.f:
                selected_cell.g = g
                selected_cell.f = f
                selected_cell.last = coord
    
    def backtracking(self):
        """After the cost matrix is filled, this method lets recover the short path"""
        blocked_path = np.zeros(shape=(self._rows, self._colums), dtype=int)
        cell = self.get_cell(self.s_cell)
        last_cell = Cell(Coord(9999, 9999), 9999, 9999, Coord(9999, 9999))
        path = [(cell.coord.X, cell.coord.Y)]
        current_f = cell.f
        while not cell.coord.into_list([self.f_cell]):
            if last_cell == cell:
                cell.f = 9999
                cell = self.get_cell(last_cell.last)
                path = path[:-2]
                blocked_path[cell.coord.X][cell.coord.Y] = 1
            for mov in Map.DIRECTIONS:
                if (self._rows - 1 < cell.coord.X + mov[0]) or (cell.coord.X + mov[0] < 0) or \
                   (self._colums - 1 < cell.coord.Y + mov[1]) or (cell.coord.Y + mov[1] < 0):  # Cell exists
                    continue
                neight_cell = self.get_cell(Coord(cell.coord.X + mov[0], cell.coord.Y + mov[1]))
                if neight_cell.f <= current_f and not self.is_wall(neight_cell.coord) \
                   and neight_cell.visited and blocked_path[neight_cell.coord.X][neight_cell.coord.Y] != 1:
                    current_f = neight_cell.f
                    current_neight_cell = neight_cell
            last_cell = cell
            cell = current_neight_cell
            path.append((cell.coord.X, cell.coord.Y))
        return path
            
    def print_matrix(self, path_map: np.ndarray, cmap):
        """
        This method lets print the matrix. The colors depends on the cmap

        Args:
            path_map (np.ndarray): A map which contains the path between the start cell to final cell
            cmap (_type_): MatPlot lib util to print the matrix.
        """
        aux_map = np.array(self._wall_map) + np.array([[2 if cell.visited else 0 for cell in row] for row in self._cell_map]) + path_map
        plt.imshow(aux_map, cmap=cmap)
        plt.draw()
        plt.pause(0.2)
    
    def print_f_matrix(self):
        """DEBUG"""
        a = np.zeros((5, 5), dtype=float)
        for i in range(self.map.shape[0]):
            for j in range(self.map.shape[1]):
                a[i][j] = self.get_cell(Coord(i, j)).f
    