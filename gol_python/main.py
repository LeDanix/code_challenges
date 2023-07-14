########################################################
# Game of Life
# Author: Daniel Saiz Azor
# Powered by Python 3.8.5
########################################################

import numpy as np
import matplotlib.pyplot as plt

import random

class Cell:
    ALIVE = 0
    DEAD = 1

    def cell_state(self, state: int):
        return self.ALIVE if state == 0 else self.DEAD

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

class Matrix:
    def __init__(self, rows: int, colums: int):
        self.cell = Cell()
        self._matrix = np.array([[random.choice([Cell.ALIVE, Cell.DEAD]) for j in range(colums)] for i in range(rows)])

    @property
    def matrix(self) -> np.array:
        return self._matrix

    @matrix.setter
    def matrix(self, matrix: np.array):
        self._matrix = matrix

    def get_cell_state(self, coord: Coord) -> Cell:
        return self.cell.cell_state(self.matrix[coord.X][coord.Y])

    def set_cell_state(self, coord: Coord, state: Cell):
        self.matrix[coord.X][coord.Y] = self.cell.cell_state(state)
    
    def n_alives(self, coord: Coord) -> int:
        mask = self.matrix[np.s_[coord.X - 1: coord.X + 2, coord.Y - 1: coord.Y + 2]] == self.cell.ALIVE
        return np.count_nonzero(mask)

    def gol_logic(self, coord: Coord) -> Cell:
        if self.get_cell_state(coord) == Cell.DEAD:
            return Cell.ALIVE if self.n_alives(coord) == 3 else Cell.DEAD
        if self.get_cell_state(coord) == Cell.ALIVE:
            if self.n_alives(coord) > 3 or self.n_alives(coord) < 2:
                return Cell.DEAD
            elif self.n_alives(coord) in [2, 3]:
                return Cell.ALIVE

    def print_matrix(self):
        plt.imshow(self.matrix.astype(float), cmap='Greys', interpolation='nearest')
        plt.draw()
        plt.pause(0.00001)
        plt.clf()

    def update(self):
        matrix_copy = np.zeros((self.matrix.shape[0], self.matrix.shape[1]))
        for i in range(self.matrix.shape[0]):
            for j in range(self.matrix.shape[1]):
                matrix_copy[i][j] = self.gol_logic(Coord(i, j))
        self.matrix = matrix_copy
        return self.matrix

def main():
    game_matrix = Matrix(100, 100)
    while True:
        game_matrix.update()
        game_matrix.print_matrix()

if __name__ == "__main__":
    main()

    