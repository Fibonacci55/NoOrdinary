
from tiles import Tile
from copy import deepcopy
from dataclasses import dataclass, field

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



class Tiling:

    def __init__(self, l):
        self.tiles = l

    def __calc_bb(self):
        uls = [t.ul for t in self.tiles]
        lrs = [t.lr for t in self.tiles]
        ulx, uly = min(uls)
        lrx, lry = max(lrs)
        return BoundingBox(ulx=ulx, uly=uly, lrx=lrx, lry=lry)

    def __transform(self, tile_list, scale= 1, shift_vec = (0, 0)):
        """

        :param shift_vec: Shifts the complete tiling about the vector
        :return:
        """
        bb = self.__calc_bb()
        #print ("before shift", bb)
        #dx = to_point[0] - self.bb.ulx
        #dy = to_point[1] - self.bb.uly

        ### Shift with Vector!!

        dx = shift_vec[0] * bb.lrx * scale
        dy = shift_vec[1] * bb.lry * scale

        #print ('dx dy', dx, dy)

        for tile in tile_list:
            tile.ulx *= scale
            tile.ulx += dx
            tile.uly *= scale
            tile.uly += dy
            tile.x_ext *= scale
            tile.y_ext *= scale

        bb = self.__calc_bb()
        #print ("after shift", bb)

    def __add_distance(self, to_tile_list, distance, x_shifted=False, y_shifted=False):

        for tile in to_tile_list:
            if tile.ulx == 0 and x_shifted:
                tile.ulx += distance
            if tile.uly == 0 and y_shifted:
                tile.uly += distance
            if tile.ulx > 0:
                tile.ulx += distance
            if tile.uly > 0:
                tile.uly += distance

    def clone(self, scale=1, shift_vec=(0,0), distance=0):
        l = deepcopy(self.tiles)
        #print (l)
        self.__transform(l, scale=scale, shift_vec=shift_vec)
        if distance > 0:
            self.__add_distance (l, distance,
                                 x_shifted=shift_vec[0]>0,
                                 y_shifted=shift_vec[1]>0
                                )
        print (l)
        return l

class Pine_Heel(Tiling):
    """
        Selectors:
            - 1:1
            - 2:1
            - 1:2
    """
    selectors = ['2:1', '1:2', '1:1']

    def __init__(self):
        tiles = [
            Tile(selector='2:1', ulx=0, uly=0, x_ext=2, y_ext=1),
            Tile(selector='1:1', ulx=2, uly=0, x_ext=1, y_ext=1),
            Tile(selector='1:2', ulx=3, uly=0, x_ext=1, y_ext=2),
            Tile(selector='1:1', ulx=0, uly=1, x_ext=1, y_ext=1),
            Tile(selector='1:1', ulx=1, uly=1, x_ext=1, y_ext=1),
            Tile(selector='1:1', ulx=2, uly=1, x_ext=1, y_ext=1),
            Tile(selector='1:2', ulx=3, uly=0, x_ext=1, y_ext=2),
            Tile(selector='1:1', ulx=1, uly=2, x_ext=1, y_ext=1),
            Tile(selector='1:1', ulx=2, uly=2, x_ext=1, y_ext=1),
            Tile(selector='1:1', ulx=3, uly=2, x_ext=1, y_ext=1),
            Tile(selector='2:1', ulx=2, uly=3, x_ext=2, y_ext=1),
        ]
        super().__init__(tiles)

