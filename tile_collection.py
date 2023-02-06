
from abc import ABC, abstractmethod
import random as ra
import glob


class SelectorExhausted(Exception):
    def __init__(self, selector):
        super().__init__("Selector %s exhausted" % selector)

class InvalidSelector(Exception):
    def __init__(self, selector):
        super().__init__("Invalid Selector %s" % selector)

class Tile_Selector(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def __call__(self, from_list):
        pass

class Random_Selector(Tile_Selector):

    def __call__(self, from_list):
        v = ra.choice (from_list)
        from_list.remove (v)
        return v

class Ordered_Selector(Tile_Selector):

    def __call__(self, from_list):
        v = from_list.pop(0)


class Tile_Collection:

    def __init__(self, selection_method):
        super().__init__()
        self.selection_method = selection_method
        self.tile_collection = {}

    def next(self, selector):
        tile_list = self.tile_collection[selector]
        try:
            next_tile = self.selection_method(tile_list)
        except IndexError:
            raise SelectorExhausted(selector)


class Picture_Tiles(Tile_Collection):

    def __init__(self, selection_method=Ordered_Selector()):
        super(Picture_Tiles).__init__()

    def add_directory(self, path, selector):
        self.tile_collection[selector] = glob.glob(path)
