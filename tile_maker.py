#import svg
import base64
from dataclasses import dataclass, field
from enum import Enum
import random as ra

class Corner(Enum):
    UL = 1
    UR = 2
    LL = 3
    LR = 4

@dataclass
class BoundingBox:

    ulx: float
    uly: float
    lrx: float
    lry: float


@dataclass
class Tiling_Action:
    
    corner: Corner
    ratio: str
    displacement: float = 0.0


@dataclass
class Tile:

    ulx: float
    uly: float
    ext_x: float
    ext_y: float
    filename: str
    base64_data: field (init=False)

    def __post_init__(self):
        f = open(self.filename, 'rb')
        buffer = bytearray(f.read())
        self.base64_data = base64.b64encode(buffer).encode('ASCII')
        f.close()

    def corner(self, which):
        if which == Corner.UL:
            return (self.ulx, self.uly)
        elif which == Corner.LL:
            return (self.ulx, self.uly+self.ext_y)
        elif which == Corner.LR:
            return (self.ulx+self.ext_x, self.uly+self.ext_y)
        else:
            return (self.ulx+self.ext_x, self.uly)

    @property
    def ul(self):
        return self.corner(Corner.UL)

    @property
    def ur(self):
        return self.corner(Corner.UR)

    @property
    def ll(self):
        return self.corner(Corner.LL)

    @property
    def lr(self):
        return self.corner(Corner.LR)



class Tiling:

    def __init__(self, size, distance=0.0):
        self.size = size
        self.distance = distance
        self.tile_list = []
        self.bb = BoundingBox (ulx=0.0, uly=0.0, lrx=0.0, lry=0.0)

    def add(self, tile, position):
        self.tile_list.append(tile)

    def shift(self, dx, dy):
        pass

    def generate(self, tiles):
        pass 
        

class MyTiling(Tiling):

    def __init__(self, size, distance):

        super().__init__(size, distance)
        #self.r_st_ext = (self.size, 2*self.size)
        #self.r_ly_ext = (2*self.size, self.size)
        #self.r_sq_ext = (self.size, self.size)

    def add(self, tiling, position):
        super.add(tiling, position)

    def select__(self, from_list):
        i = ra.randint(0, len(from_list) - 1)
        elem = from_list[i]
        del from_list[i]
        return elem

    def gen(self, squares, rects_lying, rects_standing):

        r = self.select__(rects_standing)
        self.add(0.0, 0.0)

        pass


if __name__ == '__main__':
    #t = Tile(ulx=0.0,uly=0.0, ext_x=50.0, ext_y=50.0)
    ta = Tiling_Action(Corner.UR, '1:1')

