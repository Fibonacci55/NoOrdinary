import networkx as nx
import json
from tile import Tile


c_map = {
    0: '#AC2727',
    1: '#243A73',
    2: '#ACAB27',
    3: '#1F932D'
}


def between(interval: tuple, p: int) -> bool:
    lower = interval[0]
    upper = interval[1]
    return lower <= p <= upper


def is_cover(i_one: tuple, i_two: tuple) -> bool:
    return between(i_one, i_two[0]) or between(i_one, i_two[1])


def left_neighbour(x: Tile, y: Tile) -> bool:
    """y is a left neighbour of x"""
    if x.lr[0] == y.ll[0]:
        return is_cover((x.ur[1], x.lr[1]), (y.ul[1], y.ll[1]))
    else:
        return False


def right_neighbour (x: Tile, y: Tile) -> bool:
    """y is a right neighbour of x"""
    return left_neighbour(y, x)


def upper_neighbour(x: Tile, y: Tile) -> bool:
    """y is a upper neighbour of x"""
    if x.ul[1] == y.ll[1]:
        return is_cover((x.ll[0], x.lr[0]), (y.ul[0], y.ur[0]))
    else:
        return False

def lower_neighbour(x: Tile, y: Tile) -> bool:
    return upper_neighbour(y, x)
#    if x.ll[1] == y.ul[1]:
#        return is_cover((x.ll[0], x.lr[1]), (y.ul[0], y.ur[0]))
#    else:
#        return False


def adjacent(x: Tile, y: Tile) -> bool:
    return any([left_neighbour(x, y),
                right_neighbour(x, y),
                upper_neighbour(x, y),
                lower_neighbour(x, y)])

#def colorize(graph_dict: dict, excalidrawPic: dict, color_map: dict):
def colorize(col_g: any, excalidrawPic: dict, color_map: dict):


    color_dict = nx.coloring.greedy_color(col_g, strategy="largest_first")
    print(color_dict)

    elements = excalidrawPic['elements']

    for elem in elements:
        if elem['type'] == 'line':
            # print(elem['id'])
            #print(elem)

            try:
                no = int(elem['id'].split('-')[1]) + 1
                # print(no)
                # print(color_dict[no])
                color = color_map[color_dict[no]]
                elem['backgroundColor'] = color
            except:
                pass
            # print(color)

    outf = open('D:\\Temp\\Yogi\\out.excalidraw', "w")
    s = json.dumps(excalidrawPic)
    #print(type(excalidrawPic), excalidrawPic)
    outf.write(s)
    outf.close()


if __name__ == '__main__':

    fname = "D:\\Temp\\Yogi\\roman_50.excalidraw"
    inf = open(fname, "r")
    #
    s = json.load(inf)
    #    print(type(s), s, c_map)
    #
    #    colorize(g, s, c_map)

    import tiling_factory as tf

    tiles = tf.make_single_tiling('Roman_50', transformations=[])
    print(type(tiles))
    col_g = nx.Graph()
    tile_list = [t for t in tiles.tiles.values()]
    print(len(tile_list), tile_list)
    for i, tile1 in enumerate(tile_list):
        for j, tile2 in enumerate(tile_list[i+1:]):
            if adjacent(tile1, tile2):
                col_g.add_edge(tile1.id, tile2.id)

    print(col_g.edges)
    colorize(col_g, s, c_map)
