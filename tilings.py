
from tiles import Tile
from copy import deepcopy
from dataclasses import dataclass, field
from tile_common import Position, Corner, BoundingBox

import typing



def calc_bb(tile_list : list[Tile]) -> BoundingBox:
    uls = [t.ul for t in tile_list]
    lrs = [t.lr for t in tile_list]
    ulx, uly = min(uls)
    lrx, lry = max(lrs)
    return BoundingBox(ulx=ulx, uly=uly, lrx=lrx, lry=lry)


def scale(tile_list, factor):
    """

    :param tile_list:
    :param factor:
    :return:
    """
    for tile in tile_list:
        tile.ulx *= factor
        tile.uly *= factor
        tile.x_ext *= factor
        tile.y_ext *= factor

def shift(tile_list, to_pos):
    pass

def join_tilings(tiling_collection, name, join_description):
    """

    :param name: Name of tiling
    :param join_description: String formed as NxM
    :return: A tiling list forming NxM identical tilings
    """
    rs, cs = join_description.split ('x')
    rows = int(rs)
    columns = int(cs)

    #for


def transform(tile_list, scale=1, shift_vec=(0,0), to_pos=(0, 0)):
    """

    :param self_shift_vec: Shifts the complete tiling about the vector
    :return:
    """
    bb = calc_bb(tile_list)
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

    bb = calc_bb()
    #print ("after shift", bb)

def add_distance(self, to_tile_list, distance, x_shifted=False, y_shifted=False):

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
        self.add_distance (l, distance,
                           x_shifted=shift_vec[0]>0,
                           y_shifted=shift_vec[1]>0
                           )
    print (l)
    return l


tilings = {
    'Pine_Heel' :
        [
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
        ],
}

