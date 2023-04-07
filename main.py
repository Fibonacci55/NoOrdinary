# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import argparse

def create_arg_parser():
    parser = argparse.ArgumentParser(
                    prog = 'Maze',
                    description = 'Creates mazes',
                    epilog = ' ')

    parser.add_argument('-n', '--new', action="store_true", help='Create a new maze')
    parser.add_argument('-d', '--dimension', type=str,
                        dest="dimension", default='',
                        help='Dimension of the new mask' )

    parser.add_argument('-m', '--apply_mask', type=str,
                        dest="mask", default='',
                        help='Apply the mask on the maze' )
    parser.add_argument('-s', '--save_to', type=str,
                        dest="to_file", default='',
                        help='Save a newly created maze to file')
    parser.add_argument('-r', '--reload_from', type=str,
                        dest="from_file", default='',
                        help='Reload a created maze from file')
    parser.add_argument('-p', '--print_to', type=str,
                        dest="svg_file", default='',
                        help='Create a SVG file')

    parser.add_argument('-i', '--info', action="store_true", help='Info on a maze')

    parser.add_argument('-a', '--add', type=str,
                        dest="path", default='',
                        help='Add a path from two points to a maze. Given by "n,n n,n"')
    return parser


import tiling_factory as tf
from tiling_generator import generate
from imagecollection import PictureImageCollection

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    scale = tf.ScalingTransform(factor=70)
    d = tf.AddDistanceTransform(distance=2)
    tiles = tf.make_single_tiling('Pine_Heel', transformations=[scale, d])
    #tiles = tf.make_single_tiling('Pine_Heel_1', transformations=[scale, d])
    #tiles = tf.make_single_tiling('Windmill', transformations=[scale, d])
    #tiles = tf.make_single_tiling('Basketweave', transformations=[scale, d])
    coll = PictureImageCollection()
    #coll.add_directory(path="D:\\Projects\\NoOrdinaryEyes\\1_1", selector="1:1")
    #coll.add_directory(path="D:\\Projects\\NoOrdinaryEyes\\2_1", selector="2:1")
    #coll.add_directory(path="D:\\Projects\\NoOrdinaryEyes\\1_2", selector="1:2")
    #
    coll.add_directory(path="D:\\Projects\\Baragan\\Edited\\1_1", selector="1:1")
    coll.add_directory(path="D:\\Projects\\Baragan\\Edited\\2_1", selector="2:1")
    coll.add_directory(path="D:\\Projects\\Baragan\\Edited\\1_2", selector="1:2")

    #print(coll.image_collection['1:1'])
    generate("D:\\Temp\\Test.svg", tiles, coll)
