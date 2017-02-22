import heapq
import math
import sys
from queue import PriorityQueue


"""
    This file contains the various different search algorithms
"""

#Globals
w = 160
h = 120

"""
    This Cell class will used to identify each cell's x,y,h,g,f values
"""

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
        return self.g < other.g


class SearchAlgorithm(object):
    def __init__(self):
        self.cells = []
        self.w = 160
        self.h = 120
        self.opened = []
        self.closed = set()
        self.closedAnchor = []
        self.closedInad = []
        self.path = []
        self.pathL = [ [], [], [], [] ]
        self.startC = ''
        self.endC = ''
        heapq._heapify_max(self.opened)
        self.algorithm = ''
        self.heuristic = ''
        #This is the list of 4 open lists (one for each of the heuristic)
        self.listOfFringes = [ [], [], [], [] ]
        self.closedL = [ [], [], [], [] ]


    # Abstract method
    def compute_h_value(self, cellX, cellY):
        pass

    def init_all_cells(self, start_coord, end_coord):
        for x in range(0, self.w):
            for y in range(0, self.h):
                if(x, y) in self.blocked_cells:
                    self.cells.append(Cell(x, y, True))
                else:
                    self.cells.append(Cell(x, y, False))

        self.startC = self.get_cell(*start_coord)
        self.endC = self.get_cell(*end_coord)

    def get_cell(self, x_c, y_c):
        if int(x_c) == 160:
            x_c = 159

        if int(y_c) == 120:
            y_c = 119

        return self.cells[int(x_c) * 120 + int(y_c)]

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
            if cell_xy[0] in self.unblocked_cells and adj_xy[0] in self.unblocked_cells:
                return 1
            if cell_xy[0] in self.unblocked_cells and adj_xy[0] in self.partially_blocked_cells:
                return 1.5
            if cell_xy[0] in self.unblocked_cells and adj_xy[0] in self.highway_cells:
                return 0.25
            if cell_xy[0] in self.unblocked_cells and adj_xy[0] in self.highway_cells_p_blocked:
                return 0.375

            # hard to traverse cell to other cells
            if cell_xy[0] in self.partially_blocked_cells and adj_xy[0] in self.partially_blocked_cells:
                return 2
            if cell_xy[0] in self.partially_blocked_cells and adj_xy[0] in self.unblocked_cells:
                return 1.5
            if cell_xy[0] in self.partially_blocked_cells and adj_xy[0] in self.highway_cells:
                return 0.375
            if cell_xy[0] in self.partially_blocked_cells and adj_xy[0] in self.highway_cells_p_blocked:
                return 0.5

            # unblocked highway  to other cells
            if cell_xy[0] in self.highway_cells and adj_xy[0] in self.highway_cells:
                return 0.25
            if cell_xy[0] in self.highway_cells and adj_xy[0] in self.unblocked_cells:
                return 1
            if cell_xy[0] in self.highway_cells and adj_xy[0] in self.partially_blocked_cells:
                return 1.5
            if cell_xy[0] in self.highway_cells and adj_xy[0] in self.highway_cells_p_blocked:
                return 0.375

            # hard - highway to other cells
            if cell_xy[0] in self.highway_cells_p_blocked and adj_xy[0] in self.highway_cells_p_blocked:
                return 0.5
            if cell_xy[0] in self.highway_cells_p_blocked and adj_xy[0] in self.unblocked_cells:
                return 1.5
            if cell_xy[0] in self.highway_cells_p_blocked and adj_xy[0] in self.partially_blocked_cells:
                return 2
            if cell_xy[0] in self.highway_cells_p_blocked and adj_xy[0] in self.highway_cells:
                return 0.375

        if direction == "D":
            if cell_xy[0] in self.unblocked_cells and adj_xy[0] in self.unblocked_cells:
                return math.sqrt(2)
            if cell_xy[0] in self.unblocked_cells and adj_xy[0] in self.partially_blocked_cells:
                return (math.sqrt(2) + math.sqrt(8)) / 2
            if cell_xy[0] in self.unblocked_cells and adj_xy[0] in self.highway_cells:
                return math.sqrt(2) / 4
            if cell_xy[0] in self.unblocked_cells and adj_xy[0] in self.highway_cells_p_blocked:
                return ((math.sqrt(2) + math.sqrt(8)) / 2) / 4

                # hard to traverse cell to other cells
            if cell_xy[0] in self.partially_blocked_cells and adj_xy[0] in self.partially_blocked_cells:
                return math.sqrt(8)
            if cell_xy[0] in self.partially_blocked_cells and adj_xy[0] in self.unblocked_cells:
                return (math.sqrt(2) + math.sqrt(8)) / 2
            if cell_xy[0] in self.partially_blocked_cells and adj_xy[0] in self.highway_cells:
                return ((math.sqrt(2) + math.sqrt(8)) / 2) / 4
            if cell_xy[0] in self.partially_blocked_cells and adj_xy[0] in self.highway_cells_p_blocked:
                return math.sqrt(8) / 4

                # unblocked highway  to other cells
            if cell_xy[0] in self.highway_cells and adj_xy[0] in self.highway_cells:
                return math.sqrt(2) / 4
            if cell_xy[0] in self.highway_cells and adj_xy[0] in self.unblocked_cells:
                return math.sqrt(2)
            if cell_xy[0] in self.highway_cells and adj_xy[0] in self.partially_blocked_cells:
                return (math.sqrt(2) + math.sqrt(8)) / 2
            if cell_xy[0] in self.highway_cells and adj_xy[0] in self.highway_cells_p_blocked:
                return ((math.sqrt(2) + math.sqrt(8)) / 2) / 4

                # hard - highway to other cells
            if cell_xy[0] in self.highway_cells_p_blocked and adj_xy[0] in self.highway_cells_p_blocked:
                return math.sqrt(8) / 4
            if cell_xy[0] in self.highway_cells_p_blocked and adj_xy[0] in self.unblocked_cells:
                return ((math.sqrt(2) + math.sqrt(8)) / 2) / 4
            if cell_xy[0] in self.highway_cells_p_blocked and adj_xy[0] in self.partially_blocked_cells:
                return math.sqrt(8)
            if cell_xy[0] in self.highway_cells_p_blocked and adj_xy[0] in self.highway_cells:
                return ((math.sqrt(2) + math.sqrt(8)) / 2) / 4

    def compute_cell_values(self, x, y):
        cell = self.get_cell(x, y)
        return cell.f, cell.g, cell.h

    def search(self, matrix):

        heapq.heappush(self.opened, (self.startC.f, self.startC))
        self.startC.g = 0
        self.startC.h = self.compute_h_value(self.startC.x, self.startC.y)
        self.startC.f = self.startC.g + self.startC.h

        while len(self.opened):
            f_val, cell = heapq.heappop(self.opened)
            self.closed.add(cell)
            # print(f_val)
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
        return None, None, None


class AStarSearch(SearchAlgorithm):
    def __init__(self, blocked_cells, unblocked_cells, highway_cells, partially_blocked_cells, highway_cells_p_blocked):
        super().__init__()
        self.blocked_cells = blocked_cells
        self.unblocked_cells = unblocked_cells
        self.highway_cells = highway_cells
        self.highway_cells_p_blocked = highway_cells_p_blocked
        self.partially_blocked_cells = partially_blocked_cells

    def compute_h_value(self, cellX, cellY):
        # Manhattan Distance
        if self.heuristic == '1':
            return abs(cellX - self.endC.x) + abs(cellY - self.endC.y)

        # Euclidean Distance
        elif self.heuristic == '2':
            return math.sqrt(math.pow(cellX - self.endC.x, 2) + math.pow(cellY - self.endC.y, 2))

        # Chebyshev Distance
        elif self.heuristic == '3':
            return max(abs(cellX - self.endC.x), abs(cellY - self.endC.y))

        # Diagonal Distance
        elif self.heuristic == '4':
            return math.sqrt(
                math.pow((self.endC.x - cellX), 2) + math.pow((self.endC.y - cellY), 2)
            )

        # Diagonal Distance divided by 4 for never overestimating when on highways.
        elif self.heuristic == '5':
            return math.sqrt(
                math.pow((self.endC.x - cellX), 2) + math.pow((self.endC.y - cellY), 2)
            ) / 4


class WeightedAStarSearch(SearchAlgorithm):
    def __init__(self, blocked_cells, unblocked_cells, highway_cells, partially_blocked_cells, highway_cells_p_blocked):
        super().__init__()
        self.blocked_cells = blocked_cells
        self.unblocked_cells = unblocked_cells
        self.highway_cells = highway_cells
        self.highway_cells_p_blocked = highway_cells_p_blocked
        self.partially_blocked_cells = partially_blocked_cells

    def compute_h_value(self, cellX, cellY):
        # Manhattan Distance
        if self.heuristic == '1':
            return (abs(cellX - self.endC.x) + abs(cellY - self.endC.y)) * 2

        # Euclidean Distance
        elif self.heuristic == '2':
            return (math.sqrt(math.pow(cellX - self.endC.x, 2) + math.pow(cellY - self.endC.y, 2))) * 2

        # Chebyshev Distance
        elif self.heuristic == '3':
            return (max(abs(cellX - self.endC.x), abs(cellY - self.endC.y))) * 2

        # Diagonal Distance
        elif self.heuristic == '4':
            return math.sqrt(
                math.pow((self.endC.x - cellX), 2) + math.pow((self.endC.y - cellY), 2)
            ) * 2

        # Diagonal Distance divided by 4 for never overestimating when on highways.
        elif self.heuristic == '5':
            return (math.sqrt(
                math.pow((self.endC.x - cellX), 2) + math.pow((self.endC.y - cellY), 2)
            ) / 4) * 2

class UniformCostSearch(SearchAlgorithm):
    def __init__(self, blocked_cells, unblocked_cells, highway_cells, partially_blocked_cells, highway_cells_p_blocked):
        super().__init__()
        self.blocked_cells = blocked_cells
        self.unblocked_cells = unblocked_cells
        self.highway_cells = highway_cells
        self.highway_cells_p_blocked = highway_cells_p_blocked
        self.partially_blocked_cells = partially_blocked_cells

    def compute_h_value(self, cellX, cellY):
        return 0

    def search(self, matrix):
        self.startC.g = 0
        self.startC.f = 0

        visited = set()
        path = []

        queue = PriorityQueue()
        queue.put((self.startC.g, self.startC))
        path.append(self.startC)

        while queue:
            cost, node = queue.get()
            if node not in visited:
                visited.add(node)
                path.append(node)

                if node == self.endC:
                    path.append(node)
                    return path, node.g, len(path)

                neighbors = self.get_adjacent_cells(node)
                for i in neighbors:
                    if i not in visited and not i.blocked:
                        total_cost = cost + self.get_cost(node, i)
                        i.g = total_cost
                        queue.put((i.g, i))

        return None, None, None


class SequentialAStarSearch(SearchAlgorithm):
    def __init__(self, blocked_cells, unblocked_cells, highway_cells, partially_blocked_cells, highway_cells_p_blocked):
        super().__init__()
        self.blocked_cells = blocked_cells
        self.unblocked_cells = unblocked_cells
        self.highway_cells = highway_cells
        self.highway_cells_p_blocked = highway_cells_p_blocked
        self.partially_blocked_cells = partially_blocked_cells

    def compute_h_value(self, cellX, cellY, i):
        # Manhattan
        if i == '0':
            return (abs(cellX - self.endC.x) + abs(cellY - self.endC.y)) * 1.5

        # Euclidean
        elif i == '1':
            print("weighted A star working")
            return (math.sqrt(math.pow(cellX - self.endC.x, 2) + math.pow(cellY - self.endC.y, 2))) * 1.5

        # Chebyshev
        elif i == '2':
            print("weighted A star working")
            return (max(abs(cellX - self.endC.x), abs(cellY - self.endC.y))) * 1.5

        # Diagonal Distance
        else:
            return (math.sqrt(
                math.pow((self.endC.x - cellX), 2) + math.pow((self.endC.y - cellY), 2)
            )) * 1.5

    def expandState(self, i):
        self.startC.g = 0
        self.startC.h = self.compute_h_value(self.startC.x, self.startC.y, i)
        self.startC.f = self.startC.g + self.startC.h

        f_val, cell = heapq.heappop(self.listOfFringes[i])
        self.closedL[i].append(cell)
        self.pathL[i].append(cell)

        adjacent_cells = self.get_adjacent_cells(cell)
        for adjacent in adjacent_cells:
            if adjacent not in self.closedL[i] and not adjacent.blocked:
                adjacent.g = cell.g + self.get_cost(cell, adjacent)
                adjacent.h = self.compute_h_value(adjacent.x, adjacent.y, i)
                adjacent.f = adjacent.g + adjacent.h

                if len(self.listOfFringes[i]) == 0:
                    heapq.heappush(self.listOfFringes[i], (adjacent.f, adjacent))
                else:
                    f, node = heapq.heappop(self.listOfFringes[i])
                    if adjacent.f < f:
                        heapq.heappush(self.listOfFringes[i], (adjacent.f, adjacent))
                    else:
                        heapq.heappush(self.listOfFringes[i], (f, node))

    # 1.5 used for both weight values
    def search(self, matrix):
        # There are four heuristics: manhattan, euclidian, chebyshev, diagonal
        for i in range(4):
            self.startC.g = 0
            # we know 500 is larger than any possible g value so it acts as "infinity"
            self.endC.g = 500
            heapq.heapify(self.listOfFringes[i])
            # insert start cell in this heap
            self.startC.f = 1.5 * self.compute_h_value(self.startC.x, self.startC.y, i)
            heapq.heappush(self.listOfFringes[i], (self.startC.f, self.startC))

        f_val_0, cell_0 = heapq.nsmallest(1, self.listOfFringes[0])[0]
        while f_val_0 < 500:
            f_val_0, cell_0 = heapq.nsmallest(1, self.listOfFringes[0])[0]
            for i in range(1, 4):
                f_val_i, cell_i = heapq.nsmallest(1, self.listOfFringes[i])[0]
                if f_val_i <= 1.5 * f_val_0:
                    if self.endC.g <= f_val_i:
                        if self.endC.g <= 500:
                            return self.pathL[i], self.endC.g, len(self.closedL[i])
                    else:
                        self.expandState(i)
                else:
                    if self.endC.g <= f_val_0:
                        if self.endC.g <= 500:
                            return self.pathL[0], self.endC.g, len(self.closedL[0])
                    else:
                        self.expandState(0)
        return None, None, None


class IntegratedAStarSearch(SearchAlgorithm):
    def __init__(self, blocked_cells, unblocked_cells, highway_cells, partially_blocked_cells, highway_cells_p_blocked):
        super().__init__()
        self.blocked_cells = blocked_cells
        self.unblocked_cells = unblocked_cells
        self.highway_cells = highway_cells
        self.highway_cells_p_blocked = highway_cells_p_blocked
        self.partially_blocked_cells = partially_blocked_cells


    def compute_h_value(self, cellX, cellY, i):
        # Manhattan
        if i == '0':
            return (abs(cellX - self.endC.x) + abs(cellY - self.endC.y)) * 1.5

        # Euclidean
        elif i == '1':
            print("weighted A star working")
            return (math.sqrt(math.pow(cellX - self.endC.x, 2) + math.pow(cellY - self.endC.y, 2))) * 1.5

        # Chebyshev
        elif i == '2':
            print("weighted A star working")
            return (max(abs(cellX - self.endC.x), abs(cellY - self.endC.y))) * 1.5

        # Diagonal Distance
        else:
            return (math.sqrt(
                math.pow((self.endC.x - cellX), 2) + math.pow((self.endC.y - cellY), 2)
            )) * 1.5

    def Key(self, cell, i):
        return cell.g + self.compute_h_value(cell.x, cell.y, i)

    # if anchor is 1 use anchor if it's 0 use inad
    def expandState(self, i, anchor):
        # from all fringes, pop element
        # for i in range(4):
        f_val, cell = heapq.heappop(self.listOfFringes[i])
        if anchor == 1:
            self.closedAnchor.append(cell)
        elif anchor == 0:
            self.closedInad.append(cell)
        self.startC.g = 0
        self.startC.h = self.compute_h_value(self.startC.x, self.startC.y, i)
        self.startC.f = self.startC.g + self.startC.h

        self.closedL[i].append(cell)
        self.path.append(cell)

        adjacent_cells = self.get_adjacent_cells(cell)
        for adjacent in adjacent_cells:
            if adjacent not in self.closedAnchor and not adjacent.blocked:
                adjacent.g = cell.g + self.get_cost(cell, adjacent)
                adjacent.h = self.compute_h_value(adjacent.x, adjacent.y, i)
                adjacent.f = adjacent.g + adjacent.h

                if len(self.listOfFringes[i]) == 0:
                    heapq.heappush(self.listOfFringes[i], (adjacent.f, adjacent))
                else:
                    f, node = heapq.heappop(self.listOfFringes[i])
                    if adjacent.f < f:
                        heapq.heappush(self.listOfFringes[i], (adjacent.f, adjacent))
                    else:
                        heapq.heappush(self.listOfFringes[i], (f, node))

                if adjacent not in self.closedInad:
                    for i in range(1, 4):
                        if self.Key(adjacent, i) <= 1.5 * self.Key(adjacent, 0):
                            heapq.heappush(self.listOfFringes[i], (self.Key(adjacent, i), adjacent))

    def search(self, matrix):
        self.startC.g = 0
        self.endC.g = 500
        # There are four heuristics: manhattan, euclidian, chebyshev, diagonal
        for i in range(4):
            heapq.heapify(self.listOfFringes[i])
            # insert start cell in this heap
            self.startC.f = 1.5 * self.compute_h_value(self.startC.x, self.startC.y, i)
            heapq.heappush(self.listOfFringes[i], (self.startC.f, self.startC))
        f_val_0, cell_0 = heapq.nsmallest(1, self.listOfFringes[0])[0]
        while f_val_0 < 500:
            f_val_0, cell_0 = heapq.nsmallest(1, self.listOfFringes[0])[0]
            for i in range(1, 4):
                f_val_i, cell_i = heapq.nsmallest(1, self.listOfFringes[i])[0]
                if f_val_i <= 1.5 * f_val_0:
                    if self.endC.g <= f_val_i:
                        if self.endC.g <= 500:
                            return self.path, self.endC.g, len(self.closed)
                    else:
                        self.expandState(i, 0)
                else:
                    if self.endC.g <= f_val_0:
                        if self.endC.g <= 500:
                            return self.path, self.endC.g, len(self.closed)
                    else:
                        self.expandState(i, 1)
        return None, None, None