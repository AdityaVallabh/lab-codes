#!/usr/bin/env python2.7
from copy import deepcopy
import sys

def get_empty_slot(current):
    n = len(current)
    for i in range(n):
        for j in range(n):
            if current[i][j] == n*n - 1:#0:
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
    l = len(path)
    while path:
        pp(path.pop())
    return l

def BFS(start, end):
    queue = [start]
    parent = {str(start): None}
    visited = [start]

    while queue:
        current = queue.pop(0)
        if current == end:
            l = print_solution(parent, end)
            print('Moves: ' + str(l))
            print('Nodes: ' + str(len(visited)))
            break
        # if current in visited:
        #     continue
        
        # print(current)
        moves = perform_moves(current)
        for move in moves:
            if move not in visited:
                queue.append(move)
                visited.append(move)
                parent[str(move)] = current
        # visited.append(current)

def DFS(current, end, parent={}, visited=[]):
    if current == end:
        print_solution(parent, end)
        return True
    moves = perform_moves(current)
    visited.append(current)
    for move in moves:
        if move not in visited:
            parent[str(move)] = current
            if DFS(move, end, parent, visited):
                return True
    visited.pop()
    return False

def main():
    sys.setrecursionlimit(100000)
    start = [[1, 2, 6, 3],[4, 9, 5, 7], [8, 13, 11, 15],[12, 14, 0, 10]]
    
    start = [
        [1,4,15,3],
        [0,5,2,7],
        [8,9,6,10],
        [12,13,14,11]
    ]
    n = len(start)
    end = [[(i*n+j)%(n*n) for j in range(n)] for i in range(n)]
    print('BFS')
    BFS(start, end)
    # print('DFS')
    # DFS(start, end, parent={str(start): None})

if __name__ == '__main__':
    main()
