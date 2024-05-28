from dataclasses import dataclass, field
from tile_common import Corner
import tiling_factory as tf

from tilings import Tiling
from tile import Tile

@dataclass
class D:
    a: int
    b: int = 0
    #pos : tuple[int, Corner] = (None, None)

@dataclass
class E(D):
    x:str = ''

    def __init__(self, *args, **kwargs):
        print(args, kwargs)
        d = kwargs
        x = d['x']
        del kwargs['x']
        D.__init__(self, *args, **kwargs)
        self.__dict__['x'] = x
        print('S', self.__dict__)



if __name__ == '__main__':
    pass

#    t = Tiling(
#    {
#        1: Tile(selector='2:1', ulx=0, uly=0, width=2, height=1),
#        2: Tile(selector='1:1', pos=(2, 1, Corner.UR), width=1, height=1),
#        3: Tile(selector='1:2', width=1, height=2),
#        4: Tile(selector='1:1', width=1, height=1),
#        5: Tile(selector='1:1', width=1, height=1),
#        6: Tile(selector='1:1', width=1, height=1),
#        7: Tile(selector='1:2', width=1, height=2),
#        8: Tile(selector='1:1', width=1, height=1),
#        9: Tile(selector='1:1', width=1, height=1),
#        10: Tile(selector='1:1',width=1, height=1),
#        11: Tile(selector='2:1',width=2, height=1),
#        12: Tile(selector='1:1', width=1, height=1),
#    },
#    [
#        , (3, 2, Corner.UR),
#        (1, 4, Corner.LL), (5, 5, Corner.UR), (6, 5, Corner.UR),
#        (7, 4, Corner.LL), (8, 7, Corner.UR), (9, 8, Corner.UR), (10, 9, Corner.UR),
#        (11, 8, Corner.LL), (12,11, Corner.UR)
#    ]
#    )
#
    e = E(a=1, b=1, x='xxx')
    print(e, type(e))