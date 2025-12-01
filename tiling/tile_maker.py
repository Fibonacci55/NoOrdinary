# tile_maker.py
# import svg
import base64
from dataclasses import dataclass, field
import random as ra
from collections import UserDict
import glob
import datetime


# Note: Placement, Tile, Tiling, SVG_Tiling_Generator, Tile_Collection
# are assumed to be imported from other modules or defined elsewhere in the full project.

class Tiling_Of_Tilings:
    """
    Manages a meta-tiling structure where multiple individual tilings
    are arranged relative to each other.
    """

    def __init__(self, distance):
        """
        :param distance: The spacing distance between the sub-tilings.
        """
        self.distance = distance
        self.list_of_tilings = []

    def add_dist(self, idx, to_which):
        """
        Calculates the coordinate offset for a new tiling based on a reference tiling's corner.

        :param idx: Index of the reference tiling in the list.
        :param to_which: The corner of the reference tiling to attach to (UL, LL, LR, UR).
        :return: A tuple (x, y) or BoundingBox representing the start point.
        """
        bb = self.list_of_tilings[idx].bb

        if to_which == Corner.UL:
            return bb
        elif to_which == Corner.LL:
            return (bb.ulx, bb.lry + self.distance)
        elif to_which == Corner.LR:
            return bb
        elif to_which == Corner.UR:
            return (bb.lrx + self.distance, bb.uly)
        else:
            return (0.0, 0.0)

    def add(self, tilings, tiling_program):
        """
        Adds a list of tilings to the meta-structure according to a program.

        :param tilings: List of Tiling objects to add.
        :param tiling_program: List of Placement instructions corresponding to the tilings.
        """
        for i, tiling in enumerate(tilings):
            instr = tiling_program[i]
            tiling.calc_bb()

            # Determine reference tile index (handle relative indexing)
            idx = i + instr.rel_to_tile if instr.rel_to_tile < 0 else instr.rel_to_tile

            # Determine start point (0,0 for the first one, or calculated offset)
            start_point = (tiling.bb.ulx, tiling.bb.uly) if len(self.list_of_tilings) == 0 else self.add_dist(idx,
                                                                                                              instr.corner)

            tiling.shift(start_point)
            self.list_of_tilings.append(tiling)

    def generate(self, tiling_gen):
        """
        Generates the visual output for all stored tilings.

        :param tiling_gen: An instance of a generator (e.g., SVG_Tiling_Generator).
        """
        for tiling in self.list_of_tilings:
            tiling_gen.generate(tiling)
        tiling_gen.save()


if __name__ == '__main__':

    ra.seed(1234567)

    # Define placement strategies for full and half tiles
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

    # Initialize collection and load images
    collection = Tile_Collection()
    collection['1:1'] = glob.glob('D:\\Projects\\NoOrdinaryEyes\\1_1_selected\\*.jpg')
    collection['1:2'] = glob.glob('D:\\Projects\\NoOrdinaryEyes\\1_2_selected\\*.jpg')
    collection['2:1'] = glob.glob('D:\\Projects\\NoOrdinaryEyes\\2_1_selected\\*.jpg')

    # Create base tilings
    tiling = Tiling(50, 3)
    distance = 3
    tilings = []

    # Add tilings to the list (6 tilings of size 93)
    tilings += [Tiling(93, corr_fac=1.02, distance=distance) for i in range(0, 6)]

    # Define the meta-layout program
    tot_p = [
        Placement(corner=Corner.NO, ratio='1:1'),
        Placement(corner=Corner.UR, ratio='1:1'),
        Placement(corner=Corner.LL, ratio='1:1', rel_to_tile=0),
        Placement(corner=Corner.UR, ratio='1:1'),
        Placement(corner=Corner.LL, ratio='1:1', rel_to_tile=2),
        Placement(corner=Corner.UR, ratio='1:1', rel_to_tile=4),
    ]

    # Create the meta-tiling manager
    t_o_t = Tiling_Of_Tilings(distance)

    # Populate individual tilings with images/layout
    for t in tilings[:]:
        t.add(collection, (45.0, 25.0), tp_full)

    # Add individual tilings to the meta-tiling
    t_o_t.add(tilings[:], tot_p)

    # Generate the final SVG
    gen = SVG_Tiling_Generator(
        'D:\\Projects\\NoOrdinaryEyes\\Poster\\Poster_{:%Y_%m_%d_%H_%M_%S}.svg'.format(datetime.datetime.now()))
    t_o_t.generate(gen)
