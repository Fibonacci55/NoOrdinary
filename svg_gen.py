from abc import ABC, abstractmethod
from dataclasses import dataclass
#from wand.image import Image
#import base64
from math import floor
import urllib



@dataclass
class DocumentOptions:

    width: int
    height: int
    unit: str


class SvgCreator(ABC):

    @abstractmethod
    def create_document(self, name: str, options: DocumentOptions) -> None:
        """ Creates a SVG document """

    @abstractmethod
    def create_group(self) -> int:
        """ Creates a new group of the document, returns the id of the group"""

    @abstractmethod
    def save_document(self):
        """ Saves a SVG document"""

    @abstractmethod
    def create_image (img_file : str, width : int, height: int, ulx : int, uly: int) -> object:
        """ Creates an SVG image with dimension widthxheight. upper left position at (ulx, uly) """

    def create_rectangle(self, width: int, height: int, ulx: int, uly: int):
        """ Creates an SVG rectangle at position ulx, uly awith dimensions witdh and height """
    @abstractmethod
    def add_to_canvas(self, element) -> None:
        """ Adds an element to the image canvas """

    @abstractmethod
    def add_to_group(self, grp_id: int, element: object) -> None:
        """ Adds an element to the group with id grp_id"""

    def get_group(self, grp_id: int) -> object:
        """ Retrieves group with id grp_id """

import svg

class MyImg(svg.Image):

    xlink__href: str

    def __init__(self, *args, **kwargs):
        s = kwargs['xlink__href']
        del kwargs['xlink__href']
        svg.Image.__init__(self, *args, **kwargs)
        self.__dict__['xlink__href'] = s


class SvgDraw(SvgCreator):

    def __init__(self):
        self.groups = []

    def _unit(self, dim):
        return "%s%s" % (dim, self.options.unit)

    def create_document(self, name: str, options: DocumentOptions) -> None:
        self.name = name
        self.options = options
        width = self._unit(options.width)
        height = self._unit(options.height)
        #width = options.width
        #height = options.height
        self.canvas = svg.SVG(svg.ViewBoxSpec(0, 0, width, height), width=width, height=height, elements=[])
        return self.canvas

    def add_to_canvas(self, element) -> None:
        self.canvas.elements.append(element)
    def create_group(self) -> int:
        self.groups.append(svg.G(elements=[]))
        return len(self.groups) - 1

    def create_image(self, img_data : str, width : int, height: int, ulx : int, uly: int) -> object:
        #print (width, height)
        u = lambda x: self._unit(x)
        #u = lambda x: x
        #svg_img = svg.Image(src=img_data, x=u(ulx), y=u(uly), width=u(width), height=u(height))
        svg_img = MyImg(xlink__href=img_data, x=u(ulx), y=u(uly), width=u(width), height=u(height))
        return svg_img

    def create_rectangle(self, width: int, height: int, ulx: int, uly: int):
        #r = svg.Rect(width=width, height=height,
        #             x=ulx, y=uly,
        #             style="fill:none;stroke:#000000;stroke-opacity:1")

        r = svg.Path(
            d=[svg.MoveTo(ulx, uly),
               svg.LineTo(ulx+width, uly),
               svg.LineTo(ulx+width, uly+height),
               svg.LineTo(ulx, uly+height),
               svg.ClosePath()],
            style="fill:none;stroke:#000000;stroke-opacity:1")

        return r

    def add_to_group(self, grp_id: int, element: object) -> None:
        self.groups[grp_id].elements.append(element)

    def get_group(self, grp_id: int) -> object:
        return self.groups[grp_id]
    def save_document(self):
        outf = open(self.name)
        print(self.canvas, file=outf)
        outf.close()


def create_svg_creator() -> SvgCreator:
    return SvgDraw()