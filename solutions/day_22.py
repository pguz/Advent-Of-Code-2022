# Day 22: Monkey Map

import pandas as pd
import re


def parse_file(fd):
    board_rows = []
    d = {
        ' ': None,
        '#': True,
        '.': False,
    }
    while line := fd.readline()[:-1]:
        board_rows.append([d[e] for e in line])
    commands = re.findall(r'(\d+|L|R)', fd.readline())
    return (pd.DataFrame(board_rows), commands)


def find_password(board, commands):
    b_height, b_width = board.shape
    dir = 0
    cur = 0, board.loc[0, :][board.loc[0, :] == False].index[0]

    for c in commands:
        if c.isdigit():
            n_mov = int(c)

            if dir == 0:
                line = board.loc[cur[0], :]
                i = cur[1]
                last_valid = cur[1]
                while n_mov:
                    i = (i + 1) % b_width
                    if line[i] == True:
                        i = last_valid
                        break
                    if line[i] == False:
                        n_mov -= 1
                        last_valid = i
                cur = (cur[0], i)

            if dir == 1:
                line = board.loc[:, cur[1]]
                i = cur[0]
                last_valid = cur[0]
                while n_mov:
                    i = (i + 1) % b_height
                    if line[i] == True:
                        i = last_valid
                        break
                    if line[i] == False:
                        n_mov -= 1
                        last_valid = i
                cur = (i, cur[1])

            if dir == 2:
                line = board.loc[cur[0], :]
                i = cur[1]
                last_valid = cur[1]
                while n_mov:
                    i = (i - 1) % b_width
                    if line[i] == True:
                        i = last_valid
                        break
                    if line[i] == False:
                        n_mov -= 1
                        last_valid = i
                cur = (cur[0], i)

            if dir == 3:
                line = board.loc[:, cur[1]]
                i = cur[0]
                last_valid = cur[0]
                while n_mov:
                    i = (i - 1) % b_height
                    if line[i] == True:
                        i = last_valid
                        break
                    if line[i] == False:
                        n_mov -= 1
                        last_valid = i
                cur = (i, cur[1])

        elif c == 'R':
            dir = (dir + 1) % 4
        elif c == 'L':
            dir = (dir - 1) % 4    

    return 1000 * (cur[0] + 1) + 4 *  (cur[1] + 1) + dir

def _move(board, b_width, b_height, command, dir, cur):
    if command.isdigit():
        n_mov = int(command)

        if dir == 0:
            line = board.loc[cur[0], :]
            i = cur[1]
            while n_mov:
                if i + 1 == b_width or line[i + 1] is None:
                    if cur[0] < 50:
                        p_dir = 2
                        p_cur = (149 - cur[0], 99)
                    elif cur[0] < 100:
                        p_dir = 3
                        p_cur = (49, 50 + cur[0])
                    elif cur[0] < 150:
                        p_dir = 2
                        p_cur = (149 - cur[0], 149)
                    elif cur[0] < 200:
                        p_dir = 3
                        p_cur = (149, cur[0] - 100)
                    
                    if board.loc[p_cur] == True:
                        return (dir, (cur[0], i), 0)

                    return (p_dir, p_cur, n_mov - 1)

                elif line[i + 1] == True: 
                    break
                elif line[i + 1] == False:
                    n_mov -= 1
                    i += 1

            cur = (cur[0], i)
            return dir, cur, 0

        if dir == 1:
            line = board.loc[:, cur[1]]
            i = cur[0]
            while n_mov:
                if i + 1 == b_height or line[i + 1] is None:
                    if cur[1] < 50:
                        n_dir = 1
                        n_cur = (0, 100 + cur[1])
                    elif cur[1] < 100:
                        n_dir = 2
                        n_cur = (100 + cur[1], 49)
                    elif cur[1] < 150:
                        n_dir = 2
                        n_cur = (cur[1] - 50, 99)

                    if board.loc[p_cur] == True:
                        return (dir, (i, cur[1]), 0)

                    return (n_dir, n_cur, n_mov - 1)

                elif line[i + 1] == True:
                    break
                elif line[i + 1] == False:
                    n_mov -= 1
                    i += 1

            cur = (i, cur[1])
            return dir, cur, 0

        if dir == 2:
            line = board.loc[cur[0], :]
            i = cur[1]
            while n_mov:
                if i == 0 or line[i - 1] is None:
                    if cur[0] < 50:
                        n_dir = 0
                        n_cur = (149 - cur[0], 0)
                    elif cur[0] < 100:
                        n_dir = 1
                        n_cur = (100, cur[0] - 50)
                    elif cur[0] < 150:
                        n_dir = 0
                        n_cur = (149 - cur[0], 50)
                    elif cur[0] < 200:
                        n_dir = 1
                        n_cur = (0, cur[0] - 100)

                    if board.loc[n_cur] == True:
                        return (dir, (cur[0], i), 0)

                    return (n_dir, n_cur, n_mov - 1)

                elif line[i - 1] == True:
                    break
                elif line[i - 1] == False:
                    n_mov -= 1
                    i -= 1

            cur = (cur[0], i)
            return dir, cur, 0

        if dir == 3:
            line = board.loc[:, cur[1]]
            i = cur[0]
            while n_mov:
                if i == 0 or line[i - 1] is None:
                    if cur[1] < 50:
                        n_dir = 0
                        n_cur = (50 + cur[1], 50)
                    elif cur[1] < 100:
                        n_dir = 0
                        n_cur = (cur[1] + 100, 0)
                    elif cur[1] < 150:
                        n_dir = 3
                        n_cur = (199, cur[1] - 100)

                    if board.loc[p_cur] == True:
                        return (dir, (i, cur[1]), 0)

                    return (n_dir, n_cur, n_mov - 1)

                elif line[i - 1] == True:
                    break
                elif line[i - 1] == False:
                    n_mov -= 1
                    i -= 1

            cur = (i, cur[1])
            return dir, cur, 0

    elif command == 'R':
        dir = (dir + 1) % 4
        return (dir, cur, 0)

    elif command == 'L':
        dir = (dir - 1) % 4
        return (dir, cur, 0)


def find_final_password(board, commands):
    b_height, b_width = board.shape
    dir = 0
    cur = 0, board.loc[0, :][board.loc[0, :] == False].index[0]

    for c in commands:
        while c:
            dir, cur, c = _move(board, b_width, b_height, str(c), dir, cur)

    return 1000 * (cur[0] + 1) + 4 *  (cur[1] + 1) + dir


solution_function_01 = find_password
solution_function_02 = find_final_password
