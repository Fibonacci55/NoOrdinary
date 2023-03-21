
from tilings import tilings
from tile import Tile
from tile_common import Position, Corner, BoundingBox
from copy import deepcopy
from abc import ABC, abstractmethod
from math import floor


class InvalidTiling(Exception):
    pass


def calc_bb(tile_list : list[Tile]) -> BoundingBox:
    uls = [t.ul for t in tile_list]
    lrs = [t.lr for t in tile_list]
    ulx, uly = min(uls)
    lrx, lry = max(lrs)
    return BoundingBox(ulx=ulx, uly=uly, lrx=lrx, lry=lry)

class TilingTransformation(ABC):
    @abstractmethod
    def transform(self, tiling : list[Tile]) -> list[Tile]:
        """ Does a transformation of a list of tiles """

class ScalingTransform(TilingTransformation):
    def __init__(self, factor):
        self.factor = factor
    def transform(self, tiling: list[Tile] ) -> list[Tile]:
        """
        :param tiling:
        :return:
        """
        for tile in tiling:
            tile.ulx *= self.factor
            tile.uly *= self.factor
            tile.width *= self.factor
            tile.height *= self.factor

        return tiling

class MoveTransform(TilingTransformation):

    def __init__(self, to_pos: Position):
        self.to_pos = to_pos

    def transform(self, tiling : list[Tile]) -> list[Tile]:

        for tile in tiling:
            tile.ulx += self.to_pos.x
            tile.uly += self.to_pos.y

        return tiling

class AddDistanceTransform(TilingTransformation):

    def __init__(self, distance: int, x_shifted=False, y_shifted=False):
        self.distance = distance
        self.x_shifted = x_shifted
        self.y_shifted = y_shifted


    def __adjust_tile (self, dir: chr, tile:Tile) -> None:
        pass


    #def transform(self, tiling: list[Tile]) -> list[Tile]:

    #    tiling.sort(key=lambda x: (x.ulx, x.uly))
    #    bef_tiles = []
    #    aft_tiles = []
#
#        cur_x = tiling[0].ulx
#        dist_cnt = 0
#        for tile in tiling:
#            bef_tiles.append(deepcopy(tile))
#
#            if tile.ulx != cur_x:
#                if 'T' in tile.neighbours:
#                    dist_cnt = 1
#                else:
#                    dist_cnt = 0
#                cur_x = tile.ulx
#            if tile.height > tile.width:
#                ratio = floor(tile.height / tile.width)
#                tile.height += (ratio - 1) * self.distance
#            else:
#                ratio = 1
#            if tile.uly == 0 and self.y_shifted:
#                tile.uly = self.distance
#            if tile.uly > 0:
#                tile.uly += dist_cnt * self.distance
#
#            dist_cnt += ratio
#
#        print("=====================================")
#        tiling.sort(key=lambda x: (x.uly, x.ulx))
#
#        cur_y = tiling[0].uly
#        dist_cnt = 0
#        for tile in tiling:
#
#            if tile.uly != cur_y:
#                if 'L' in tile.neighbours:
#                    dist_cnt = 1
#                else:
#                    dist_cnt = 0
#                cur_y = tile.uly
#            if tile.width > tile.height:
#                ratio = floor(tile.width / tile.height)
#                tile.width += (ratio - 1) * self.distance
#            else:
#                ratio = 1
#            if tile.ulx == 0 and self.x_shifted:
#                tile.ulx = self.distance
#            if tile.ulx > 0:
#                tile.ulx += dist_cnt * self.distance
#
#            dist_cnt += ratio
#
#            aft_tiles.append(deepcopy(tile))
#
#        tiling.sort(key=lambda x: (x.ulx, x.uly))
#
#        for i in range(0, len(tiling)-1):
#            print(bef_tiles[i], tiling[i])
#
#        return tiling



def make_single_tiling(name: str, transformations: list[TilingTransformation]) -> list[Tile]:
    if name not in tilings:
       raise InvalidTiling('Tiling %s not found' % name)

    tiles = deepcopy(tilings[name])
    for t in transformations:
       tiles = t.transform(tiles)

    return tiles


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
