from dataclasses import dataclass, field
from tile_common import Corner
import tiling_factory as tf
from tiling_generator import SvgRectTilingGenerator, ImageTilingGenerator
from tiledatacollection import const_sel_factory, SvgFrameCollection,ImageTileDataCollection, ord_sel_factory
from svg_gen import DocumentOptions

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

    scale = tf.ScalingTransform(factor=70)
    d = tf.AddDistanceTransform(distance=5)
    # tiles = tf.make_single_tiling('Cobbiesstone_90', transformations=[scale, d])
    #t = Tile(selector='2:1', pos=(1, Corner.LR, Corner.LL), width=2, height=1),
    #tiles = tf.make_single_tiling('Roman_50', transformations=[scale, d])
    tiles = tf.make_single_tiling('Prague', transformations=[scale, d])
    #tiles = tf.make_single_tiling('Roman_50', transformations=[scale])
    #tiles = tf.make_single_tiling('Roman_5', transformations=[scale, d])
    #coll = SvgFrameCollection()
    coll = ImageTileDataCollection(base_path="D:\\Projects\\Prague_2024")
    img_gen = ImageTilingGenerator()
    #img_gen = SvgRectTilingGenerator()
    coll.add_selector(selector="1:1", sel_mthd_factory=ord_sel_factory)
    coll.add_selector(selector="2:1", sel_mthd_factory=ord_sel_factory)
    coll.add_selector(selector="1:2", sel_mthd_factory=ord_sel_factory)
    coll.add_selector(selector="2:2", sel_mthd_factory=ord_sel_factory)

    # coll.add_selector(selector="1:1", sel_mthd_factory=ord_sel_factory)
    # coll.add_selector(selector="2:1", sel_mthd_factory=ord_sel_factory)
    # coll.add_selector(selector="1:2", sel_mthd_factory=ord_sel_factory)

    #coll.add_selector(selector="1:1", sel_mthd_factory=const_sel_factory)
    #coll.add_selector(selector="2:1", sel_mthd_factory=const_sel_factory)
    #coll.add_selector(selector="1:2", sel_mthd_factory=const_sel_factory)
    #coll.add_selector(selector="2:2", sel_mthd_factory=const_sel_factory)
    #coll.add_selector(selector="3:3", sel_mthd_factory=const_sel_factory)
    #coll.add_selector(selector="3:2", sel_mthd_factory=const_sel_factory)
    #coll.add_selector(selector="2:3", sel_mthd_factory=const_sel_factory)
    # print(coll.image_collection['1:1'])
    #img_gen.generate("D:\\Temp\\Test.svg", tiles, coll, DocumentOptions(width=300, height=300, unit="mm"))
    img_gen.generate("D:\\Temp\\Yogi\\prague_poster.svg", tiles, coll, DocumentOptions(width=300, height=300, unit="mm"))
