
import svgwrite
from math import floor
from wand.image import Image
import base64
from abc import ABC, abstractmethod
import svg_gen as svg
from tile import Tile
from svg_gen import create_svg_creator

class TilingGenerator(ABC):

    pass


class SVGTilingGenerator(TilingGenerator):

    def __init__(self, file_name, image_collection, size, distance, corr_factor):
        """

        :param fname: Name of file to generated
        :param image_collection: Collection of pictures to be used as tile_list
        :param size: Base size in mm of one logical unit
        :param distance: Distance between two adjacent pictures in resulting tiling
        :param corr_factor: Heuristic for correcting the dimension of picture using
                            liquid rescale
        """
        #self.dwg = svgwrite.Drawing(fname, size=("841mm", "1189mm"))
        self.file_name = file_name
        self.tile_collection = image_collection
        self.size = size
        self.distance = distance
        self.corr_factor = corr_factor

        def make_image_tile(tile: Tile, file_name: str, corr_fac: float):

            x = "%smm" % floor(tile.ulx)
            y = "%smm" % floor(tile.uly)
            x_ext = "%smm" % tile.x_ext
            y_ext = "%smm" % tile.y_ext

            infile = open(tile.filename, 'rb')
            print(tile.filename)
            with Image(file=infile) as img:
                width = img.width
                height = img.height
                if x_ext > y_ext:
                    img.liquid_rescale(width, floor(height * corr_fac))
                elif x_ext < y_ext:
                    img.liquid_rescale(floor(width * corr_fac), height)
                base64_data = base64.b64encode(img.make_blob()).decode('ASCII')

            img_data = "data:image/jpg;base64," + base64_data
            img = svgwrite.image.Image(img_data, insert=(x, y), size=(x_ext, y_ext))
            return img

    def generate(self, tiling_program: list[Tile], tile_collection, corr_fac):
        """

        :type tiling_program: object
        """

        for tile in tiling_program():

            img = self.make_image(tile, corr_fac)
            self.dwg.add (img)

    def save(self):
        self.dwg.save()
