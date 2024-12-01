from enum import Enum
from dataclasses import dataclass


@dataclass
class Position:
    """
        Position in "normalized" ccordinates where to put the
        respective tile
    """
    x : int
    y : int

class Corner(Enum):
    """
        Enum type of four corners of a rectangular tile
    """
    NO = 0
    UL = 1
    UR = 2
    LL = 3
    LR = 4


@dataclass
class BoundingBox:
    """
        Bounding box of a rectangular tile
    """
    ulx: float
    uly: float
    lrx: float
    lry: float

    def __str__(self):
        return "({0}, {1}) / ({2}, {3})".format(self.ulx, self.uly, self.lry, self.lry)


