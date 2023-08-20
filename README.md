# Code Challenges
This repository contains diferent code challenges.

## Game of Life - Python powered
This project simulates cells behaviour into a NxN matrix.

The logic about the creation and elimination of the cells follows the next logic:

- If a cell is sourronding by less than 2 cells or more than 3 cells, this cell dies. If not, remains.

- If a empty space whitout any cell is sourronding by exactly 3 cells, a new one borns. If not, the empty space will remain.

*This project is powered by Python, NumPy and MatplotLib for matrix visualization.*

## Game of Life - Java powered
This projects copy the same methodology as [the python based](#game-of-life---python-based).

*It is powered by Java JDK 20 and only use java default libraries.*

## Maze solver - A* algorithm Python powered
This project simulates a random wall map (maze) and the optimal path between StartCell to FinalCell.

Can be used into 2 diferent modes
* 4 directions availables of movement
* 8 directions availables of movement (Diagonals).
with the following code
```python
DIRECTIONS = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)]  # Diagonal movement
DIRECTIONS = [(-1, 0), (0, -1), (1, 0), (0, 1)]  # Non diagonal movement
```

Also, the number of walls can be changed by this 2 parameters
```python
WEIGHTS: list = [0.6, 0.4]  # % empty, % wall
```

As result, the algorithm can resolved any possible situation into any size, as you can see

<img src="https://github.com/LeDanix/code_challenges/assets/74117305/ec262a59-906e-46bc-93d7-3e6057ee747d" alt="Easy map" width="300" height="200">
<img src="https://github.com/LeDanix/code_challenges/assets/74117305/547cafc8-101e-4abb-ad4d-7534295d006b" alt="Complex map" width="300" height="200">

In green, the optimal path. In red, all the cells which were researched but not optimal or possible path.
