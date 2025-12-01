# tiling_factory.py

from tilings import tilings
from tile import Tile
from tile_common import Position, Corner, BoundingBox
from copy import deepcopy
from abc import ABC, abstractmethod
from math import floor


class InvalidTiling(Exception):
    """Exception raised when a requested tiling name does not exist."""
    pass


def calc_bb(tile_list: list[Tile]) -> BoundingBox:
    """
    Calculates the Bounding Box for a list of tiles.

    :param tile_list: List of Tile objects.
    :return: A BoundingBox object encompassing all tiles.
    """
    uls = [t.ul for t in tile_list]
    lrs = [t.lr for t in tile_list]
    ulx, uly = min(uls)
    lrx, lry = max(lrs)
    return BoundingBox(ulx=ulx, uly=uly, lrx=lrx, lry=lry)


class TilingTransformation(ABC):
    """Abstract base class for tiling transformations."""

    @abstractmethod
    def transform(self, tiling: list[Tile]) -> list[Tile]:
        """ Does a transformation of a list of tiles """


class ScalingTransform(TilingTransformation):
    """Scales the position and dimensions of tiles by a factor."""

    def __init__(self, factor):
        self.factor = factor

    def transform(self, tiling: list[Tile]) -> list[Tile]:
        """
        Apply scaling to all tiles in the list.

        :param tiling: List of tiles to transform.
        :return: The modified list of tiles.
        """
        for tile in tiling:
            tile.ulx *= self.factor
            tile.uly *= self.factor
            tile.width *= self.factor
            tile.height *= self.factor

        return tiling


class MoveTransform(TilingTransformation):
    """Moves (translates) tiles by a specific offset."""

    def __init__(self, to_pos: Position):
        self.to_pos = to_pos

    def transform(self, tiling: list[Tile]) -> list[Tile]:
        """
        Apply translation to all tiles.

        :param tiling: List of tiles to move.
        :return: The moved list of tiles.
        """
        for tile in tiling:
            tile.ulx += self.to_pos.x
            tile.uly += self.to_pos.y

        return tiling


class AddDistanceTransform(TilingTransformation):
    """
    Adds spacing (distance) between tiles, effectively expanding the tiling
    layout while maintaining relative order.
    """

    def __init__(self, distance: int, x_shifted=False, y_shifted=False):
        """
        :param distance: The amount of space to add between tiles.
        :param x_shifted: Flag indicating if X-axis is already shifted.
        :param y_shifted: Flag indicating if Y-axis is already shifted.
        """
        self.distance = distance
        self.x_shifted = x_shifted
        self.y_shifted = y_shifted

    def __adjust_tile(self, dir: chr, tile: Tile) -> None:
        """Placeholder for internal tile adjustment logic."""
        pass

    def transform(self, tiling: list[Tile]) -> list[Tile]:
        """
        Applies the distance transformation. It processes the tiling in two passes
        (Horizontal and Vertical) to insert gaps.

        :param tiling: List of tiles.
        :return: Transformed list of tiles with added spacing.
        """

        def one_pass(tiling: list[Tile], distance: int, att1: str, att2: str, side1: str, side2: str) -> None:
            """
            Internal helper to process one dimension (X or Y).

            :param tiling: The list of tiles.
            :param distance: Distance to insert.
            :param att1: Primary attribute to sort/check (e.g., 'ulx').
            :param att2: Secondary attribute to adjust (e.g., 'uly').
            :param side1: Neighbor direction to check for gap (e.g., 'T' for Top).
            :param side2: Neighbor direction to check for edge (e.g., 'L' for Left).
            """
            ref_att = getattr(tiling[0], att1)
            dist_cnt = 0
            for tile in tiling:

                # If we moved to a new row/column
                if getattr(tile, att1) != ref_att:
                    if side1 in tile.neighbours:
                        dist_cnt = 1
                    else:
                        dist_cnt = 0
                    ref_att = getattr(tile, att1)

                # Adjust size based on aspect ratio logic
                if tile.width > tile.height:
                    ratio = floor(tile.width / tile.height)
                    tile.width += (ratio - 1) * distance
                else:
                    ratio = 1

                # Adjust position
                if getattr(tile, att2) == 0 and side2 in tile.neighbours:
                    setattr(tile, att2, distance)
                if getattr(tile, att2) > 0:
                    setattr(tile, att2, getattr(tile, att2) + dist_cnt * distance)

                dist_cnt += ratio

        # Pass 1: Sort by X then Y, process horizontal spacing
        tiling.sort(key=lambda x: (x.ulx, x.uly))
        one_pass(tiling, self.distance, 'ulx', 'uly', 'T', 'L')

        # Pass 2: Sort by Y then X, process vertical spacing
        tiling.sort(key=lambda x: (x.uly, x.ulx))
        one_pass(tiling, self.distance, 'uly', 'ulx', 'L', 'T')

        return tiling


def make_single_tiling(name: str, transformations: list[TilingTransformation]) -> list[Tile]:
    """
    Factory function to create a tiling by name and apply a series of transformations.

    :param name: Key name of the base tiling in the `tilings` dictionary.
    :param transformations: List of TilingTransformation objects to apply sequentially.
    :return: A list of transformed Tile objects.
    :raises InvalidTiling: If the name is not found.
    """
    if name not in tilings:
        raise InvalidTiling('Tiling %s not found' % name)

    tiles = deepcopy(tilings[name])
    for t in transformations:
        tiles = t.transform(tiles)

    return tiles


def join_tilings(tiling_collection, name, join_description):
    """
    Joins multiple tilings together in a grid (Not fully implemented).

    :param tiling_collection: Collection of available tilings.
    :param name: Name of tiling to replicate.
    :param join_description: String formed as NxM (e.g., "3x4").
    :return: A tiling list forming NxM identical tilings.
    """
    rs, cs = join_description.split('x')
    rows = int(rs)
    columns = int(cs)

    # Implementation incomplete in source
    # for ...
