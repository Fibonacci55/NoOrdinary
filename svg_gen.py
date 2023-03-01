from abc import ABC, abstractmethod
from dataclasses import dataclass
from wand.image import Image
import base64
from math import floor



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

    def create_image (img_file : str, width : int, height: int, ulx : int, uly: int, corr_fac: float) -> object:
        """ Creates an SVG image with dimension widthxheight. upper left position at (ulx, uly) """


import svg

class SvgDraw(SvgCreator):


    def __init__(self):
        pass

    def create_document(self, name: str, options: DocumentOptions) -> None:
        self.options = options
        self.canvas = svg.SVG(svg.ViewBoxSpec(0, 0, options.width, options.height))


    def create_image(img_file : str, width : int, height: int, ulx : int, uly: int, corr_fac: float) -> object:
        with Image(file=img_file) as img:
            width = img.width
            height = img.height
            if width > height:
                img.liquid_rescale(width, floor(height * corr_fac))
            elif width < height:
                img.liquid_rescale(floor(width * corr_fac), height)
            base64_data = base64.b64encode(img.make_blob()).decode('ASCII')

        img_data = "data:image/jpg;base64," + base64_data
        svg_img = svg.Image(data=img_data, )


def create_svg_creator() -> SvgCreator:
    return SvgDraw()