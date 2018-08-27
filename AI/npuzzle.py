from copy import deepcopy

def get_empty_slot(current):
    n = len(current)
    for i in range(n):
        for j in range(n):
            if current[i][j] == 0:
                return i, j

def perform_moves(current):
    n = len(current)
    x, y = get_empty_slot(current)
    all_moves = [
        (x-1, y),
        (x+1, y),
        (x, y-1),
        (x, y+1),
    ]
    moves = []

    for i, j in all_moves:
        if i >= 0 and j >= 0 and i < n and j < n:
            new_b = deepcopy(current)
            new_b[x][y], new_b[i][j] = new_b[i][j], new_b[x][y]
            moves.append(new_b)
    return moves

def pp(board):
    n = len(board)
    for i in range(n):
        for j in range(n):
            print("%02d" % (board[i][j])),
        print('')
    print('')

def print_solution(parent, p):
    path = []
    while p:
        path.append(p)
        p = parent[str(p)]
    while path:
        pp(path.pop())

def BFS(start, end):
    queue = [start]
    parent = {str(start): None}
    visited = []

    while queue:
        current = queue.pop(0)
        # print(current)
        if current == end:
            print_solution(parent, end)
            break
        if current in visited:
            continue
            
        moves = perform_moves(current)
        for move in moves:
            if move not in visited:
                queue.append(move)
                # visited.append(move)
                parent[str(move)] = current
        visited.append(current)
def main():
    start = [[1, 2, 6, 3],[4, 9, 5, 7], [8, 13, 11, 15],[12, 14, 0, 10]]
    # start = [
    #     [1, 2, 3],
    #     [4, 5, 6],
    #     [7, 0, 8]
    # ]
    n = len(start)
    end = [[(i*n+j+1)%(n*n) for j in range(n)] for i in range(n)]
    BFS(start, end)

if __name__ == '__main__':
    main()
