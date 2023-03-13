import base64
import random as ra
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from wand.image import Image
from math import floor
import urllib

import svgwrite

from typing import Optional

def xxx(l):
    i = ra.randint(0, len(l)-1)
    print (l, i)
    del l[i]

def encode(filename):

    print('Encode')
    f = open(filename, 'rb')
    buffer = bytearray(f.read())
    print(len(buffer))
    s = base64.b64encode(buffer)
    print (len(s))
    return (s)


def make_image(fname, image):

    dwg = svgwrite.Drawing(fname, size=("841mm", "1189mm"))
    img = svgwrite.image.Image(image, insert=("100", "100"), size=("10mm", "20mm"))
    dwg.add(img)

    dwg.save()

import svg
#import svg_gen
class MyImage(svg.Image):

    bla : Optional[str] = ''


def make_image_2(fname):

    infile = open(fname, 'rb')
    with Image(file=infile) as img:
        width = img.width
        height = img.height
        if width > height:
            img.liquid_rescale(width, floor(height * 0.9))
        elif width < height:
            img.liquid_rescale(floor(width * 0.9), height)
        base64_data = base64.b64encode(img.make_blob()).decode('ASCII')

    img_data = "data:image/jpg;base64," + base64_data
    #svg_img = svg.Image(href=img_data, x="10", y="10", width="20", height="20" )
    img_ref = 'file:' + urllib.request.pathname2url(fname)
    svg_img = svg.Image(xlink__href=img_data, x="10", y="10", width="20", height="20" )

    #canvas = svg.SVG(svg.ViewBoxSpec(0, 0, 100, 100), elements=[svg_img])
    canvas = svg.SVG(elements=[svg_img])

    outf = open("D:\\Temp\\out_2.svg", "w")
    print(canvas, file=outf)
    #outf.write(canvas)
    outf.close()

@dataclass
class B(ABC):
    x: str = field(init=False)

class Tile_Selector(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def __call__(self, from_list):
        pass

class Random_Selector(Tile_Selector):

    def __call__(self, from_list):
        v = ra.choice (from_list)
        from_list.remove (v)
        return v

class Ordered_Selector(Tile_Selector):

    def __call__(self, from_list):
        v = from_list.pop(0)

def bla (sel=Ordered_Selector()):
    print (sel.__class__)


class X:

    def G__init__(self):
        pass

    def do(self):
        self.xxx = 'Done'

#from copy import deepcopy

def bla(l):

    l[0] += 3



@dataclass
class base:

    x: str

@dataclass
class child(base):

    y : str

from tile import Tile
from operator import attrgetter


if __name__ == '__main__':
    pass
    fname = "D:\\Projects\\NoOrdinaryEyes\\1_1\\182385403_10159279385843501_1771795695471674866_n_cr.jpg"
    #make_image_2(fname)
    #b = base(x='x', y='xxx')
    #c = child(x='xx', y='y')
    #print (b, c)
    #c = svg.SVG(elements=[])
    #c.elements.append(svg.Image())
    l = [
        Tile(selector='1:1', ulx=2, uly=0, width=1, height=1),
        Tile(selector='1:2', ulx=3, uly=0, width=1, height=2),
        Tile(selector='1:1', ulx=0, uly=1, width=1, height=1),
        Tile(selector='2:1', ulx=0, uly=0, width=2, height=1),
        Tile(selector='1:1', ulx=1, uly=1, width=1, height=1),
        Tile(selector='1:1', ulx=2, uly=1, width=1, height=1),
        Tile(selector='1:2', ulx=0, uly=2, width=1, height=2),
        Tile(selector='1:1', ulx=1, uly=2, width=1, height=1),
        Tile(selector='1:1', ulx=2, uly=2, width=1, height=1),
        Tile(selector='1:1', ulx=3, uly=2, width=1, height=1),
        Tile(selector='2:1', ulx=2, uly=3, width=2, height=1),
        Tile(selector='1:1', ulx=1, uly=3, width=1, height=1),
    ]

    l.sort(key=lambda x: (x.ulx, x.uly))
    for t in l:
        print(t)

    l.sort(key=lambda x: (x.uly, x.ulx))
    for t in l:
        print(t)
