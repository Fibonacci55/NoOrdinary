from tile import Tile
from tile_common import Corner
import networkx as nx

class Tiling:

    def __init__(self, tiles: dict[Tile]) -> None:
        self.tiles = tiles
        self.graph = nx.DiGraph()
        for tile_id, tile in self.tiles.items():
            rel_to_tile, corner = tile.pos
            if rel_to_tile:
                print ('adding', rel_to_tile, tile_id)
                self.graph.add_edge(rel_to_tile, tile_id)

        self.graph.add_edge(1,2)
        self.edge_list = list(nx.dfs_edges(self.graph, source=1))
        print(self.edge_list)
        for edge in self.edge_list:
            cur_tile = self.tiles[edge[1]]
            rel_tile = self.tiles[edge[0]]
            cur_tile.ulx, cur_tile.uly = rel_tile.corner(cur_tile.pos[1])
            #x, y = rel_tile.corner(cur_tile.pos[1])
            #cur_tile.ul_x = x
            #cur_tile.ul_y = y
        print(self.tiles)

tilings = {
    'Pine_Heel':
        Tiling(
        {
            1: Tile(selector='2:1', ulx=0, uly=0, width=2, height=1),
            2: Tile(selector='1:1', pos=(1, Corner.UR), width=1, height=1),
            3: Tile(selector='1:2', pos=(2, Corner.UR), width=1, height=2),
            4: Tile(selector='1:1', pos=(1, Corner.LL), width=1, height=1),
            5: Tile(selector='1:1', pos=(4, Corner.UR), width=1, height=1),
            6: Tile(selector='1:1', pos=(5, Corner.UR), width=1, height=1),
            7: Tile(selector='1:2', pos=(4, Corner.LL), width=1, height=2),
            8: Tile(selector='1:1', pos=(7, Corner.UR), width=1, height=1),
            9: Tile(selector='1:1', pos=(8, Corner.UR), width=1, height=1),
            10: Tile(selector='1:1', pos=(9, Corner.UR), width=1, height=1),
            11: Tile(selector='1:1', pos=(8, Corner.LL), width=1, height=1),
            12: Tile(selector='2:1', pos=(11, Corner.UR), width=2, height=1),
        }),
    'Pine_Heel_1':
        Tiling(
            {
                1: Tile(selector='2:1', ulx=0, uly=0, width=2, height=1),
                2: Tile(selector='1:1', pos=(1, Corner.UR), width=1, height=1),
                3: Tile(selector='1:2', pos=(2, Corner.UR), width=1, height=2),
                4: Tile(selector='1:1', pos=(1, Corner.LL), width=1, height=1),
                5: Tile(selector='1:1', pos=(4, Corner.UR), width=2, height=2),
                6: Tile(selector='1:1', pos=(3, Corner.LL), width=1, height=1),
                7: Tile(selector='1:2', pos=(4, Corner.LL), width=1, height=2),
                8: Tile(selector='1:1', pos=(5, Corner.LL), width=1, height=1),
                9: Tile(selector='2:1', pos=(8, Corner.UR), width=2, height=1),
            }),

    'Windmill':
        Tiling (
            {
            1: Tile(selector='1:2', ulx=0, uly=0, width=1, height=2),
            2: Tile(selector='2:1', pos=(1, Corner.UR), width=2, height=1),
            3: Tile(selector='2:1', pos=(1, Corner.LL), width=2, height=1),
            4: Tile(selector='1:1', pos=(2, Corner.LL), width=1, height=1),
            5: Tile(selector='1:2', pos=(4, Corner.UR), width=1, height=2),
            }),
    'Basketweave':
        Tiling (
            {
            1: Tile(selector='1:2', ulx=0, uly=0, width=1, height=2),
            2: Tile(selector='1:2', pos=(1, Corner.UR), width=1, height=2),
            3: Tile(selector='2:1', pos=(2, Corner.UR), width=2, height=1),
            4: Tile(selector='2:1', pos=(3, Corner.LL), width=2, height=1),

            5: Tile(selector='2:1', pos=(1, Corner.LL), width=2, height=1),
            6: Tile(selector='2:1', pos=(5, Corner.LL), width=2, height=1),
            7: Tile(selector='1:2', pos=(4, Corner.LL), width=1, height=2),
            8: Tile(selector='1:2', pos=(7, Corner.UR), width=1, height=2),
            }),

    'Roman_5' :
        Tiling (
        {
            1: Tile(selector='2:2', ulx=0, uly=0, width=2, height=2),
            2: Tile(selector='2:1', pos=(1, Corner.LR), width=2, height=1),
            3: Tile(selector='2:3', pos=(2, Corner.UR), width=2, height=3),
            4: Tile(selector='1:2', pos=(1, Corner.LL), width=1, height=2),
            5: Tile(selector='3:3', pos=(4, Corner.UR), width=3, height=3),
            6: Tile(selector='2:1', pos=(1, Corner.LL), width=2, height=1),
            7: Tile(selector='1:1', pos=(5, Corner.LL), width=1, height=1),
            8: Tile(selector='3:2', pos=(7, Corner.UR), width=3, height=2),
        }),
    'Cobbiesstone_90' :
        Tiling (
{
            1: Tile(selector='1:2', ulx=0, uly=0, width=1, height=2),
            2: Tile(selector='1:1', pos=(1, Corner.UR), width=1, height=1),
            3: Tile(selector='2:1', pos=(2, Corner.UR), width=2, height=1),
            4: Tile(selector='2:1', pos=(2, Corner.LL), width=2, height=1),
            5: Tile(selector='1:2', pos=(4, Corner.UR), width=1, height=2),
            6: Tile(selector='2:1', pos=(1, Corner.LL), width=2, height=1),
            7: Tile(selector='1:2', pos=(6, Corner.UR), width=1, height=2),
            8: Tile(selector='1:1', pos=(6, Corner.LL), width=1, height=1),
            9: Tile(selector='1:1', pos=(8, Corner.UR), width=1, height=1),
            10: Tile(selector='1:1', pos=(5, Corner.LL), width=1, height=1),

        }
        )

}
