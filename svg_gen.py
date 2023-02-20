from abc import ABC, abstractmethod
from dataclasses import dataclass



@dataclass
class DocumentOptions:

    width: int
    height: int
    unit: str



class SvgLib(ABC):

    @abstractmethod
    def create_document(self, name: str, options: DocumentOptions) -> None:
        """ Creates a SVG document """

    @abstractmethod
    def create_group(self) -> int:
        """ Creates a new group of the document, returns the id of the group"""


