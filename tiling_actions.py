from dataclasses import dataclass, field
from enum import Enum

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


@dataclass
class Tiling_Action:

    corner: Corner = field(default=Corner.NO)
    displacement: float = 0.0
    add_to_x_ext: float = 0.0
    add_to_y_ext: float = 0.0

    def __call__(self, *args, **kwargs):
        pass

@dataclass
class Placement(Tiling_Action):

    selector: str
    x : int
    y : int

    def __call__(self, to_tiling):
        pass
