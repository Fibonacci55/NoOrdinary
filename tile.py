from dataclasses import dataclass, field
from tile_common import Position, Corner, BoundingBox


@dataclass
class Tile:

    ulx: float = 0.0
    uly: float = 0.0
    width: float = 0.0
    height: float = 0.0
    selector: str = ''
    pos: tuple[int, Corner] = (None, None)

    def corner(self, which):
        if which == Corner.UL:
            return self.ulx, self.uly
        elif which == Corner.LL:
            print(self.ulx, self.uly+self.height)
            return self.ulx, self.uly+self.height
        elif which == Corner.LR:
            print(self.ulx + self.width, self.uly + self.height)
            return self.ulx + self.width, self.uly + self.height
        else:
            print(self.ulx+self.width, self.uly)
            return self.ulx+self.width, self.uly

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
        return (self.width, self.height)

    #def __str__(self):
    #    return "({0}, {1}) / ({2}, {3})".format(self.ulx, self.uly, self.width, self.height)

    def __lt__(self, other):
        if self.ulx < other.ulx:
            return True
        if self.ulx == other.ulx:
            if self.uly < other.uly:
                return True
        return False
