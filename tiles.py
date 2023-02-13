from dataclasses import dataclass, field
from tile_common import Position, Corner, BoundingBox


@dataclass
class Tile:

    ulx: float
    uly: float
    x_ext: float
    y_ext: float
    selector: str

    def corner(self, which):
        if which == Corner.UL:
            return self.ulx, self.uly
        elif which == Corner.LL:
            return self.ulx, self.uly+self.y_ext
        elif which == Corner.LR:
            return self.ulx+self.x_ext, self.uly+self.y_ext
        else:
            return self.ulx+self.x_ext, self.uly

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

@dataclass
class ImageTile (Tile):
    filename: str

def tiles2image_tiles (tile_list, collection):

    for tile in tile_list:
        pass
