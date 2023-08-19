class Coord:

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
