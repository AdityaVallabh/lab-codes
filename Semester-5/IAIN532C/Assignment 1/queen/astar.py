from pprint import pprint as pp
from copy import deepcopy
import sys

def is_safe(board, x, y, n):
    for i in range(n):
        if board[i][y]:
            return False

    left_up    = zip(range(x,-1,-1), range(y,-1,-1))
    right_up   = zip(range(x,-1,-1), range(y,n,1))
    left_down  = zip(range(x, n,1), range(y,-1,-1))
    right_down = zip(range(x, n,1), range(y, n, 1))

    for i,j in list(left_up) + list(right_up) + list(right_down) + list(left_down):
        if board[i][j]:
            return False

    return True

def get_least(nodes):
    idx = -1
    mini = None
    for i in range(len(nodes)):
        if mini == None or nodes[i][0] < mini:
            mini = nodes[i][0]
            idx = i
            
    return nodes.pop(idx)

def calc_h(board):
    count = 0
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 0 and is_safe(board, i, j, len(board)):
                count += 1
    return count

def AStar(board, n):
    queue = [(0,0,board)]

    while queue:
        f, i, board = get_least(queue)
        sys.stdout.write(str(len(queue)) + '\r')
        if i == n:
            pp(board)
            break
        for j in range(n):
            new_board = deepcopy(board)
            if is_safe(new_board, i, j, n):
                new_board[i][j] = 1
                queue.append((n-i+calc_h(board), i+1, new_board))

n = int(input("Enter board size: "))
board = [[0 for _ in range(n)] for _ in range(n)]
AStar(board, n)


