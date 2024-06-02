from abc import ABC, abstractmethod
import random as ra
import glob
from typing import Callable
import os


class SelectorExhausted(Exception):
    def __init__(self, selector):
        super().__init__("Selector %s exhausted" % selector)


class InvalidSelector(Exception):
    def __init__(self, selector):
        super().__init__("Invalid Selector %s" % selector)


class ImageSelector(ABC):

    def __init__(self, from_list=[]):
        self.from_list = from_list
        pass

    @abstractmethod
    def __call__(self) -> str:
        """ returns an image """


class RandomSelector(ImageSelector):

    def __call__(self) -> str:
        v = ra.choice(self.from_list)
        self.from_list.remove(v)
        return v


class OrderedSelector(ImageSelector):

    def __call__(self) -> str:
        v = self.from_list.pop(0)
        return v
class ConstantSelector(ImageSelector):

    def __call__(self) -> str:
        return self.from_list[0]

ord_sel_factory = lambda l: OrderedSelector(from_list=l)
rnd_sel_factory = lambda l: RandomSelector(from_list=l)
const_sel_factory = lambda l: ConstantSelector(from_list=l)


class TileDataCollection(ABC):

    def __init__(self):
        #self.selection_method = sel_mthd_factory()
        self.image_collection = {}

    @abstractmethod
    def add_selector(self, selector: str, sel_mthd_factory: Callable) -> None:
        """Add a selector to the collection"""

    def next(self, selector: str) -> str:

        try:
            tile_selector = self.image_collection[selector]
            next_image = tile_selector()
            return next_image

        except KeyError:
            raise InvalidSelector(selector)

        except IndexError:
            raise SelectorExhausted(selector)


class ImageTileDataCollection(TileDataCollection):

    def __init__(self, base_path='', img_ext='.jpg'):
        super().__init__()
        self.img_ext = img_ext
        self.base_path = base_path

    def add_selector(self, selector: str, sel_mthd_factory: Callable) -> None:
        sel = selector.replace(':', '_')
        path = os.path.join(self.base_path, sel)
        self.image_collection[selector] = sel_mthd_factory(glob.glob(path + '\*' + self.img_ext ))


class SvgFrameCollection(TileDataCollection):

    def __init__(self):
        super().__init__()

    def add_selector(self, selector: str, sel_mthd_factory: Callable) -> None:
        self.image_collection[selector] = sel_mthd_factory([selector])

if __name__ == '__main__':
    f = ord_sel_factory([1, 2, 3])
    print(f())