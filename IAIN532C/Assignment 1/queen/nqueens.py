from pprint import pprint as pp
from copy import deepcopy

try:
    input = raw_input
except:
    pass

def is_safe(board, x, y, n):
    for i in range(n):
        if board[i][y]:
            return False

    left_diag = zip(range(x,-1,-1), range(y,-1,-1))
    right_diag = zip(range(x,-1,-1), range(y,n,1))

    for i,j in list(left_diag) + list(right_diag):
        if board[i][j]:
            return False

    return True

def DFS(board, i, n):
    if i == n:
        pp(board)
        return True
    for j in range(n):
        if is_safe(board, i, j, n):
            board[i][j] = 1
            if DFS(board, i+1, n):
                return True
            board[i][j] = 0
    return False

def BFS(board, n):
    queue = [(board,0)]

    while queue:
        board, i = queue.pop(0)
        if i == n:
            pp(board)
            break
        for j in range(n):
            new_board = deepcopy(board)
            if is_safe(new_board, i, j, n):
                new_board[i][j] = 1
                queue.append((new_board,i+1))

algo = input("Enter algorithm type: ")
n = int(input("Enter board size: "))
board = [[0 for _ in range(n)] for _ in range(n)]

if algo == 'dfs':
    DFS(board, 0, n)
elif algo == 'bfs':
    BFS(board, n)
else:
    print('Invalid')
