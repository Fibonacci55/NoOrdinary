#import svg
import base64
from dataclasses import dataclass, field
import random as ra
from collections import UserDict
import glob
import datetime

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




if __name__ == '__main__':

    ra.seed(1234567)
    #t = Tile(ulx=0.0,uly=0.0, ext_x=50.0, ext_y=50.0)
    tp_full = [
            Placement(corner=Corner.UR, ratio='2:1', add_to_x_ext=1),
            Placement(corner=Corner.UR, ratio='1:1'),
            Placement(corner=Corner.UR, ratio='1:2', add_to_y_ext=1),
            Placement(corner=Corner.LL, ratio='1:1', rel_to_tile=0),
            Placement(corner=Corner.UR, ratio='1:1'),
            Placement(corner=Corner.UR, ratio='1:1'),
            Placement(corner=Corner.LL, ratio='1:2', rel_to_tile=3, add_to_y_ext=1),
            Placement(corner=Corner.UR, ratio='1:1'),
            Placement(corner=Corner.UR, ratio='1:1'),
            Placement(corner=Corner.UR, ratio='1:1'),
            Placement(corner=Corner.LL, ratio='1:1', rel_to_tile=7),
            Placement(corner=Corner.UR, ratio='2:1', add_to_x_ext=1)
    ]

    tp_half = [
        Placement(corner=Corner.NO, ratio='1:2', add_to_y_ext=1),
        Placement(corner=Corner.UR, ratio='1:1'),
        Placement(corner=Corner.UR, ratio='1:1'),
        Placement(corner=Corner.UR, ratio='1:1'),
        Placement(corner=Corner.LL, ratio='1:1', rel_to_tile=1),
        Placement(corner=Corner.UR, ratio='2:1', add_to_x_ext=1)
    ]

    collection = Tile_Collection()
    #D:\\Projects\\NoOrdinaryExes\\1_1
    collection['1:1'] = glob.glob('D:\\Projects\\NoOrdinaryEyes\\1_1_selected\\*.jpg')
    collection['1:2'] = glob.glob('D:\\Projects\\NoOrdinaryEyes\\1_2_selected\\*.jpg')
    collection['2:1'] = glob.glob('D:\\Projects\\NoOrdinaryEyes\\2_1_selected\\*.jpg')
    #print (collection.keys())

    tiling  = Tiling(50, 3)
    #tilings = [
    #            Tiling(50, 3),
    #            Tiling(50, 3),
    #            Tiling(50, 3),
    #            Tiling(50, 3),
    #            Tiling(100, 3),
    #]
    distance = 3
    #tilings = [Tiling(45,  corr_fac=0.96, distance=distance) for i in range(0, 4)]
    tilings = []
    #tilings.append(Tiling(93, corr_fac=1.02, distance=distance))
    #tilings.append(Tiling(93, corr_fac=1.02, distance=distance))
    #tilings += [Tiling(45,  corr_fac=0.96, distance=distance) for i in range(0, 4)]
    tilings += [Tiling(93,  corr_fac=1.02, distance=distance) for i in range(0, 6)]

    tot_p = [
        Placement(corner=Corner.NO, ratio='1:1'),
        Placement(corner=Corner.UR, ratio='1:1'),
        Placement(corner=Corner.LL, ratio='1:1', rel_to_tile=0),
        Placement(corner=Corner.UR, ratio='1:1'),
        Placement(corner=Corner.LL, ratio='1:1', rel_to_tile=2),
        Placement(corner=Corner.UR, ratio='1:1', rel_to_tile=4),
        #Placement(corner=Corner.UR, ratio='1:1'),
        #Placement(corner=Corner.UR, ratio='1:1'),
        #Placement(corner=Corner.LL, ratio='1:1', rel_to_tile=7),
        #Placement(corner=Corner.UR, ratio='1:1'),
    ]

    t_o_t = Tiling_Of_Tilings(distance)
    #tilings[0].add(collection, (45.0, 10), tp_half)
    for t in tilings[:]:
        t.add(collection, (45.0, 25.0), tp_full)

    t_o_t.add(tilings[:], tot_p)
    #print (tiling.tile_list)

    gen = SVG_Tiling_Generator('D:\\Projects\\NoOrdinaryEyes\\Poster\\Poster_{:%Y_%m_%d_%H_%M_%S}.svg'.format(datetime.datetime.now()))
    t_o_t.generate(gen)

    #gen.generate(tiling)
    #gen.save()
    #tiling.shift((10, 10))
