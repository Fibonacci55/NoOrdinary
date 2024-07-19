from tile import Tile
from tile_common import Corner, Positioning
import networkx as nx

class Tiling:

    def __init__(self, tiles: dict[int, Tile]) -> None:
        self.tiles = tiles
        self.graph = nx.DiGraph()
        for tile_id, tile in self.tiles.items():
            #rel_to_tile, corner = (tile.pos.related_tile, tile.pos[1])
            if tile.pos:
                rel_to_tile = tile.pos.related_tile
                print('adding', rel_to_tile, tile_id)
                self.graph.add_edge(rel_to_tile, tile_id)

        self.graph.add_edge(1,2)
        self.edge_list = list(nx.dfs_edges(self.graph, source=1))
        print(self.edge_list)
        for edge in self.edge_list:
            cur_tile = self.tiles[edge[1]]
            rel_tile = self.tiles[edge[0]]
            print('cur_tile.pos', cur_tile.pos)
            if cur_tile.pos.positioned_corner == Corner.UL:
                cur_tile.ulx, cur_tile.uly = rel_tile.corner(cur_tile.pos.related_corner)
            elif cur_tile.pos.positioned_corner == Corner.LL:
                #print('position to', cur_tile.pos.positioned_corner)
                ll_x, ll_y = rel_tile.corner(cur_tile.pos.related_corner)
                cur_tile.ulx = ll_x
                cur_tile.uly = ll_y - cur_tile.height
            elif cur_tile.pos.positioned_corner == Corner.LR:
                #print('position to', cur_tile.pos.positioned_corner)
                ur_x, ur_y = rel_tile.corner(cur_tile.pos.related_corner)
                cur_tile.ulx = ur_x - cur_tile.width
                cur_tile.uly = ur_y - cur_tile.height
            else:
                print('position toi UR', cur_tile.pos.positioned_corner)
                ur_x, ur_y = rel_tile.corner(cur_tile.pos.related_corner)
                cur_tile.ulx = ur_x - cur_tile.width
                cur_tile.uly = ur_y
                print(ur_x, ur_y, cur_tile.ulx, cur_tile.uly)

        print(self.tiles)


    def colorize(self):
        pass



tilings = {
#    'Pine_Heel':
#        Tiling(
#        {
#            1: Tile(selector='2:1', ulx=0, uly=0, width=2, height=1),
#            2: Tile(selector='1:1', pos=(1, Corner.UR), width=1, height=1),
#            3: Tile(selector='1:2', pos=(2, Corner.UR), width=1, height=2),
#            4: Tile(selector='1:1', pos=(1, Corner.LL), width=1, height=1),
#            5: Tile(selector='1:1', pos=(4, Corner.UR), width=1, height=1),
#            6: Tile(selector='1:1', pos=(5, Corner.UR), width=1, height=1),
#            7: Tile(selector='1:2', pos=(4, Corner.LL), width=1, height=2),
#            8: Tile(selector='1:1', pos=(7, Corner.UR), width=1, height=1),
#            9: Tile(selector='1:1', pos=(8, Corner.UR), width=1, height=1),
#            10: Tile(selector='1:1', pos=(9, Corner.UR), width=1, height=1),
#            11: Tile(selector='1:1', pos=(8, Corner.LL), width=1, height=1),
#            12: Tile(selector='2:1', pos=(11, Corner.UR), width=2, height=1),
#        }),
#    'Pine_Heel_1':
#        Tiling(
#            {
#                1: Tile(selector='2:1', ulx=0, uly=0, width=2, height=1),
#                2: Tile(selector='1:1', pos=(1, Corner.UR), width=1, height=1),
#                3: Tile(selector='1:2', pos=(2, Corner.UR), width=1, height=2),
#                4: Tile(selector='1:1', pos=(1, Corner.LL), width=1, height=1),
#                5: Tile(selector='1:1', pos=(4, Corner.UR), width=2, height=2),
#                6: Tile(selector='1:1', pos=(3, Corner.LL), width=1, height=1),
#                7: Tile(selector='1:2', pos=(4, Corner.LL), width=1, height=2),
#                8: Tile(selector='1:1', pos=(5, Corner.LL), width=1, height=1),
#                9: Tile(selector='2:1', pos=(8, Corner.UR), width=2, height=1),
#            }),
#
#    'Windmill':
#        Tiling (
#            {
#            1: Tile(selector='1:2', ulx=0, uly=0, width=1, height=2),
#            2: Tile(selector='2:1', pos=(1, Corner.UR), width=2, height=1),
#            3: Tile(selector='2:1', pos=(1, Corner.LL), width=2, height=1),
#            4: Tile(selector='1:1', pos=(2, Corner.LL), width=1, height=1),
#            5: Tile(selector='1:2', pos=(4, Corner.UR), width=1, height=2),
#            }),
#    'Basketweave':
#        Tiling (
#            {
#            1: Tile(selector='1:2', ulx=0, uly=0, width=1, height=2),
#            2: Tile(selector='1:2', pos=(1, Corner.UR), width=1, height=2),
#            3: Tile(selector='2:1', pos=(2, Corner.UR), width=2, height=1),
#            4: Tile(selector='2:1', pos=(3, Corner.LL), width=2, height=1),
#
#            5: Tile(selector='2:1', pos=(1, Corner.LL), width=2, height=1),
#            6: Tile(selector='2:1', pos=(5, Corner.LL), width=2, height=1),
#            7: Tile(selector='1:2', pos=(4, Corner.LL), width=1, height=2),
#            8: Tile(selector='1:2', pos=(7, Corner.UR), width=1, height=2),
#            }),
#
#    'Roman_5':
#        Tiling(
#        {
#            1: Tile(selector='2:2', ulx=0, uly=0, width=2, height=2),
#            2: Tile(selector='2:1', pos=Positioning(1, Corner.LR, positioned_corner=Corner.LL), width=2, height=1),
#            3: Tile(selector='1:2', pos=Positioning(1, Corner.LL), width=1, height=2),
#            4: Tile(selector='3:3', pos=Positioning(3, Corner.UR), width=3, height=3),
#            5: Tile(selector='2:3', pos=Positioning(2, Corner.UR), width=2, height=3),
#            6: Tile(selector='1:1', pos=Positioning(5, Corner.LL), width=1, height=1),
#            7: Tile(selector='1:1', pos=Positioning(4, Corner.LL), width=1, height=1),
#            8: Tile(selector='3:2', pos=Positioning(7, Corner.UR), width=3, height=2),
#            9: Tile(selector='2:2', pos=Positioning(6, Corner.UR), width=2, height=2),
#            10: Tile(selector='1:1', pos=Positioning(5, Corner.UR, positioned_corner=Corner.LR), width=1, height=1),
#        }),

    'Roman_50':
        Tiling(
            {
                1: Tile(id=1, selector='2:2', ulx=0, uly=0, width=2, height=2),
                2: Tile(id=2, selector='2:1', pos=Positioning(1, Corner.LR, positioned_corner=Corner.LL), width=2, height=1),
                3: Tile(id=3, selector='1:2', pos=Positioning(1, Corner.LL), width=1, height=2),
                4: Tile(id=4, selector='3:3', pos=Positioning(3, Corner.UR), width=3, height=3),
                5: Tile(id=5, selector='2:3', pos=Positioning(2, Corner.UR), width=2, height=3),
                6: Tile(id=6, selector='1:1', pos=Positioning(5, Corner.LL), width=1, height=1),
                7: Tile(id=7, selector='1:1', pos=Positioning(4, Corner.LL), width=1, height=1),
                8: Tile(id=8, selector='3:2', pos=Positioning(7, Corner.UR), width=3, height=2),
                9: Tile(id=9, selector='2:2', pos=Positioning(6, Corner.UR), width=2, height=2),
                10: Tile(id=10, selector='1:1', pos=Positioning(5, Corner.UR, positioned_corner=Corner.LR), width=1, height=1),

                11: Tile(id=11, selector='2:2', pos=Positioning(10, Corner.UR), width=2, height=2),
                12: Tile(id=12, selector='2:1', pos=Positioning(11, Corner.LR, positioned_corner=Corner.LL), width=2, height=1),
                13: Tile(id=13, selector='1:2', pos=Positioning(11, Corner.LL), width=1, height=2),
                14: Tile(id=14, selector='3:3', pos=Positioning(13, Corner.UR), width=3, height=3),
                15: Tile(id=15, selector='2:3', pos=Positioning(12, Corner.UR), width=2, height=3),
                16: Tile(id=16, selector='1:1', pos=Positioning(15, Corner.LL), width=1, height=1),
                17: Tile(id=17, selector='1:1', pos=Positioning(14, Corner.LL), width=1, height=1),
                18: Tile(id=18, selector='3:2', pos=Positioning(17, Corner.UR), width=3, height=2),
                19: Tile(id=19, selector='2:2', pos=Positioning(16, Corner.UR), width=2, height=2),
                20: Tile(id=20, selector='1:1', pos=Positioning(15, Corner.UR, positioned_corner=Corner.LR), width=1, height=1),

                21: Tile(id=21, selector='2:2', pos=Positioning(7,  Corner.LR, positioned_corner=Corner.UR), width=2, height=2),
                22: Tile(id=22, selector='2:1', pos=Positioning(21, Corner.LR, positioned_corner=Corner.LL), width=2, height=1),
                23: Tile(id=23, selector='1:2', pos=Positioning(21, Corner.LL), width=1, height=2),
                24: Tile(id=24, selector='3:3', pos=Positioning(23, Corner.UR), width=3, height=3),
                25: Tile(id=25, selector='2:3', pos=Positioning(22, Corner.UR), width=2, height=3),
                26: Tile(id=26, selector='1:1', pos=Positioning(25, Corner.LL), width=1, height=1),
                27: Tile(id=27, selector='1:1', pos=Positioning(24, Corner.LL), width=1, height=1),
                28: Tile(id=28, selector='3:2', pos=Positioning(27, Corner.UR), width=3, height=2),
                29: Tile(id=29, selector='2:2', pos=Positioning(26, Corner.UR), width=2, height=2),
                30: Tile(id=30, selector='1:1', pos=Positioning(25, Corner.UR, positioned_corner=Corner.LR), width=1, height=1),

                31: Tile(id=31, selector='2:2', pos=Positioning(30, Corner.UR), width=2, height=2),
                32: Tile(id=32, selector='2:1', pos=Positioning(31, Corner.LR, positioned_corner=Corner.LL), width=2, height=1),
                33: Tile(id=33, selector='1:2', pos=Positioning(31, Corner.LL), width=1, height=2),
                34: Tile(id=34, selector='3:3', pos=Positioning(33, Corner.UR), width=3, height=3),
                35: Tile(id=35, selector='2:3', pos=Positioning(32, Corner.UR), width=2, height=3),
                36: Tile(id=36, selector='1:1', pos=Positioning(35, Corner.LL), width=1, height=1),
                37: Tile(id=37, selector='1:1', pos=Positioning(34, Corner.LL), width=1, height=1),
                38: Tile(id=38, selector='3:2', pos=Positioning(37, Corner.UR), width=3, height=2),
                39: Tile(id=39, selector='2:2', pos=Positioning(36, Corner.UR), width=2, height=2),
                40: Tile(id=40, selector='1:1', pos=Positioning(35, Corner.UR, positioned_corner=Corner.LR), width=1, height=1),

                41: Tile(id=21, selector='2:2', pos=Positioning(27, Corner.LR, positioned_corner=Corner.UR), width=2,
                         height=2),
                42: Tile(id=22, selector='2:1', pos=Positioning(41, Corner.LR, positioned_corner=Corner.LL), width=2,
                         height=1),
                44: Tile(id=24, selector='3:3', pos=Positioning(42, Corner.LR, positioned_corner=Corner.UR), width=3, height=3),
                45: Tile(id=25, selector='2:3', pos=Positioning(42, Corner.UR), width=2, height=3),
                50: Tile(id=30, selector='1:1', pos=Positioning(45, Corner.UR, positioned_corner=Corner.LR), width=1, height=1),

                51: Tile(id=51, selector='2:2', pos=Positioning(50, Corner.UR), width=2, height=2),
                52: Tile(id=52, selector='2:1', pos=Positioning(51, Corner.LR, positioned_corner=Corner.LL), width=2, height=1),
                53: Tile(id=53, selector='1:2', pos=Positioning(51, Corner.LL), width=1, height=2),
                54: Tile(id=54, selector='3:3', pos=Positioning(53, Corner.UR), width=3, height=3),
                55: Tile(id=55, selector='2:3', pos=Positioning(52, Corner.UR), width=2, height=3),

            }),

    #    'Cobbiesstone_90' :
#        Tiling (
#{
#            1: Tile(selector='1:2', ulx=0, uly=0, width=1, height=2),
#            2: Tile(selector='1:1', pos=(1, Corner.UR), width=1, height=1),
#            3: Tile(selector='2:1', pos=(2, Corner.UR), width=2, height=1),
#            4: Tile(selector='2:1', pos=(2, Corner.LL), width=2, height=1),
#            5: Tile(selector='1:2', pos=(4, Corner.UR), width=1, height=2),
#            6: Tile(selector='2:1', pos=(1, Corner.LL), width=2, height=1),
#            7: Tile(selector='1:2', pos=(6, Corner.UR), width=1, height=2),
#            8: Tile(selector='1:1', pos=(6, Corner.LL), width=1, height=1),
#            9: Tile(selector='1:1', pos=(8, Corner.UR), width=1, height=1),
#            10: Tile(selector='1:1', pos=(5, Corner.LL), width=1, height=1),
#
#        }
#        )

}
