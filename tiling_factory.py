
from tilings import tilings
from tile import Tile
from tile_common import Position, Corner, BoundingBox
from copy import deepcopy
from abc import ABC, abstractmethod


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
            tile.x_ext *= self.factor
            tile.y_ext *= self.factor

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

    def transform(self, tiling: list[Tile]) -> list[Tile]:

        for tile in tiling:
            if tile.ulx == 0 and self.x_shifted:
                tile.ulx += self.distance
            if tile.uly == 0 and self.y_shifted:
                tile.uly += self.distance
            if tile.ulx > 0:
                tile.ulx += self.distance
            if tile.uly > 0:
                tile.uly += self.distance

        return tiling


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
