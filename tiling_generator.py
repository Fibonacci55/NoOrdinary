
import svgwrite
from math import floor
from wand.image import Image
import base64
from abc import ABC, abstractmethod
import svg_gen as svg
from tile import Tile
from svg_gen import create_svg_creator, DocumentOptions
from imagecollection import ImageCollection
from tilings import Tiling

def make_image_data(file_name: str):

    infile = open(file_name, 'rb')
    #print (file_name)
    with Image(file=infile) as img:
        width = img.width
        height = img.height
        img.liquid_rescale(width, height)
        base64_data = base64.b64encode(img.make_blob()).decode('ASCII')

    img_data = "data:image/jpg;base64," + base64_data
    return img_data

def generate(file_name: str,
             tiling: Tiling,
             img_coll: ImageCollection):

    svg = create_svg_creator()
    doc = svg.create_document(file_name, DocumentOptions(width=300, height=300, unit="mm"))
    group = svg.create_group()
    for id, tile in tiling.tiles.items():
        img_file = img_coll.next(tile.selector)
        img_data = make_image_data(img_file)
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


