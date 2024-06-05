
from tilings import tilings, Tiling
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
    def transform(self, tiling : Tiling) -> list[Tile]:
        """ Does a transformation of a list of tiles """

class ScalingTransform(TilingTransformation):
    def __init__(self, factor):
        self.factor = factor
    def transform(self, tiling: Tiling) -> Tiling:
        """
        :param tiling:
        :return:
        """
        for id, tile in tiling.tiles.items():
            tile.ulx *= self.factor
            tile.uly *= self.factor
            tile.width *= self.factor
            tile.height *= self.factor

        return tiling

class MoveTransform(TilingTransformation):

    def __init__(self, to_pos: Position):
        self.to_pos = to_pos

    def transform(self, tiling: Tiling) -> Tiling:

        for tile in tiling.tiles:
            tile.ulx += self.to_pos.x
            tile.uly += self.to_pos.y

        return tiling

class AddDistanceTransform(TilingTransformation):

    def __init__(self, distance: int, x_shifted=False, y_shifted=False):
        self.distance = distance
        self.x_shifted = x_shifted
        self.y_shifted = y_shifted

    def transform(self, tiling: Tiling) -> Tiling:

        if self.x_shifted:
            tiling.tiles[1].ulx += self.distance
        if self.y_shifted:
            tiling.tiles[1].uly += self.distance

        cur_tile = tiling.tiles[1]
        if cur_tile.height > cur_tile.width:
            r = cur_tile.height // cur_tile.width - 1
            cur_tile.height += r * self.distance
        if cur_tile.height < cur_tile.width:
            r = cur_tile.width // cur_tile.height  - 1
            cur_tile.width += r * self.distance

        for edge in tiling.edge_list:
            cur_tile = tiling.tiles[edge[1]]
            rel_tile = tiling.tiles[edge[0]]
            if cur_tile.pos.related_corner == Corner.UL:
                pass
            if cur_tile.pos.related_corner == Corner.UR:
                urx, ury = rel_tile.corner(Corner.UR)
                if cur_tile.pos.positioned_corner == Corner.LR:
                    cur_tile.ulx = urx - cur_tile.width
                    cur_tile.uly = ury - cur_tile.height - self.distance
                else:
                    cur_tile.ulx = urx + self.distance
                    cur_tile.uly = ury
            if cur_tile.pos.related_corner == Corner.LL:
                if cur_tile.pos.positioned_corner == Corner.UL:
                    llx, lly = rel_tile.corner(Corner.LL)
                    cur_tile.ulx = llx
                    cur_tile.uly = lly + self.distance
            if cur_tile.pos.related_corner == Corner.LR:
                lrx, lry = rel_tile.corner(Corner.LR)
                cur_tile.ulx = lrx + self.distance
                cur_tile.uly = lry - cur_tile.height
            #if cur_tile.height > cur_tile.width:
            #    r = cur_tile.height // cur_tile.width - 1
            #    cur_tile.height += r * self.distance
            #if cur_tile.height < cur_tile.width:
            #    r = cur_tile.width // cur_tile.height  - 1
            #    cur_tile.width += r * self.distance

        return tiling



def make_single_tiling(name: str, transformations: list[TilingTransformation]) -> Tiling:
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
