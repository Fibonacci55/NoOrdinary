
import networkx as nx
import json


g = {
    1: [2, 3, 4],
    2: [1, 4, 5],
    3: [1, 4],
    4: [1, 2, 3, 4, 5, 6, 6, 8],
    5: [2,4,6, 9],
    6: [4, 5, 8, 9],
    7: [4, 8, 21],
    8: [4, 6, 7, 22],
    9: [5, 6, 30],
    10: [5, 11],

    11: [12, 13, 14, 5],
    12: [11, 14, 15],
    13: [11, 14, 5, 9],
    14: [11, 12, 13, 14, 15, 16, 17, 18],
    15: [12, 14, 16, 19],
    16: [14, 15, 18, 19],
    17: [14, 18],
    18: [14, 16, 17],
    19: [15, 16],
    20: [15],

    21: [22, 23, 24, 8],
    22: [21, 24, 25],
    23: [21, 24],
    24: [21, 22, 23, 24, 25, 26, 27, 28],
    25: [22, 24, 26, 29, 8],
    26: [24, 25, 28, 29],
    27: [24, 28],
    28: [24, 26, 27],
    29: [25, 26, 33, 37],
    30: [25],

    31: [32, 33, 34],
    32: [31, 34, 35],
    33: [31, 34],
    34: [31, 32, 33, 34, 35, 36, 37, 38],
    35: [32, 34, 36, 39],
    36: [34, 35, 38, 39],
    37: [34, 38],
    38: [34, 36, 37, 55],
    39: [35, 36],
    40: [35],

    41: [32, 33, 34],
    42: [31, 34, 35],
    44: [31, 32, 33, 34, 35, 36, 37, 38],
    45: [32, 34, 36, 39],
    50: [45, 28, 29, 51],

    51: [52, 53, 54],
    52: [51, 54, 55],
    53: [51, 54],
    54: [51, 52, 53, 54, 55, 56, 57, 58],
    55: [52, 54],

}

c_map = {
    0: '#AC2727',
    1: '#243A73',
    2: '#ACAB27',
    3: '#1F932D'
}


def is_cover(i_one: int, i_two:int) -> bool:




def colorize(graph_dict: dict, excalidrawPic: dict, color_map: dict):

    col_g = nx.Graph()
    for k in graph_dict:
        #print(k)
        edges = graph_dict[k]
        for e in edges:
            col_g.add_edge(k, e)


    color_dict = nx.coloring.greedy_color(col_g, strategy="largest_first")
    print(color_dict)

    elements = excalidrawPic['elements']

    for elem in elements:
        if elem['type'] == 'line':
            #print(elem['id'])
            print(elem)

            try:
                no = int(elem['id'].split('-')[1]) + 1
            #print(no)
            #print(color_dict[no])
                color = color_map[color_dict[no]]
                elem['backgroundColor'] = color
            except:
                pass
            #print(color)

    outf = open('C:\\Temp\\out.excalidraw', "w")
    s = json.dumps( excalidrawPic)
    print(type(excalidrawPic), excalidrawPic)
    outf.write(s)
    outf.close()

if __name__ == '__main__':

    fname = "C:\\Temp\\XXX.excalidraw"
    inf = open(fname, "r")

    s = json.load(inf)
    print(type(s), s, c_map)

    colorize(g, s, c_map)