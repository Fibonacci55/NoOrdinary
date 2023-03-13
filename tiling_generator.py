
import svgwrite
from math import floor
from wand.image import Image
import base64
from abc import ABC, abstractmethod
import svg_gen as svg
from tile import Tile
from svg_gen import create_svg_creator, DocumentOptions
from imagecollection import ImageCollection

def make_image_data(file_name: str, corr_fac: float):

    infile = open(file_name, 'rb')
    #print (file_name)
    with Image(file=infile) as img:
        width = img.width
        height = img.height
        if width > height:
            img.liquid_rescale(width, floor(height * corr_fac))
        elif width < height:
            img.liquid_rescale(floor(width * corr_fac), height)
        base64_data = base64.b64encode(img.make_blob()).decode('ASCII')

    img_data = "data:image/jpg;base64," + base64_data
    return img_data

def generate(file_name: str,
             tiling_program: list[Tile],
             img_coll: ImageCollection,
             corr_factor: float):

    svg = create_svg_creator()
    doc = svg.create_document(file_name, DocumentOptions(width=200, height=200, unit="mm"))
    group = svg.create_group()
    for tile in tiling_program:
        img_file = img_coll.next(tile.selector)
        img_data = make_image_data(img_file, corr_factor)
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


