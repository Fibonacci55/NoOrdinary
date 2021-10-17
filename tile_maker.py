#import svg
import base64
from dataclasses import dataclass, field
from enum import Enum
import random as ra
from collections import UserDict
import glob
import svgwrite
from math import floor
from wand.image import Image
import datetime

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
    
    ratio: str
    corner: Corner = field(default=Corner.NO)
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

    #def __post_init__(self):
    #    f = open(self.filename, 'rb')
    #    buffer = bytearray(f.read())
    #    self.base64_data = base64.b64encode(buffer).decode('ASCII')
    #    f.close()

    def __post_init__(self):
        infile = open(self.filename, 'rb')
        print (self.filename)
        with Image(file=infile) as img:
            width = img.width
            height = img.height
            if self.x_ext > self.y_ext:
                img.liquid_rescale(floor(width), floor(height*0.96))
            elif self.x_ext < self.y_ext:
                img.liquid_rescale(floor(width*0.96), floor(height*1.0))
            self.base64_data = base64.b64encode(img.make_blob()).decode('ASCII')

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
        elif to_which == Corner.UR:
            return (pos[0] + self.distance, pos[1])
        else:
            return (0.0, 0.0)

    def add(self, tiles, start_position, tiling_program):

        local_tile_list = []
        for i, instr in enumerate(tiling_program):
            idx = i + instr.rel_to_tile if instr.rel_to_tile < 0 else instr.rel_to_tile
            #print ('Index', i, idx)
            start_x, start_y = start_position if len(local_tile_list) == 0 else self.add_dist(local_tile_list[idx].corner(instr.corner), instr.corner)
            #print ("add", start_x, start_y)
            ### TBD handle displacement
            x_ext = float(instr.ratio.split(':')[0])
            y_ext = float(instr.ratio.split(':')[1])
            fname = tiles.select(instr.ratio)
            t = Tile(ulx=start_x,
                     uly=start_y,
                     x_ext=x_ext * self.size + self.distance * instr.add_to_x_ext,
                     y_ext=y_ext * self.size + self.distance * instr.add_to_y_ext,
                     filename=fname)
            local_tile_list.append(t)

        self.tile_list += local_tile_list

    def calc_bb(self):
        uls = [t.ul for t in self.tile_list]
        lrs = [t.lr for t in self.tile_list]
        self.bb.ulx, self.bb.uly = min(uls)
        self.bb.lrx, self.bb.lry = max(lrs)

    def shift(self, to_point):
        self.calc_bb()
        print ("before shift", self.bb, to_point)
        dx = to_point[0] - self.bb.ulx
        dy = to_point[1] - self.bb.uly
        for tile in self.tile_list:
            tile.ulx += dx
            tile.uly += dy
        self.calc_bb()
        print ("after shift", self.bb)

    def generate(self, tiles):
        pass 
        

class Tiling_Of_Tilings:

    def __init__(self, distance):

        self.distance = distance
        self.list_of_tilings = []

    def add_dist(self, idx, to_which):

        bb = self.list_of_tilings[idx].bb

        if to_which == Corner.UL:
            return bb
        elif to_which == Corner.LL:
            return (bb.ulx,  bb.lry + self.distance)
        elif to_which == Corner.LR:
            return bb
        elif to_which == Corner.UR:
            return (bb.lrx + self.distance, bb.uly)
        else:
            return (0.0, 0.0)

    def add(self, tilings, tiling_program):
        for i, tiling in enumerate(tilings):
            instr = tiling_program[i]
            tiling.calc_bb()
            idx = i + instr.rel_to_tile if instr.rel_to_tile < 0 else instr.rel_to_tile
            start_point = (tiling.bb.ulx, tiling.bb.uly) if len(self.list_of_tilings) == 0 else self.add_dist(idx, instr.corner)
            tiling.shift(start_point)
            self.list_of_tilings.append(tiling)

    def generate(self, tiling_gen):
        for tiling in self.list_of_tilings:
            tiling_gen.generate(tiling)
        tiling_gen.save()


class SVG_Tiling_Generator:

    def __init__(self, fname):
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
            #print (tile)
            img = make_image(tile.base64_data, tile.ul, tile.ext)
            self.dwg.add (img)

    def save(self):
        self.dwg.save()


if __name__ == '__main__':

    ra.seed(1234567)
    #t = Tile(ulx=0.0,uly=0.0, ext_x=50.0, ext_y=50.0)
    tp = [
            Tiling_Action(corner=Corner.UR, ratio='2:1', add_to_x_ext=1),
            Tiling_Action(corner=Corner.UR, ratio='1:1'),
            Tiling_Action(corner=Corner.UR, ratio='1:2', add_to_y_ext=1),
            Tiling_Action(corner=Corner.LL, ratio='1:1', rel_to_tile=0),
            Tiling_Action(corner=Corner.UR, ratio='1:1'),
            Tiling_Action(corner=Corner.UR, ratio='1:1'),
            Tiling_Action(corner=Corner.LL, ratio='1:2', rel_to_tile=3, add_to_y_ext=1),
            Tiling_Action(corner=Corner.UR, ratio='1:1'),
            Tiling_Action(corner=Corner.UR, ratio='1:1'),
            Tiling_Action(corner=Corner.UR, ratio='1:1'),
            Tiling_Action(corner=Corner.LL, ratio='1:1', rel_to_tile=7),
            Tiling_Action(corner=Corner.UR, ratio='2:1', add_to_x_ext=1)
    ]

    collection = Tile_Collection()
    #D:\\Projects\\NoOrdinaryExes\\1_1
    collection['1:1'] = glob.glob('D:\\Projects\\NoOrdinaryExes\\1_1\\*.jpg')
    collection['1:2'] = glob.glob('D:\\Projects\\NoOrdinaryExes\\1_2\\*.jpg')
    collection['2:1'] = glob.glob('D:\\Projects\\NoOrdinaryExes\\2_1\\*.jpg')
    #print (collection.keys())

    tiling  = Tiling(50, 3)
    #tilings = [
    #            Tiling(50, 3),
    #            Tiling(50, 3),
    #            Tiling(50, 3),
    #            Tiling(50, 3),
    #            Tiling(100, 3),
    #]
    tilings = [Tiling(45, 3) for i in range(0, 4)]
    tilings.append(Tiling(90, 3))

    tot_p = [
        Tiling_Action(corner=Corner.NO, ratio='1:1'),
        Tiling_Action(corner=Corner.UR, ratio='1:1'),
        Tiling_Action(corner=Corner.LL, ratio='1:1', rel_to_tile=0),
        Tiling_Action(corner=Corner.UR, ratio='1:1'),
        Tiling_Action(corner=Corner.UR, ratio='1:1', rel_to_tile=1),
    ]

    t_o_t = Tiling_Of_Tilings(3)
    for t in tilings:
        t.add(collection, (10.0, 10.0), tp)

    t_o_t.add(tilings, tot_p)
    #print (tiling.tile_list)

    gen = SVG_Tiling_Generator('D:\\Projects\\NoOrdinaryExes\\Poster\\Poster_{:%Y_%m_%d_%H_%M_%S}.svg'.format(datetime.datetime.now()))
    t_o_t.generate(gen)

    #gen.generate(tiling)
    #gen.save()
    #tiling.shift((10, 10))
