import random
import numpy as np
from copy import copy, deepcopy


w = 160
h = 120


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
        if matrix[n_rand][m_rand] == 'a' or matrix[n_rand][m_rand] == 'b':
            continue
        else:
            m.append(m_rand)
            n.append(n_rand)
            count += 1

    return m, n


def generate_random_highway_point(region_num):
    if region_num == 1:
        x_rand = random.randrange(0, 159)
        y_rand = 0
    if region_num == 2:
        x_rand = random.randrange(0, 159)
        y_rand = 119
    if region_num == 3:
        x_rand = 0
        y_rand = random.randrange(0, 119)
    if region_num == 4:
        x_rand = 159
        y_rand = random.randrange(0, 119)

    return x_rand, y_rand


def add_more_highways(matrix, highway_x, highway_y, direction):
    print(direction)
    while 0 <= highway_x < w and 0 <= highway_y < h:
        if direction == "top":
            prob = random.randint(1, 5)
            print(prob)
            # move same direction
            if prob >= 3:
                j = 0
                for j in range(0, 20):
                    if highway_y >= 0 and highway_y != h and highway_x >= 0 and highway_x != w:
                        if matrix[highway_y][highway_x] == '2':
                            matrix[highway_y][highway_x] = 'b'
                        elif matrix[highway_y][highway_x] == '1':
                            matrix[highway_y][highway_x] = 'a'
                        else:
                            return False
                    else:
                        return True
                    highway_y -= 1

            elif prob == 2:
                #move right
                j = 0
                direction = "right"
                for j in range(0, 20):
                    if highway_y >= 0 and highway_y != h and highway_x >= 0 and highway_x != w:
                        if matrix[highway_y][highway_x] == '2':
                            matrix[highway_y][highway_x] = 'b'
                        elif matrix[highway_y][highway_x] == '1':
                            matrix[highway_y][highway_x] = 'a'
                        else:
                            return False
                    else:
                        return True
                    highway_x += 1

            else:
                #move left
                j = 0
                direction = "left"
                for j in range(0, 20):
                    if highway_y >= 0 and highway_y != h and highway_x >= 0 and highway_x != w:
                        if matrix[highway_y][highway_x] == '2':
                            matrix[highway_y][highway_x] = 'b'
                        elif matrix[highway_y][highway_x] == '1':
                            matrix[highway_y][highway_x] = 'a'
                        else:
                            return False
                    else:
                        return True
                    highway_x -= 1

        elif direction == "bottom":
            prob = random.randint(1, 5)
            # move same direction

            if prob >= 3:
                j = 0
                for j in range(0, 20):
                    if highway_y >= 0 and highway_y != h and highway_x >= 0 and highway_x != w:
                        if matrix[highway_y][highway_x] == '2':
                            matrix[highway_y][highway_x] = 'b'
                        elif matrix[highway_y][highway_x] == '1':
                            matrix[highway_y][highway_x] = 'a'
                        else:
                            return False
                    else:
                        return True
                    highway_y += 1

            elif prob == 2:
                # move right
                direction = "left"
                j = 0
                for j in range(0, 20):
                    if highway_y >= 0 and highway_y != h and highway_x >= 0 and highway_x != w:
                        if matrix[highway_y][highway_x] == '2':
                            matrix[highway_y][highway_x] = 'b'
                        elif matrix[highway_y][highway_x] == '1':
                            matrix[highway_y][highway_x] = 'a'
                        else:
                            return False
                    else:
                        return True
                    highway_x -= 1

            else:
                # move left
                direction = "right"
                j = 0
                for j in range(0, 20):
                    if highway_y >= 0 and highway_y != h and highway_x >= 0 and highway_x != w:
                        if matrix[highway_y][highway_x] == '2':
                            matrix[highway_y][highway_x] = 'b'
                        elif matrix[highway_y][highway_x] == '1':
                            matrix[highway_y][highway_x] = 'a'
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
                            matrix[highway_y][highway_x] = 'b'
                        elif matrix[highway_y][highway_x] == '1':
                            matrix[highway_y][highway_x] = 'a'
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
                            matrix[highway_y][highway_x] = 'b'
                        elif matrix[highway_y][highway_x] == '1':
                            matrix[highway_y][highway_x] = 'a'
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
                            matrix[highway_y][highway_x] = 'b'
                        elif matrix[highway_y][highway_x] == '1':
                            matrix[highway_y][highway_x] = 'a'
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
                            matrix[highway_y][highway_x] = 'b'
                        elif matrix[highway_y][highway_x] == '1':
                            matrix[highway_y][highway_x] = 'a'
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
                            matrix[highway_y][highway_x] = 'b'
                        elif matrix[highway_y][highway_x] == '1':
                            matrix[highway_y][highway_x] = 'a'
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
                            matrix[highway_y][highway_x] = 'b'
                        elif matrix[highway_y][highway_x] == '1':
                            matrix[highway_y][highway_x] = 'a'
                        else:
                            return False
                    else:
                        return True
                    highway_y -= 1

    return True


def add_highways(matrix, region_num):
    # 1 = top, bottom = 2, left = 3, right  = 4
    x_rand, y_rand = generate_random_highway_point(region_num)
    direction = ""

    if region_num == 1:
        for k in range(0, 20):
            if matrix[y_rand + k][x_rand] == '2':
                matrix[y_rand + k][x_rand] = 'b'
            else:
                matrix[y_rand + k][x_rand] = 'a'
        direction = "bottom"
        y_rand += 20

    if region_num == 2:
        for k in range(0, 20):
            if matrix[y_rand - k][x_rand] == '2':
                matrix[y_rand - k][x_rand] = 'b'
            else:
                matrix[y_rand - k][x_rand] = 'a'
        direction = "top"
        y_rand -= 20

    if region_num == 3:
        for k in range(0, 20):
            if matrix[y_rand][x_rand + k] == '2':
                matrix[y_rand][x_rand + k] = 'b'
            else:
                matrix[y_rand][x_rand + k] = 'a'
        direction = "right"
        x_rand += 20

    if region_num == 4:
        for k in range(0, 20):
            if matrix[y_rand][x_rand - k] == '2':
                matrix[y_rand][x_rand - k] = 'b'
            else:
                matrix[y_rand][x_rand - k] = 'a'
        direction = "left"
        x_rand -= 20

    return add_more_highways(matrix, x_rand, y_rand, direction)


"""
    This function takes the two lists and changes the main matrix.
"""

def add_hard_cells(matrix, x_s, y_s):
    for i in range(8):
        Matrix[y_s[i]][x_s[i]] = '2'

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
                    Matrix[p][q] = '2'


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

Matrix = [['1' for x in range(160)] for y in range(120)]

x, y = get_hard_cells_coordinates()
add_hard_cells(Matrix, x, y)

temp_matrix = deepcopy(Matrix)
isGood = add_highways(Matrix, 1)
while not isGood:
    Matrix = deepcopy(temp_matrix)
    isGood = add_highways(Matrix, 1)

temp_matrix = deepcopy(Matrix)
isGood = add_highways(Matrix, 2)
while not isGood:
    Matrix = deepcopy(temp_matrix)
    isGood = add_highways(Matrix, 2)

temp_matrix = deepcopy(Matrix)
isGood = add_highways(Matrix, 3)
while not isGood:
    Matrix = deepcopy(temp_matrix)
    isGood = add_highways(Matrix, 3)

temp_matrix = deepcopy(Matrix)
isGood = add_highways(Matrix, 4)
while not isGood:
    Matrix = deepcopy(temp_matrix)
    isGood = add_highways(Matrix, 4)

x_blocked, y_blocked = get_blocked_cells_coordinates(Matrix)

for e in range(3840):
    Matrix[y_blocked[e]][x_blocked[e]] = '0'

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
ff = open('map.txt', 'w')
ff.write(str(s_x) + ", " + str(s_y) + "\n")
ff.write(str(e_x) + ", " + str(e_y) + "\n")

for i in range(0, 8):
    ff.write("Hard to Traverse Center Point #" + str(i) + ": (" + str(x[i]) + ", " + str(y[i]) + ")\n")

ff.write(answer)
ff.close()