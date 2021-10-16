#import svg
import base64
from dataclasses import dataclass, field
from enum import Enum
import random as ra
from collections import UserDict
import glob
import svgwrite
from math import floor

class Corner(Enum):
    NO = 0
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

    def __str__(self):
        return "({0}, {1}) / ({2}, {3})".format(self.ulx, self.uly, self.lry, self.lry)

@dataclass
class Tiling_Action:
    
    corner: Corner = Corner.NO
    ratio: str
    rel_to_tile : int = -1
    displacement: float = 0.0
    add_to_x_ext: float = 0.0
    add_to_y_ext: float = 0.0

@dataclass
class Tile:

    ulx: float
    uly: float
    x_ext: float
    y_ext: float
    filename: str
    base64_data: str = None

    def __post_init__(self):
        f = open(self.filename, 'rb')
        buffer = bytearray(f.read())
        self.base64_data = base64.b64encode(buffer).decode('ASCII')
        f.close()

    def corner(self, which):
        if which == Corner.UL:
            return (self.ulx, self.uly)
        elif which == Corner.LL:
            return (self.ulx, self.uly+self.y_ext)
        elif which == Corner.LR:
            return (self.ulx+self.x_ext, self.uly+self.y_ext)
        else:
            return (self.ulx+self.x_ext, self.uly)

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

    @property
    def ext(self):
        return (self.x_ext, self.y_ext)

    def __str__(self):
        return "({0}, {1}) / ({2}, {3})".format(self.ulx, self.uly, self.x_ext, self.y_ext)

class Tile_Collection(UserDict):

    def __init__(self):
        super().__init__()

    def select(self, selector):
        #print ('select', selector)
        #print(self.data[selector])
        if selector in self.data:
            i = ra.randint(0, len(self.data[selector]) - 1)
            res = self.data[selector][i]
            del self.data[selector][i]
            if len(self.data[selector]) == 0:
                del self.data[selector]
            return res
        else:
            raise KeyError


class Tiling:

    """"

    """

    def __init__(self, size, distance=0.0):
        self.size = size
        self.distance = distance
        self.tile_list = []
        self.bb = BoundingBox (ulx=0.0, uly=0.0, lrx=0.0, lry=0.0)

    def add_dist(self, pos, to_which):
        if to_which == Corner.UL:
            return pos
        elif to_which == Corner.LL:
            return (pos[0], pos[1] + self.distance)
        elif to_which == Corner.LR:
            return pos
        else:
            return (pos[0] + self.distance, pos[1])

    def add(self, tiles, start_position, tiling_program):

        local_tile_list = []
        instr = tiling_program[0]
        fname = tiles.select (instr.ratio)
        x_ext = float(instr.ratio.split(':')[0])
        y_ext = float(instr.ratio.split(':')[1])
        t = Tile(ulx=start_position[0],
                 uly=start_position[1],
                 x_ext=x_ext * self.size + self.distance * instr.add_to_x_ext,
                 y_ext=y_ext * self.size + self.distance * instr.add_to_y_ext,
                 filename=fname)
        local_tile_list.append(t)
        for i, instr in enumerate(tiling_program[1:]):
            idx = 1 + i + instr.rel_to_tile if instr.rel_to_tile < 0 else instr.rel_to_tile
            print ('Index', i, idx)
            start_x, start_y = self.add_dist(local_tile_list[idx].corner(instr.corner), instr.corner)
            #print (start_x, start_y)
            ### TBD handle displacement
            x_ext = float(instr.ratio.split(':')[0])
            y_ext = float(instr.ratio.split(':')[1])
            fname = tiles.select(instr.ratio)
            t = Tile(ulx=start_x,
                     uly=start_y,
                     x_ext=x_ext * self.size + self.distance * instr.add_to_x_ext,
                     y_ext=y_ext * self.size + self.distance * instr.add_to_y_ext,
                     #x_ext=x_ext * self.size + (self.distance if instr.add_to_x_ext else 0),
                     #y_ext=y_ext * self.size + (self.distance if instr.add_to_y_ext else 0),
                     #x_ext=x_ext * self.size,
                     #y_ext=y_ext * self.size,
                     filename=fname)
            local_tile_list.append(t)
        self.tile_list += local_tile_list

    def calc_bb__(self):
        uls = [t.ul for t in self.tile_list]
        lrs = [t.lr for t in self.tile_list]
        self.bb.ulx, self.bb.uly = min(uls)
        self.bb.lrx, self.bb.lry = max(lrs)

    def shift(self, to_point):
        self.calc_bb__()
        print ("Shift", self.bb)
        for tile in self.tile_list:
            pass

    def generate(self, tiles):
        pass 
        

class Tiling_Of_Tiligs:

    def __init__(self, distance):

        self.distance = distance
        self.list_of_tilings = []

    def add(self, tilings, pred, corner=None):



    #def select__(self, from_list):
    #    i = ra.randint(0, len(from_list) - 1)
    #    elem = from_list[i]
    #    del from_list[i]
    #    return elem

    def gen(self, squares, rects_lying, rects_standing):
        r = self.select__(rects_standing)
        self.add(0.0, 0.0)

        pass

class SVG_Tiling_Generator:

    def __init__(self, fname):
        pass
        self.dwg = svgwrite.Drawing(fname, size=("841mm", "1189mm"))

    def generate(self, tiling):
        def make_image (data, pos, size):
            x = "%smm" % floor(pos[0])
            y = "%smm" % floor(pos[1])
            #print ((x, y))

            x_ext = "%smm" % size[0]
            y_ext = "%smm" % size[1]
            img_data = "data:image/jpg;base64," + data
            img = svgwrite.image.Image(img_data, insert=(x, y), size=(x_ext, y_ext))
            return img


        for tile in tiling.tile_list:
            print (tile)
            img = make_image(tile.base64_data, tile.ul, tile.ext)
            self.dwg.add (img)

        self.dwg.save()


if __name__ == '__main__':
    #t = Tile(ulx=0.0,uly=0.0, ext_x=50.0, ext_y=50.0)
    tp = [
            Tiling_Action(Corner.UR, '2:1', add_to_x_ext=1),
            Tiling_Action(Corner.UR, '1:1'),
            Tiling_Action(Corner.UR, '1:2', add_to_y_ext=1),
            Tiling_Action(Corner.LL, '1:1', rel_to_tile=0),
            Tiling_Action(Corner.UR, '1:1'),
            Tiling_Action(Corner.UR, '1:1'),
            Tiling_Action(Corner.LL, '1:2', rel_to_tile=3, add_to_y_ext=1),
            Tiling_Action(Corner.UR, '1:1'),
            Tiling_Action(Corner.UR, '1:1'),
            Tiling_Action(Corner.UR, '1:1'),
            Tiling_Action(Corner.LL, '1:1', rel_to_tile=7),
            Tiling_Action(Corner.UR, '2:1', add_to_x_ext=1)
    ]

    collection = Tile_Collection()
    #D:\\Projects\\NoOrdinaryExes\\1_1
    collection['1:1'] = glob.glob('D:\\Projects\\NoOrdinaryExes\\1_1\\*.jpg')
    collection['1:2'] = glob.glob('D:\\Projects\\NoOrdinaryExes\\1_2\\*.jpg')
    collection['2:1'] = glob.glob('D:\\Projects\\NoOrdinaryExes\\2_1\\*.jpg')
    #print (collection.keys())

    tiling  = My_Tiling(50, 3)
    tiling.add(collection, (0.0, 0.0), tp)
    #print (tiling.tile_list)

    gen = SVG_Tiling_Generator('D:\\Projects\\NoOrdinaryExes\\Poster\\Poster.svg')

    gen.generate(tiling)
    tiling.shift((10, 10))
