# imagecollection.py
from abc import ABC, abstractmethod
import random as ra
import glob


class SelectorExhausted(Exception):
    """Raised when a selector cannot provide any more unique items."""

    def __init__(self, selector):
        super().__init__("Selector %s exhausted" % selector)


class InvalidSelector(Exception):
    """Raised when a requested selector key does not exist."""

    def __init__(self, selector):
        super().__init__("Invalid Selector %s" % selector)


class ImageSelector(ABC):
    """Abstract base class for image selection strategies."""

    def __init__(self):
        pass

    @abstractmethod
    def __call__(self, from_list: list[str]) -> str:
        """
        Selects and returns an image path from the list.

        :param from_list: List of available image paths.
        :return: Selected image path.
        """


class RandomSelector(ImageSelector):
    """Selects an image randomly and removes it from the list to avoid repetition."""

    def __call__(self, from_list: list[str]) -> str:
        v = ra.choice(from_list)
        from_list.remove(v)
        return v


class OrderedSelector(ImageSelector):
    """Selects the first image in the list and removes it (FIFO)."""

    def __call__(self, from_list: list[str]) -> str:
        v = from_list.pop(0)
        return v


class ImageCollection:
    """
    Manages collections of images categorized by selectors (keys).
    Uses a selection strategy to retrieve images.
    """

    def __init__(self, selection_method: ImageSelector):
        """
        :param selection_method: Strategy for picking images (e.g., Random, Ordered).
        """
        self.selection_method = selection_method
        self.image_collection = {}

    def next(self, selector: str) -> str:
        """
        Retrieves the next image for the given selector category.

        :param selector: Key identifying the image group.
        :return: Path to the image.
        :raises SelectorExhausted: If no images remain in the list.
        """
        tile_list = self.image_collection[selector]
        try:
            next_image = self.selection_method(tile_list)
            return next_image

        except IndexError:
            raise SelectorExhausted(selector)


class PictureImageCollection(ImageCollection):
    """
    Specialized ImageCollection that populates itself from file directories.
    """

    def __init__(self, selection_method=OrderedSelector(), img_ext='.jpg'):
        super().__init__(selection_method)
        self.img_ext = img_ext

    def add_directory(self, path: str, selector: str) -> None:
        """
        Adds all images with the specific extension from a directory to a selector group.

        :param path: Directory path.
        :param selector: Key to associate these images with.
        """
        # print(path)
        self.image_collection[selector] = glob.glob(path + '\*' + self.img_ext)
