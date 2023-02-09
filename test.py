import base64
import random as ra
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

from svgwrite.extensions import Inkscape
import svgwrite

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

if __name__ == '__main__':
    pass
    #fname = "D:\\Projects\\NoOrdinaryExes\\1_2\\131342501_858098905110778_4492636055371751330_n_cr.jpg"
    #outf_name = "D:\\Projects\\NoOrdinaryExes\\poster_1.svg"
    #img = encode(fname)
    #img_href = "data:image/jpg;base64," + img.decode('ASCII')
    #make_image(outf_name, img_href)

    import tilings as tp

    p = tp.Pine_Heel().clone()
    p = tp.Pine_Heel().clone(shift_vec=(1,0))
    p = tp.Pine_Heel().clone(scale=10)
    p = tp.Pine_Heel().clone(scale=10, distance=10)
    p = tp.Pine_Heel().clone(scale=10, shift_vec=(1,0), distance=10)
