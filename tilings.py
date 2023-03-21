from tile import Tile

tilings = {
    'Pine_Heel':
        [
            Tile(selector='2:1', ulx=0, uly=0, width=2, height=1, neighbours='RB'),
            Tile(selector='1:1', ulx=2, uly=0, width=1, height=1, neighbours='LRB'),
            Tile(selector='1:2', ulx=3, uly=0, width=1, height=2, neighbours='LB'),
            Tile(selector='1:1', ulx=0, uly=1, width=1, height=1, neighbours='TRB'),
            Tile(selector='1:1', ulx=1, uly=1, width=1, height=1, neighbours='LTRB'),
            Tile(selector='1:1', ulx=2, uly=1, width=1, height=1, neighbours='LTRB'),
            Tile(selector='1:2', ulx=0, uly=2, width=1, height=2, neighbours='TR'),
            Tile(selector='1:1', ulx=1, uly=2, width=1, height=1, neighbours='LTRB'),
            Tile(selector='1:1', ulx=2, uly=2, width=1, height=1, neighbours='LTRB'),
            Tile(selector='1:1', ulx=3, uly=2, width=1, height=1, neighbours='LTB'),
            Tile(selector='2:1', ulx=2, uly=3, width=2, height=1, neighbours='LTR'),
            Tile(selector='1:1', ulx=1, uly=3, width=1, height=1, neighbours='LT'),
        ],
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
