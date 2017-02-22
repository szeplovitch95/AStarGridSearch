from tkinter import *
import random
import time
import math
from searchalgorithms import *
import queue as Q
from copy import copy, deepcopy
from collections import defaultdict
import sys

def initialize_cells_lists(matrix, unblocked_cells, highway_cells, partially_blocked_cells, highway_cells_p_blocked, blocked_cells):
    for y_coo in range(0, 120):
        for x_coo in range(0, 160):
            if matrix[y_coo][x_coo] == '1':
                unblocked_cells.append((x_coo, y_coo))
            if matrix[y_coo][x_coo] == 's':
                unblocked_cells.append((x_coo, y_coo))
            if matrix[y_coo][x_coo] == 'g':
                unblocked_cells.append((x_coo, y_coo))
            if matrix[y_coo][x_coo] == '2':
                partially_blocked_cells.append((x_coo, y_coo))
            if matrix[y_coo][x_coo] == 'a1':
                highway_cells.append((x_coo, y_coo))
            if matrix[y_coo][x_coo] == 'b1':
                highway_cells_p_blocked.append((x_coo, y_coo))
            if matrix[y_coo][x_coo] == 'a2':
                highway_cells.append((x_coo, y_coo))
            if matrix[y_coo][x_coo] == 'b2':
                highway_cells_p_blocked.append((x_coo, y_coo))
            if matrix[y_coo][x_coo] == 'a3':
                highway_cells.append((x_coo, y_coo))
            if matrix[y_coo][x_coo] == 'b3':
                highway_cells_p_blocked.append((x_coo, y_coo))
            if matrix[y_coo][x_coo] == 'a4':
                highway_cells.append((x_coo, y_coo))
            if matrix[y_coo][x_coo] == 'b4':
                highway_cells_p_blocked.append((x_coo, y_coo))
            if matrix[y_coo][x_coo] == '0':
                blocked_cells.append((x_coo, y_coo))


def main(argv, filename):

    unblocked_cells = list()
    highway_cells = list()
    partially_blocked_cells = list()
    highway_cells_p_blocked = list()
    blocked_cells = list()

    # statistics variables
    avg_time = 0
    avg_cost = 0
    avg_nodes_expanded = 0
    avg_memory_usage = 0
    avg_path_length = 0

    # reads the matrix from the random generated values in the file

    with open(filename) as textFile:
        start_coordinates = textFile.readline().strip().split(',')
        end_coordinates = textFile.readline().strip().split(',')
        Matrix = [
            line.split() for line in textFile.readlines()[8:]
            ]

    # algorithm = input("Choose an algorithm: \n 1.Uniform cost\n 2.A star\n 3.Weighted A star\n Enter your choice: ")
    # heuristic = input("Choose a heuristic function:\n 1.Manhattan\n 2.Euclidean\n 3.Chebyshev\n Enter your choice:")

    if argv[1] == '1':
        a = UniformCostSearch(blocked_cells, unblocked_cells, highway_cells, partially_blocked_cells, highway_cells_p_blocked)
    elif argv[1] == '2':
        a = AStarSearch(blocked_cells, unblocked_cells, highway_cells, partially_blocked_cells, highway_cells_p_blocked)
    elif argv[1] == '3':
        a = WeightedAStarSearch(blocked_cells, unblocked_cells, highway_cells, partially_blocked_cells, highway_cells_p_blocked)
    elif argv[1] == '4':
        a = SequentialAStarSearch(blocked_cells, unblocked_cells, highway_cells, partially_blocked_cells, highway_cells_p_blocked)
    elif argv[1] == '5':
        a = IntegratedAStarSearch(blocked_cells, unblocked_cells, highway_cells, partially_blocked_cells, highway_cells_p_blocked)
    else:
        sys.exit(1)

    initialize_cells_lists(Matrix, unblocked_cells, highway_cells, partially_blocked_cells, highway_cells_p_blocked, blocked_cells)
    a.init_all_cells(start_coordinates, end_coordinates)
    a.heuristic = argv[2]

    start_time = time.time()
    path_map, path_cost, nodes_expanded = a.search(Matrix)
    # memory_used = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000

    if path_map is None and path_cost is None and nodes_expanded is None:
        return {
            "time": -1,
            "cost": -1,
            "nodes_expanded": -1,
            "path_length": -1
        }

    for j in range(0, len(path_map)):
        if Matrix[path_map[j].y][path_map[j].x] != 's' and Matrix[path_map[j].y][path_map[j].x] != 'g':
            Matrix[path_map[j].y][path_map[j].x] = 'p'

    print("Some statistics from the search: ")
    print("It took %s seconds to complete" % (time.time() - start_time))
    print("The cost from start to the goal is %s" % (path_cost))
    print("Number of Nodes Expanded: " + str(nodes_expanded))
    # print("Amount of memory used: " + str(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000))
    print("Path length is: " + str(len(path_map)))

    avg_time += (time.time() - start_time)
    avg_cost += path_cost
    avg_nodes_expanded += nodes_expanded
    # avg_memory_usage += resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000
    avg_path_length += len(path_map)

    results = {
        "time": (time.time() - start_time),
        "cost": path_cost,
        "nodes_expanded": nodes_expanded,
        "path_length":  len(path_map)
    }

    """
        Tklinter Drawing parts start here
    """

    y = 0
    width = 160
    height = 120
    root = Tk()
    w = Canvas(root, width=width * 7, height=height * 7)
    cell_x, cell_y = 0, 0
    topLine = StringVar()

    def cell_clicked_event(event):
        cell_x, cell_y = round(event.x / 7), round(event.y / 7)
        f_val, g_val, h_val = a.compute_cell_values(cell_x, cell_y)
        ans = "f=" + str(f_val) + "\t" + "g=" + str(g_val) + "\t" + "h=" + str(
            h_val) + "\t" + "are the values for the coordinates:" + "\t" + "(" + str(cell_x) + "," + str(
            cell_y) + ")"
        topLine.set(ans)

    for x in range(0, width * 7, 7):
        for y in range(0, height * 7, 7):
            if Matrix[round(y / 7)][round(x / 7)] == '0':
                single_cell = w.create_rectangle(x, y, x + 7, y + 7, fill='black')
                w.tag_bind(single_cell, "<ButtonPress-1>", cell_clicked_event)
            if Matrix[round(y / 7)][round(x / 7)] == '1':
                single_cell = w.create_rectangle(x, y, x + 7, y + 7, fill='white')
                w.tag_bind(single_cell, "<ButtonPress-1>", cell_clicked_event)
            elif Matrix[round(y / 7)][round(x / 7)] == 'p':
                single_cell = w.create_rectangle(x, y, x + 7, y + 7, fill='yellow')
                w.tag_bind(single_cell, "<ButtonPress-1>", cell_clicked_event)
            elif Matrix[round(y / 7)][round(x / 7)] == '2':
                single_cell = w.create_rectangle(x, y, x + 7, y + 7, fill='orange')
                w.tag_bind(single_cell, "<ButtonPress-1>", cell_clicked_event)
            elif Matrix[round(y / 7)][round(x / 7)] == 's':
                single_cell = w.create_rectangle(x, y, x + 7, y + 7, fill='green')
                w.tag_bind(single_cell, "<ButtonPress-1>", cell_clicked_event)
            elif Matrix[round(y / 7)][round(x / 7)] == 'g':
                single_cell = w.create_rectangle(x, y, x + 7, y + 7, fill='red')
                w.tag_bind(single_cell, "<ButtonPress-1>", cell_clicked_event)
            elif Matrix[round(y / 7)][round(x / 7)] == 'a1':
                single_cell = w.create_rectangle(x, y, x + 7, y + 7, fill='blue')
                w.tag_bind(single_cell, "<ButtonPress-1>", cell_clicked_event)
            elif Matrix[round(y / 7)][round(x / 7)] == 'b1':
                single_cell = w.create_rectangle(x, y, x + 7, y + 7, fill='blue')
                w.tag_bind(single_cell, "<ButtonPress-1>", cell_clicked_event)
            elif Matrix[round(y / 7)][round(x / 7)] == 'a2':
                single_cell = w.create_rectangle(x, y, x + 7, y + 7, fill='blue')
                w.tag_bind(single_cell, "<ButtonPress-1>", cell_clicked_event)
            elif Matrix[round(y / 7)][round(x / 7)] == 'b2':
                single_cell = w.create_rectangle(x, y, x + 7, y + 7, fill='blue')
                w.tag_bind(single_cell, "<ButtonPress-1>", cell_clicked_event)
            elif Matrix[round(y / 7)][round(x / 7)] == 'a3':
                single_cell = w.create_rectangle(x, y, x + 7, y + 7, fill='blue')
                w.tag_bind(single_cell, "<ButtonPress-1>", cell_clicked_event)
            elif Matrix[round(y / 7)][round(x / 7)] == 'b3':
                single_cell = w.create_rectangle(x, y, x + 7, y + 7, fill='blue')
                w.tag_bind(single_cell, "<ButtonPress-1>", cell_clicked_event)
            elif Matrix[round(y / 7)][round(x / 7)] == 'a4':
                single_cell = w.create_rectangle(x, y, x + 7, y + 7, fill='blue')
                w.tag_bind(single_cell, "<ButtonPress-1>", cell_clicked_event)
            elif Matrix[round(y / 7)][round(x / 7)] == 'b4':
                single_cell = w.create_rectangle(x, y, x + 7, y + 7, fill='blue')
                w.tag_bind(single_cell, "<ButtonPress-1>", cell_clicked_event)


    lab = Label(root, textvariable=topLine)
    lab.pack()
    w.pack()
    root.mainloop()
    return results


if __name__ == "__main__":
    main(sys.argv[:])