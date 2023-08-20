from Coord import Coord

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
     
