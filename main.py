from tkinter import *
import random
import heapq
import time
import math
import queue as Q
from copy import copy, deepcopy
from collections import defaultdict


"""
    This Cell class will used to identify each cell's x,y,h,g,f values
"""

w = 160
h = 120
unblocked_cells = list()
highway_cells = list()
partially_blocked_cells = list()
highway_cells_p_blocked = list()
blocked_cells = list()

#costs
unblocked_to_unblocked = 1


class Cell(object):
    def __init__(self, x, y, blocked):
        self.x = x
        self.y = y
        self.h = 0.0
        self.g = 0.0
        self.f = 0.0
        self.adjacent_cells = []
        self.parent = None
        self.blocked = blocked

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def get_cell(self):
        return self.x, self.y

    def __lt__(self, other):
        return self.f > other.f


class AStar:
    def __init__(self):
        self.cells = []
        self.w = 160
        self.h = 120
        self.opened = []
        self.closed = set()
        self.path = []
        self.startC = ''
        self.endC = ''
        heapq.heapify(self.opened)
        self.algorithm = ''
        self.heuristic = ''

    def init_all_cells(self, start_coord, end_coord):
        for x in range(0, self.w):
            for y in range(0, self.h):
                if(x, y) in blocked_cells:
                    self.cells.append(Cell(x, y, True))
                else:
                    self.cells.append(Cell(x, y, False))

        self.startC = self.get_cell(*start_coord)
        self.endC = self.get_cell(*end_coord)

    def get_cell(self, x_c, y_c):
        if int(x_c) == 160 and int(y_c) == 120:
            x_c = 159
            y_c = 119

        return self.cells[int(x_c) * 120 + int(y_c)]

    def compute_h_value(self, cellX, cellY):
        # Manhattan
        if self.heuristic == '1':
            if self.algorithm == '1':
                return 0
            elif self.algorithm == '2':
                return abs(cellX - self.endC.x) + abs(cellY - self.endC.y)
            else:
                return (abs(cellX - self.endC.x) + abs(cellY - self.endC.y)) * 1.5

        # Euclidean
        if self.heuristic == '2':
            if self.algorithm == '1':
                return 0
            elif self.algorithm == '2':
                return math.sqrt(
                    math.pow(cellX - self.endC.x, 2) + math.pow(cellY - self.endC.y, 2)
                )
            else:
                return math.sqrt(math.pow(cellX - self.endC.x, 2) + math.pow(cellY - self.endC.y, 2)) * 1.5

        # Chebyshev
        if self.heuristic == '3':
            if self.algorithm == '1':
                return 0
            elif self.algorithm == '2':
                return max(abs(cellX - self.endC.x), abs(cellY - self.endC.y))
            else:
                return max(abs(cellX - self.endC.x), abs(cellY - self.endC.y)) * 1.5

    def geth(self, cell, adj):
        return abs(cell.x - adj.x) + abs(cell.y - adj.y)

    def get_adjacent_cells(self, cell):
        adjacent_cells = []
        if cell.y > 0:
            adjacent_cells.append(self.get_cell(cell.x, cell.y - 1))
        if cell.x > 0:
            adjacent_cells.append(self.get_cell(cell.x - 1, cell.y))
        if cell.y < self.h - 1:
            adjacent_cells.append(self.get_cell(cell.x, cell.y + 1))
        if cell.x < self.w - 1:
            adjacent_cells.append(self.get_cell(cell.x + 1, cell.y))
        if cell.y > 0 and cell.x > 0:
            adjacent_cells.append(self.get_cell(cell.x - 1, cell.y - 1))
        if cell.x < self.w - 1 and cell.y > 0:
            adjacent_cells.append(self.get_cell(cell.x + 1, cell.y - 1))
        if cell.x > 0 and cell.y < self.h - 1:
            adjacent_cells.append(self.get_cell(cell.x - 1, cell.y + 1))
        if cell.y < self.h - 1 and cell.x < self.w - 1:
            adjacent_cells.append(self.get_cell(cell.x + 1, cell.y + 1))

        return adjacent_cells

    def get_cost(self, cell, adjacent):
        cell_xy = [(cell.x, cell.y)]
        adj_xy = [(adjacent.x, adjacent.y)]
        direction = ""

        if adjacent.x == cell.x + 1 and adjacent.y == cell.y + 1:
            direction = "D"
        elif adjacent.x == cell.x - 1 and adjacent.y == cell.y + 1:
            direction = "D"
        elif adjacent.x == cell.x + 1 and adjacent.y == cell.y - 1:
            direction = "D"
        elif adjacent.x == cell.x - 1 and adjacent.y == cell.y - 1:
            direction = "D"
        else:
            direction = "ND"

        if direction == "ND":
            if cell_xy[0] in unblocked_cells and adj_xy[0] in unblocked_cells:
                return 1
            if cell_xy[0] in unblocked_cells and adj_xy[0] in partially_blocked_cells:
                return 1.5
            if cell_xy[0] in unblocked_cells and adj_xy[0] in highway_cells:
                return 0.25
            if cell_xy[0] in unblocked_cells and adj_xy[0] in highway_cells_p_blocked:
                return 0.375

            # hard to traverse cell to other cells
            if cell_xy[0] in partially_blocked_cells and adj_xy[0] in partially_blocked_cells:
                return 2
            if cell_xy[0] in partially_blocked_cells and adj_xy[0] in unblocked_cells:
                return 1.5
            if cell_xy[0] in partially_blocked_cells and adj_xy[0] in highway_cells:
                return 0.375
            if cell_xy[0] in partially_blocked_cells and adj_xy[0] in highway_cells_p_blocked:
                return 0.5

            # unblocked highway  to other cells
            if cell_xy[0] in highway_cells and adj_xy[0] in highway_cells:
                return 0.25
            if cell_xy[0] in highway_cells and adj_xy[0] in unblocked_cells:
                return 1
            if cell_xy[0] in highway_cells and adj_xy[0] in partially_blocked_cells:
                return 1.5
            if cell_xy[0] in highway_cells and adj_xy[0] in highway_cells_p_blocked:
                return 0.375

            # hard - highway to other cells
            if cell_xy[0] in highway_cells_p_blocked and adj_xy[0] in highway_cells_p_blocked:
                return 0.5
            if cell_xy[0] in highway_cells_p_blocked and adj_xy[0] in unblocked_cells:
                return 1.5
            if cell_xy[0] in highway_cells_p_blocked and adj_xy[0] in partially_blocked_cells:
                return 2
            if cell_xy[0] in highway_cells_p_blocked and adj_xy[0] in highway_cells:
                return 0.375

        if direction == "D":
            if cell_xy[0] in unblocked_cells and adj_xy[0] in unblocked_cells:
                return math.sqrt(2)
            if cell_xy[0] in unblocked_cells and adj_xy[0] in partially_blocked_cells:
                return (math.sqrt(2) + math.sqrt(8)) / 2
            if cell_xy[0] in unblocked_cells and adj_xy[0] in highway_cells:
                return math.sqrt(2) / 4
            if cell_xy[0] in unblocked_cells and adj_xy[0] in highway_cells_p_blocked:
                return ((math.sqrt(2) + math.sqrt(8)) / 2) / 4

                # hard to traverse cell to other cells
            if cell_xy[0] in partially_blocked_cells and adj_xy[0] in partially_blocked_cells:
                return math.sqrt(8)
            if cell_xy[0] in partially_blocked_cells and adj_xy[0] in unblocked_cells:
                return (math.sqrt(2) + math.sqrt(8)) / 2
            if cell_xy[0] in partially_blocked_cells and adj_xy[0] in highway_cells:
                return ((math.sqrt(2) + math.sqrt(8)) / 2) / 4
            if cell_xy[0] in partially_blocked_cells and adj_xy[0] in highway_cells_p_blocked:
                return math.sqrt(8) / 4

                # unblocked highway  to other cells
            if cell_xy[0] in highway_cells and adj_xy[0] in highway_cells:
                return math.sqrt(2) / 4
            if cell_xy[0] in highway_cells and adj_xy[0] in unblocked_cells:
                return math.sqrt(2)
            if cell_xy[0] in highway_cells and adj_xy[0] in partially_blocked_cells:
                return (math.sqrt(2) + math.sqrt(8)) / 2
            if cell_xy[0] in highway_cells and adj_xy[0] in highway_cells_p_blocked:
                return ((math.sqrt(2) + math.sqrt(8)) / 2) / 4

                # hard - highway to other cells
            if cell_xy[0] in highway_cells_p_blocked and adj_xy[0] in highway_cells_p_blocked:
                return math.sqrt(8) / 4
            if cell_xy[0] in highway_cells_p_blocked and adj_xy[0] in unblocked_cells:
                return ((math.sqrt(2) + math.sqrt(8)) / 2) / 4
            if cell_xy[0] in highway_cells_p_blocked and adj_xy[0] in partially_blocked_cells:
                return math.sqrt(8)
            if cell_xy[0] in highway_cells_p_blocked and adj_xy[0] in highway_cells:
                return ((math.sqrt(2) + math.sqrt(8)) / 2) / 4

    def compute_cell_values(self, x, y):
        cell = self.get_cell(x, y)
        return cell.f, cell.g, cell.h

    def get_solution(self):
        heapq.heappush(self.opened, (self.startC.f, self.startC))
        self.startC.g = 0
        self.startC.h = self.compute_h_value(self.startC.x, self.startC.y)
        self.startC.f = self.startC.g + self.startC.h

        while len(self.opened):
            f_val, cell = heapq.heappop(self.opened)
            self.closed.add(cell)
            self.path.append(cell)
            # if this is true that means we find the goal cell and its over.
            if cell == self.endC:
                return self.path, self.endC.g, len(self.closed)

            adjacent_cells = self.get_adjacent_cells(cell)
            for adjacent in adjacent_cells:
                if adjacent not in self.closed and not adjacent.blocked:
                    adjacent.g = cell.g + self.get_cost(cell, adjacent)
                    adjacent.h = self.compute_h_value(adjacent.x, adjacent.y)
                    adjacent.f = adjacent.g + adjacent.h

                    if len(self.opened) == 0:
                        heapq.heappush(self.opened, (adjacent.f, adjacent))
                    else:
                        f, node = heapq.heappop(self.opened)
                        if adjacent.f < f:
                            heapq.heappush(self.opened, (adjacent.f, adjacent))
                        else:
                            heapq.heappush(self.opened, (f, node))


def initialize_cells_lists(matrix):
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
            if matrix[y_coo][x_coo] == 'a':
                highway_cells.append((x_coo, y_coo))
            if matrix[y_coo][x_coo] == 'b':
                highway_cells_p_blocked.append((x_coo, y_coo))
            if matrix[y_coo][x_coo] == '0':
                blocked_cells.append((x_coo, y_coo))

# reads the matrix from the random generated values in the file
with open("map.txt") as textFile:
    start_coordinates = textFile.readline().strip().split(',')
    end_coordinates = textFile.readline().strip().split(',')
    Matrix = [
            line.split() for line in textFile.readlines()[8:]
        ]

algorithm = input("Choose an algorithm: \n 1.Uniform cost\n 2.A star\n 3.Weighted A star\n Enter your choice: ")
heuristic = input("Choose a heuristic function:\n 1.Manhattan\n 2.Euclidean\n 3.Chebyshev\n Enter your choice:")

a = AStar()
initialize_cells_lists(Matrix)
a.init_all_cells(start_coordinates, end_coordinates)
a.algorithm = algorithm
a.heuristic = heuristic
start_time = time.time()
path_map, path_cost, length = a.get_solution()

for j in range(0, len(path_map)):
    if Matrix[path_map[j].y][path_map[j].x] != 's' and Matrix[path_map[j].y][path_map[j].x] != 'g':
        Matrix[path_map[j].y][path_map[j].x] = 'p'

print("Some statistics from the search: ")
print("It took %s seconds to complete" % (time.time() - start_time))
print("The cost from start to the goal is %s" %(path_cost))


"""
    Tklinter Drawing parts start here
"""
root = Tk()
y = 0
width = 160
height = 120

w = Canvas(root, width=width * 7, height=height * 7)
cell_x, cell_y = 0, 0
topLine = StringVar()

def cell_clicked_event(event):
    cell_x, cell_y = round(event.x / 7), round(event.y / 7)
    f_val, g_val, h_val = a.compute_cell_values(cell_x, cell_y)
    ans = "f=" + str(f_val) + "\t" + "g=" + str(g_val) + "\t" + "h=" + str(h_val) + "\t" + "are the values for the coordinates:" + "\t" + "(" + str(cell_x) + "," + str(cell_y) + ")"
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
        elif Matrix[round(y / 7)][round(x / 7)] == 'a':
            single_cell = w.create_rectangle(x, y, x + 7, y + 7, fill='blue')
            w.tag_bind(single_cell, "<ButtonPress-1>", cell_clicked_event)
        elif Matrix[round(y / 7)][round(x / 7)] == 'b':
            single_cell = w.create_rectangle(x, y, x + 7, y + 7, fill='blue')
            w.tag_bind(single_cell, "<ButtonPress-1>", cell_clicked_event)


lab = Label(root, textvariable=topLine)
lab.pack()
w.pack()
root.mainloop()