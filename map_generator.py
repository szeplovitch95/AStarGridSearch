import random
from copy import copy, deepcopy
import sys
from os import path

w = 160
h = 120

MAP_DIRECTORY = path.join(path.dirname(__file__), "maps")

def print_matrix(matrix):
    answer = ''
    for i, val in enumerate(matrix):
        print('\t'.join(val))
        answer += '\t'.join(val) + '\n'

    return answer


"""
    This function generates random numbers into two lists
    which are used as (x,y) coordinates to mark the hard-to-traverse cells
"""


def get_hard_cells_coordinates():
    x = []
    y = []
    for i in range(0, 8):
        x_rand = random.randrange(0, 160)
        y_rand = random.randrange(0, 120)

        if x_rand in x and y_rand in y:
            continue
        else:
            x.append(x_rand)
            y.append(y_rand)

    return x, y


"""
    This function generates random numbers into two lists
    which are used as (x,y) coordinates to mark the blocked cells
"""


def get_blocked_cells_coordinates(matrix):
    m = []
    n = []
    count = 0
    while count < 3840:
        m_rand = random.randrange(0, 160)
        n_rand = random.randrange(0, 120)
        if matrix[n_rand][m_rand] == 'a1' or matrix[n_rand][m_rand] == 'b1':
            continue
        if matrix[n_rand][m_rand] == 'a2' or matrix[n_rand][m_rand] == 'b2':
            continue
        if matrix[n_rand][m_rand] == 'a3' or matrix[n_rand][m_rand] == 'b3':
            continue
        if matrix[n_rand][m_rand] == 'a4' or matrix[n_rand][m_rand] == 'b4':
            continue
        else:
            m.append(m_rand)
            n.append(n_rand)
            count += 1

    return m, n


def generate_random_highway_point(region_num):
    if region_num == 1:
        x_random = random.randrange(0, 159)
        y_random = 0
    if region_num == 2:
        x_random = random.randrange(0, 159)
        y_random = 119
    if region_num == 3:
        x_random = 0
        y_random = random.randrange(0, 119)
    if region_num == 4:
        x_random = 159
        y_random = random.randrange(0, 119)

    return x_random, y_random


def add_more_highways(matrix, highway_x, highway_y, direction, highway, highway_num):
    # print(direction)
    while 0 <= highway_x < w and 0 <= highway_y < h:
        if direction == "top":
            prob = random.randint(1, 5)
            # move same direction
            if prob >= 3:
                for j in range(0, 20):
                    if highway_y >= 0 and highway_y != h and highway_x >= 0 and highway_x != w:
                        if matrix[highway_y][highway_x] == '2':
                            matrix[highway_y][highway_x] = 'b' + str(highway_num)
                            highway.append((highway_x, highway_y))
                        elif matrix[highway_y][highway_x] == '1':
                            matrix[highway_y][highway_x] = 'a' + str(highway_num)
                            highway.append((highway_x, highway_y))
                        else:
                            return False
                    else:
                        return True
                    highway_y -= 1
            elif prob == 2:
                #move right
                direction = "right"
                for j in range(0, 20):
                    if highway_y >= 0 and highway_y != h and highway_x >= 0 and highway_x != w:
                        if matrix[highway_y][highway_x] == '2':
                            matrix[highway_y][highway_x] = 'b' + str(highway_num)
                            highway.append((highway_x + j, highway_y))
                        elif matrix[highway_y][highway_x] == '1':
                            matrix[highway_y][highway_x] = 'a' + str(highway_num)
                            highway.append((highway_x, highway_y))
                        else:
                            return False
                    else:
                        return True
                    highway_x += 1
            else:
                #move left
                direction = "left"
                for j in range(0, 20):
                    if highway_y >= 0 and highway_y != h and highway_x >= 0 and highway_x != w:
                        if matrix[highway_y][highway_x] == '2':
                            matrix[highway_y][highway_x] = 'b' + str(highway_num)
                            highway.append((highway_x, highway_y))
                        elif matrix[highway_y][highway_x] == '1':
                            matrix[highway_y][highway_x] = 'a' + str(highway_num)
                            highway.append((highway_x, highway_y))
                        else:
                            return False
                    else:
                        return True
                    highway_x -= 1
        elif direction == "bottom":
            prob = random.randint(1, 5)
            # move same direction
            if prob >= 3:
                for j in range(0, 20):
                    if highway_y >= 0 and highway_y != h and highway_x >= 0 and highway_x != w:
                        if matrix[highway_y][highway_x] == '2':
                            matrix[highway_y][highway_x] = 'b' + str(highway_num)
                            highway.append((highway_x, highway_y))
                        elif matrix[highway_y][highway_x] == '1':
                            matrix[highway_y][highway_x] = 'a' + str(highway_num)
                            highway.append((highway_x, highway_y))
                        else:
                            return False
                    else:
                        return True
                    highway_y += 1
            elif prob == 2:
                # move right
                direction = "left"
                for j in range(0, 20):
                    if highway_y >= 0 and highway_y != h and highway_x >= 0 and highway_x != w:
                        if matrix[highway_y][highway_x] == '2':
                            matrix[highway_y][highway_x] = 'b' + str(highway_num)
                            highway.append((highway_x, highway_y))
                        elif matrix[highway_y][highway_x] == '1':
                            matrix[highway_y][highway_x] = 'a' + str(highway_num)
                            highway.append((highway_x, highway_y))
                        else:
                            return False
                    else:
                        return True
                    highway_x -= 1
            else:
                # move left
                direction = "right"
                for j in range(0, 20):
                    if highway_y >= 0 and highway_y != h and highway_x >= 0 and highway_x != w:
                        if matrix[highway_y][highway_x] == '2':
                            matrix[highway_y][highway_x] = 'b' + str(highway_num)
                            highway.append((highway_x, highway_y))
                        elif matrix[highway_y][highway_x] == '1':
                            matrix[highway_y][highway_x] = 'a' + str(highway_num)
                            highway.append((highway_x, highway_y))
                        else:
                            return False
                    else:
                        return True
                    highway_x += 1
        elif direction == "left":
            prob = random.randint(1, 5)
            # move same direction
            if prob >= 3:
                for j in range(0, 20):
                    if highway_y >= 0 and highway_y != h and highway_x >= 0 and highway_x != w:
                        if matrix[highway_y][highway_x] == '2':
                            matrix[highway_y][highway_x] = 'b' + str(highway_num)
                            highway.append((highway_x, highway_y))
                        elif matrix[highway_y][highway_x] == '1':
                            matrix[highway_y][highway_x] = 'a' + str(highway_num)
                            highway.append((highway_x, highway_y))
                        else:
                            return False
                    else:
                        return True
                    highway_x -= 1
            elif prob == 2:
                # move right
                direction = "top"
                for j in range(0, 20):
                    if highway_y >= 0 and highway_y != h and highway_x >= 0 and highway_x != w:
                        if matrix[highway_y][highway_x] == '2':
                            matrix[highway_y][highway_x] = 'b' + str(highway_num)
                            highway.append((highway_x, highway_y))
                        elif matrix[highway_y][highway_x] == '1':
                            matrix[highway_y][highway_x] = 'a' + str(highway_num)
                            highway.append((highway_x, highway_y))
                        else:
                            return False
                    else:
                        return True
                    highway_y -= 1
            else:
                # move left
                direction = "bottom"
                for j in range(0, 20):
                    if highway_y >= 0 and highway_y != h and highway_x >= 0 and highway_x != w:
                        if matrix[highway_y][highway_x] == '2':
                            matrix[highway_y][highway_x] = 'b' + str(highway_num)
                            highway.append((highway_x, highway_y))
                        elif matrix[highway_y][highway_x] == '1':
                            matrix[highway_y][highway_x] = 'a' + str(highway_num)
                            highway.append((highway_x, highway_y))
                        else:
                            return False
                    else:
                        return True
                    highway_y += 1
        else:
            prob = random.randint(1, 5)
            # move same direction
            if prob >= 3:
                for j in range(0, 20):
                    if highway_y >= 0 and highway_y != h and highway_x >= 0 and highway_x != w:
                        if matrix[highway_y][highway_x] == '2':
                            matrix[highway_y][highway_x] = 'b' + str(highway_num)
                            highway.append((highway_x, highway_y))
                        elif matrix[highway_y][highway_x] == '1':
                            matrix[highway_y][highway_x] = 'a' + str(highway_num)
                            highway.append((highway_x, highway_y))
                        else:
                            return False
                    else:
                        return True
                    highway_x += 1
            elif prob == 2:
                # move right
                direction = "bottom"
                for j in range(0, 20):
                    if highway_y >= 0 and highway_y != h and highway_x >= 0 and highway_x != w:
                        if matrix[highway_y][highway_x] == '2':
                            matrix[highway_y][highway_x] = 'b' + str(highway_num)
                            highway.append((highway_x, highway_y))
                        elif matrix[highway_y][highway_x] == '1':
                            matrix[highway_y][highway_x] = 'a' + str(highway_num)
                            highway.append((highway_x, highway_y))
                        else:
                            return False
                    else:
                        return True
                    highway_y += 1
            else:
                # move left
                direction = "top"
                for j in range(0, 20):
                    if highway_y >= 0 and highway_y != h and highway_x >= 0 and highway_x != w:
                        if matrix[highway_y][highway_x] == '2':
                            matrix[highway_y][highway_x] = 'b' + str(highway_num)
                            highway.append((highway_x, highway_y))
                        elif matrix[highway_y][highway_x] == '1':
                            matrix[highway_y][highway_x] = 'a' + str(highway_num)
                            highway.append((highway_x, highway_y))
                        else:
                            return False
                    else:
                        return True
                    highway_y -= 1
    return False


def add_highways(matrix, region_num, highway):
    # 1 = top, bottom = 2, left = 3, right  = 4
    x_rand, y_rand = generate_random_highway_point(region_num)
    direction = ""

    if region_num == 1:
        for k in range(0, 20):
            if matrix[y_rand + k][x_rand] == '2':
                matrix[y_rand + k][x_rand] = 'b' + str(region_num)
                highway.append((x_rand, y_rand + k))
            else:
                matrix[y_rand + k][x_rand] = 'a' + str(region_num)
                highway.append((x_rand, y_rand + k))
        direction = "bottom"
        y_rand += 20

    if region_num == 2:
        for k in range(0, 20):
            if matrix[y_rand - k][x_rand] == '2':
                matrix[y_rand - k][x_rand] = 'b' + str(region_num)
                highway.append((x_rand, y_rand - k))
            else:
                matrix[y_rand - k][x_rand] = 'a' + str(region_num)
                highway.append((x_rand, y_rand - k))
        direction = "top"
        y_rand -= 20

    if region_num == 3:
        for k in range(0, 20):
            if matrix[y_rand][x_rand + k] == '2':
                matrix[y_rand][x_rand + k] = 'b' + str(region_num)
                highway.append((x_rand + k, y_rand))
            else:
                matrix[y_rand][x_rand + k] = 'a' + str(region_num)
                highway.append((x_rand + k, y_rand))
        direction = "right"
        x_rand += 20

    if region_num == 4:
        for k in range(0, 20):
            if matrix[y_rand][x_rand - k] == '2':
                matrix[y_rand][x_rand - k] = 'b' + str(region_num)
                highway.append((x_rand - k, y_rand))
            else:
                matrix[y_rand][x_rand - k] = 'a' + str(region_num)
                highway.append((x_rand - k, y_rand))
        direction = "left"
        x_rand -= 20

    return add_more_highways(matrix, x_rand, y_rand, direction, highway, region_num)


"""
    This function takes the two lists and changes the main matrix.
"""

def add_hard_cells(matrix, x_s, y_s):
    for i in range(8):
        matrix[y_s[i]][x_s[i]] = '2'

        if x_s[i] - 15 < 0:
            x_m = 0
        else:
            x_m = x_s[i] - 15
        if x_s[i] + 15 > w:
            x_n = w
        else:
            x_n = x_s[i] + 15
        if y_s[i] - 15 < 0:
            y_m = 0
        else:
            y_m = y_s[i] - 15
        if y_s[i] + 15 > h:
            y_n = h
        else:
            y_n = y_s[i] + 15

        for p in range(y_m, y_n):
            for q in range(x_m, x_n):
                random_number = random.randint(0, 1)
                if random_number == 1:
                    matrix[p][q] = '2'


def add_start_node():
    start_node_region = random.randint(1, 4)
    start_node_x = 0
    start_node_y = 0

    # top left = 1, top-right = 2, bottom-left = 3, bottom-right = 4
    if start_node_region == 1:
        start_node_x = random.randint(0, 79)
        start_node_y = random.randint(0, 59)

    if start_node_region == 2:
        start_node_x = random.randint(80, 159)
        start_node_y = random.randint(0, 59)

    if start_node_region == 3:
        start_node_x = random.randint(0, 79)
        start_node_y = random.randint(60, 119)

    if start_node_region == 4:
        start_node_x = random.randint(80, 159)
        start_node_y = random.randint(60, 119)

    return start_node_x, start_node_y


def add_end_node():
    end_node_region = random.randint(1, 4)
    end_node_x = 0
    end_node_y = 0

    # top left = 1, top-right = 2, bottom-left = 3, bottom-right = 4
    if end_node_region == 1:
        end_node_x = random.randint(0, 79)
        end_node_y = random.randint(0, 59)

    if end_node_region == 2:
        end_node_x = random.randint(80, 159)
        end_node_y = random.randint(0, 59)

    if end_node_region == 3:
        end_node_x = random.randint(0, 79)
        end_node_y = random.randint(60, 119)

    if end_node_region == 4:
        end_node_x = random.randint(80, 159)
        end_node_y = random.randint(60, 119)

    return end_node_x, end_node_y

def lists_overlap(a, b):
    # shachar = list(set(a) & set(b))
    return len(list(set(a) & set(b))) != 0

def map_nodes():

    for it in range(5):
        Matrix = [['1' for x in range(160)] for y in range(120)]
        x, y = get_hard_cells_coordinates()
        add_hard_cells(Matrix, x, y)

        highway1 = []
        highway2 = []
        highway3 = []
        highway4 = []

        temp_matrix = deepcopy(Matrix)

        isGood = add_highways(Matrix, 1, highway1)
        while not isGood:
            Matrix = deepcopy(temp_matrix)
            highway1.clear()
            isGood = add_highways(Matrix, 1, highway1)

        temp_matrix = deepcopy(Matrix)
        isGood = add_highways(Matrix, 2, highway2)

        while not isGood or (lists_overlap(highway1, highway2)):
            Matrix = deepcopy(temp_matrix)
            highway2.clear()
            isGood = add_highways(Matrix, 2, highway2)

        temp_matrix = deepcopy(Matrix)
        isGood = add_highways(Matrix, 3, highway3)

        while not isGood or (lists_overlap(highway1, highway3) or lists_overlap(highway2, highway3)):
            Matrix = deepcopy(temp_matrix)
            highway3.clear()
            isGood = add_highways(Matrix, 3, highway3)

        temp_matrix = deepcopy(Matrix)
        isGood = add_highways(Matrix, 4, highway4)

        while not isGood or (lists_overlap(highway1, highway4) or lists_overlap(highway2, highway4) or lists_overlap(highway3, highway4)):
            Matrix = deepcopy(temp_matrix)
            highway4.clear()
            isGood = add_highways(Matrix, 4, highway4)

        x_blocked, y_blocked = get_blocked_cells_coordinates(Matrix)

        for e in range(3840):
            Matrix[y_blocked[e]][x_blocked[e]] = '0'

        for i in range(10):
            s_x, s_y = add_start_node()
            while Matrix[s_y][s_x] != '1':
                s_x, s_y = add_start_node()

            while True:
                e_x, e_y = add_end_node()
                if Matrix[e_y][e_x] != '1':
                    continue
                if (abs(e_y - s_y) + abs(e_x - s_x)) >= 100:
                    break

            Matrix[s_y][s_x] = 's'
            Matrix[e_y][e_x] = 'g'
            answer = print_matrix(Matrix)

            file_name = 'map' + str((it*10) + i) + '.txt'

            ff = open(path.join(MAP_DIRECTORY, file_name), 'w')
            ff.write(str(s_x) + ", " + str(s_y) + "\n")
            ff.write(str(e_x) + ", " + str(e_y) + "\n")

            for i in range(0, 8):
                ff.write("Hard to Traverse Center Point #" + str(i) + ": (" + str(x[i]) + ", " + str(y[i]) + ")\n")

            ff.write(answer)
            ff.close()
            Matrix[s_y][s_x] = '1'
            Matrix[e_y][e_x] = '1'


if __name__ == "__main__":
    map_nodes(sys.argv[:])
