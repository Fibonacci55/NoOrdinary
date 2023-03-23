from tile import Tile

class Tiling:

    def __init__(self, tiles: dict[Tile], positions) -> None:
        pass


tilings = {
    'Pine_Heel':
        {
            1: Tile(selector='2:1', ulx=0, uly=0, width=2, height=1),
            2: Tile(selector='1:1', ulx=2, uly=0, width=1, height=1),
            3: Tile(selector='1:2', ulx=3, uly=0, width=1, height=2),
            4: Tile(selector='1:1', ulx=0, uly=1, width=1, height=1),
            5: Tile(selector='1:1', ulx=1, uly=1, width=1, height=1),
            6: Tile(selector='1:1', ulx=2, uly=1, width=1, height=1),
            7: Tile(selector='1:2', ulx=0, uly=2, width=1, height=2),
            8: Tile(selector='1:1', ulx=1, uly=2, width=1, height=1),
            9: Tile(selector='1:1', ulx=2, uly=2, width=1, height=1),
            10: Tile(selector='1:1', ulx=3, uly=2, width=1, height=1),
            11: Tile(selector='2:1', ulx=2, uly=3, width=2, height=1),
            12: Tile(selector='1:1', ulx=1, uly=3, width=1, height=1),
        },
    'Windmill':
        [
            Tile(selector='2:1', ulx=0, uly=0, width=2, height=1, neighbours='RB'),
            Tile(selector='1:2', ulx=2, uly=0, width=1, height=2, neighbours='LB'),
            Tile(selector='1:2', ulx=0, uly=1, width=1, height=2, neighbours='RT'),
            Tile(selector='1:1', ulx=1, uly=1, width=1, height=1, neighbours='LTRB'),
            Tile(selector='2:1', ulx=1, uly=2, width=2, height=1, neighbours='LT'),

        ],
    'Basketweave':
        [
            Tile(selector='1:2', ulx=0, uly=0, width=1, height=2, neighbours='R'),
            Tile(selector='1:2', ulx=1, uly=0, width=1, height=2, neighbours='L'),
            Tile(selector='2:1', ulx=0, uly=2, width=2, height=1, neighbours='TB'),
            Tile(selector='2:1', ulx=0, uly=3, width=2, height=1, neighbours='2T'),

            Tile(selector='2:1', ulx=2, uly=0, width=2, height=1, neighbours='L'),
            Tile(selector='2:1', ulx=2, uly=1, width=2, height=1, neighbours='TBL'),
            Tile(selector='1:2', ulx=2, uly=2, width=1, height=2, neighbours='RLT'),
            Tile(selector='1:2', ulx=3, uly=2, width=1, height=2, neighbours='LT'),

        ]
}
