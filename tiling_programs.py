
from tiling_actions import Tiling_Action
from abc import ABC, abstractmethod
from tiling_actions import Position, Placement

class Tiling_Program:

    def __call__(self):
        return self.tiles


class Pine_Heel(Tiling_Program):
    """
        Selectors:
            - 1:1
            - 2:1
            - 1:2
    """
    selectors = ['2:1', '1:2', '1:1']

    def __init__(self):
        self.tiles = [
            Placement(selector='2:1', x=0, y=0),
            Placement(selector='1:1', x=2, y=0),
            Placement(selector='1:2', x=3, y=0),
            Placement(selector='1:1', x=0, y=1),
            Placement(selector='1:1', x=1, y=1),
            Placement(selector='1:1', x=2, y=1),
            Placement(selector='1:2', x=3, y=0),
            Placement(selector='1:1', x=1, y=2),
            Placement(selector='1:1', x=2, y=2),
            Placement(selector='1:1', x=3, y=2),
            Placement(selector='2:1', x=2, y=3),
        ]

