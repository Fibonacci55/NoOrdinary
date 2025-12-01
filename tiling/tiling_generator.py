# tiling_generator.py
from wand.image import Image
import base64
from tile import Tile
from svg_gen import create_svg_creator, DocumentOptions
from tiling.imagecollection import ImageCollection


def make_image_data(file_name: str):
    """
    Reads an image file, resizes it using liquid rescaling, and converts it to a base64 string.

    :param file_name: Path to the image file.
    :return: Base64 encoded string formatted for SVG embedding (data:image/jpg;base64,...).
    """
    infile = open(file_name, 'rb')
    # print (file_name)
    with Image(file=infile) as img:
        width = img.width
        height = img.height
        # Liquid rescale preserves features while resizing
        img.liquid_rescale(width, height)
        base64_data = base64.b64encode(img.make_blob()).decode('ASCII')

    img_data = "data:image/jpg;base64," + base64_data
    return img_data


def generate(file_name: str,
             tiling_program: list[Tile],
             img_coll: ImageCollection):
    """
    Generates an SVG file representing the tiling.

    :param file_name: Output filename for the SVG.
    :param tiling_program: List of Tile objects defining the layout.
    :param img_coll: ImageCollection to source images from.
    """

    svg = create_svg_creator()
    # Create document with standard dimensions
    doc = svg.create_document(file_name, DocumentOptions(width=200, height=200, unit="mm"))
    group = svg.create_group()

    for tile in tiling_program:
        # Get next image based on tile selector
        img_file = img_coll.next(tile.selector)
        img_data = make_image_data(img_file)

        print(tile)  # Debug output

        # Create SVG image element
        img = svg.create_image(img_data,
                               tile.width,
                               tile.height,
                               tile.ulx,
                               tile.uly)
        svg.add_to_group(group, img)

    # Add the group to the main image canvas
    svg.add_to_image(svg.get_group(group))

    # Write to file
    with open(file_name, "w") as img_file:
        print(doc, file=img_file)
