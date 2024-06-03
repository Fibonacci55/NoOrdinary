import math

#import svgwrite
#from wand.image import Image
import base64
from math import ceil, modf
from tile import Tile
from svg_gen import create_svg_creator, DocumentOptions
from tiledatacollection import TileDataCollection
from tilings import Tiling
from abc import ABC, abstractmethod


#def generate(tile_data: str,
#             tiling: Tiling,
#             tile_data_coll: TileDataCollection,
#             doc_options: DocumentOptions) -> None:
#
#    svg = create_svg_creator()
#    doc = svg.create_document(tile_data, doc_options)
#    group = svg.create_group()
#    for id, tile in tiling.tiles.items():
#        img_file = tile_data_coll.next(tile.selector)
#        img_data = make_image_data(img_file, tile.width, tile.height)
#        #print(len(img_data))
#        #print(tile.width, tile.height)
#        print(tile)
#        img = svg.create_image(img_data,
#                               tile.width,
#                               tile.height,
#                               tile.ulx,
#                               tile.uly)
#        svg.add_to_group(group, img)
#
#    #print(len(doc.canvas.elements))
#    svg.add_to_image(svg.get_group(group))
#
#    with open(tile_data, "w") as img_file:
#        print(doc, file=img_file)
#

class TilingGenerator(ABC):

    @abstractmethod
    def make_final_tile(self, tile_data: str, width, height, x, y):
        """Adapt image data from file"""

    def generate(self,
                 file_name: str,
                 tiling: Tiling,
                 tile_data_coll: TileDataCollection,
                 doc_options: DocumentOptions) -> None:
        self.svg = create_svg_creator()
        doc = self.svg.create_document(file_name, doc_options)
        group = self.svg.create_group()
        for id, tile in tiling.tiles.items():
            tile_data = tile_data_coll.next(tile.selector)
            final_tile = self.make_final_tile(tile_data, tile.width, tile.height, tile.ulx, tile.uly)
            # print(len(final_tile))
            # print(tile.width, tile.height)
            #print(tile)

            self.svg.add_to_group(group, final_tile)

        # print(len(doc.canvas.elements))
        self.svg.add_to_canvas(self.svg.get_group(group))

        with open(file_name, "w") as tile_data:
            print(doc, file=tile_data)



#class ImageTilingGenerator(TilingGenerator):
#
#    def make_final_tile(self, tile_data: str, width, height, x, y):
#
#        infile = open(tile_data, 'rb')
#        # print (tile_data)
#        with Image(file=infile) as img:
#            i_width = img.width
#            i_height = img.height
#            if width > height:
#                f, r = math.modf(width / height)
#                print('F', f, r)
#                i_width = math.ceil((1.0 + f) * i_width)
#            else:
#                f, r = math.modf(height / width)
#                # i_height *= math.ceil(1.0 + (f))
#                print('F', f, r)
#                i_height = math.ceil((1.0 + f) * i_height)
#            print(r)
#            print('width', i_width, img.width)
#            print('height', i_height, img.height)

#            img.liquid_rescale(i_width, i_height)
#            # img.liquid_rescale(img.width, img.height)
#            base64_data = base64.b64encode(img.make_blob()).decode('ASCII')
#
#        img_data = "data:image/jpg;base64," + base64_data
#        img = self.svg.create_image(img_data,
#                               width,
#                               height,
#                               x,
#                               y)
#        return img
#

class SvgRectTilingGenerator(TilingGenerator):

    def make_final_tile(self, tile_data: str, width, height, x, y):

        try:
            l = tile_data.split(':')
            r_width = int(l[1])
            r_height = int(l[0])
        except:
            print(tile_data)

        w_factor = width // r_width
        h_factor = height // r_height

        print("make final", tile_data, width, height, r_width*w_factor, r_height*h_factor)

        rect = self.svg.create_rectangle(width=r_width*w_factor,
                                         height=r_height*h_factor,
                                         ulx=x, uly=y)

        return rect

