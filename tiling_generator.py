
import svgwrite
from math import floor
from wand.image import Image
import base64


class SVG_Tiling_Generator:

    def __init__(self, fname, tile_collection, size, distance, corr_factor):
        """

        :param fname: Name of file to generated
        :param tile_collection: Collection of pictures to be used as tiles
        :param size: Base size in mm of one logical unit
        :param distance: Distance between two adjacent pictures in resulting tiling
        :param corr_factor: Heuristic for correcting the dimension of picture using
                            liquid rescale
        """
        self.dwg = svgwrite.Drawing(fname, size=("841mm", "1189mm"))
        self.tile_collection = tile_collection
        self.size = size
        self.distance = distance
        self.corr_factor = corr_factor

    def generate(self, tiling_program, tile_collection, corr_fac):
        def make_image (tile, corr_fac):

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

        for tile in tiling_program():

            img = make_image(tile, corr_fac)
            self.dwg.add (img)

    def save(self):
        self.dwg.save()
