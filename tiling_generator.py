import math

import svgwrite
from wand.image import Image
import base64
from math import ceil, modf
from tile import Tile
from svg_gen import create_svg_creator, DocumentOptions
from imagecollection import ImageCollection
from tilings import Tiling

def make_image_data(file_name: str, width, height):

    infile = open(file_name, 'rb')
    #print (file_name)
    with Image(file=infile) as img:
        i_width = img.width
        i_height = img.height
        if width > height:
            f,r = math.modf(width / height)
            print('F', f, r)
            i_width = math.ceil((1.0 + f) * i_width)
        else:
            f,r = math.modf(height / width)
            #i_height *= math.ceil(1.0 + (f))
            print('F', f, r)
            i_height = math.ceil((1.0 + f) * i_height)
        print (r)
        print('width', i_width, img.width)
        print('height', i_height, img.height)

        img.liquid_rescale(i_width, i_height)
        #img.liquid_rescale(img.width, img.height)
        base64_data = base64.b64encode(img.make_blob()).decode('ASCII')

    img_data = "data:image/jpg;base64," + base64_data
    return img_data

def generate(file_name: str,
             tiling: Tiling,
             img_coll: ImageCollection,
             doc_options: DocumentOptions) -> None:

    svg = create_svg_creator()
    doc = svg.create_document(file_name, doc_options)
    group = svg.create_group()
    for id, tile in tiling.tiles.items():
        img_file = img_coll.next(tile.selector)
        img_data = make_image_data(img_file, tile.width, tile.height)
        #print(len(img_data))
        #print(tile.width, tile.height)
        print(tile)
        img = svg.create_image(img_data,
                               tile.width,
                               tile.height,
                               tile.ulx,
                               tile.uly)
        svg.add_to_group(group, img)

    #print(len(doc.canvas.elements))
    svg.add_to_image(svg.get_group(group))

    with open(file_name, "w") as img_file:
        print(doc, file=img_file)


