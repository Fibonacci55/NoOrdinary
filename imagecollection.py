from abc import ABC, abstractmethod
import random as ra
import glob


class SelectorExhausted(Exception):
    def __init__(self, selector):
        super().__init__("Selector %s exhausted" % selector)


class InvalidSelector(Exception):
    def __init__(self, selector):
        super().__init__("Invalid Selector %s" % selector)


class ImageSelector(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def __call__(self, from_list: list[str]) -> str:
        """ returns an image """


class RandomSelector(ImageSelector):

    def __call__(self, from_list: list[str]) -> str:
        v = ra.choice(from_list)
        from_list.remove(v)
        return v


class OrderedSelector(ImageSelector):

    def __call__(self, from_list: list[str]) -> str:
        v = from_list.pop(0)
        return v


class ImageCollection:

    def __init__(self, selection_method: ImageSelector):
        self.selection_method = selection_method
        self.image_collection = {}

    def next(self, selector: str) -> str:
        tile_list = self.image_collection[selector]
        try:
            next_image = self.selection_method(tile_list)
            return next_image

        except IndexError:
            raise SelectorExhausted(selector)


class PictureImageCollection(ImageCollection):

    def __init__(self, selection_method=OrderedSelector()):
        super(PictureImageCollection).__init__(selection_method)

    def add_directory(self, path: str, selector: str) -> None:
        self.image_collection[selector] = glob.glob(path)
