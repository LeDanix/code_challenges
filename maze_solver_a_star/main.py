import numpy as np

from Coord import Coord
from Cell import Cell
from Map import Map


def resolve_a_star(map: Map):
    """
    This method resolves the maze with the A* methodology

    Args:
        map (Map): Object Map where all the information is located
    """
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
        map.print_matrix(path_map, Map.COLOR_MAP_1)
        act_cell_coord = less_f_cell.coord

    # Backtracking
    path = map.backtracking()
    
    # Print path
    for p in path:
        path_map[p[0], p[1]] = 1
    map.print_matrix(path_map, Map.COLOR_MAP_2)

def main():
    # TODO
    # Fix Bugs
    # PR and README.md
    rows, columns = 15, 15
    map = Map(rows, columns, Coord(0, 0), Coord(rows - 1, columns - 1))
    resolve_a_star(map)
    input("")


if __name__ == '__main__':
    main()