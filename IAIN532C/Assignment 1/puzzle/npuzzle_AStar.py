#!/usr/bin/env python2
from copy import deepcopy
import sys

class Puzzle:

    def __init__(self, initial, parent):
        self.board = initial
        self.parent = parent
        self.n = len(board)
        self.f = 0
        self.g = 0
        self.h = 0

    def manhattan(self):
        h = 0
        for i in range(self.n):
            for j in range(self.n):
                x = self.board[i][j] / self.n
                y = self.board[i][j] % self.n
                h += abs(x-i) + abs(y-j)
        return h

    def is_solved(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.board[i][j] != self.n*i + j:
                    return False
        return True
    
    def __eq__(self, other):
        return self.board == other.board

def get_empty_slot(board):
    n = len(board)
    for i in range(n):
        for j in range(n):
            if board[i][j] == (n**2 - 1):
                return i, j

def perform_all_moves(current):
    board = current.board
    x, y = get_empty_slot(board)
    all_moves = [
        (x-1, y),
        (x+1, y),
        (x, y-1),
        (x, y+1),
    ]
    moves = []
    n = len(board)
    for new_x, new_y in all_moves:
        if new_x >= 0 and new_x < n and new_y >= 0 and new_y < n:
            new_board = deepcopy(board)
            new_board[x][y] = new_board[new_x][new_y]
            new_board[new_x][new_y] = n**2 - 1
            successor = Puzzle(new_board, board)
            moves.append(successor)

    return moves

def least_f(open_list):
    idx, f = 0, open_list[0].f
    for i in range(len(open_list)):
        if open_list[i].f < f:
            f = open_list[i].f
            idx = i
    return open_list.pop(idx)

def A_Star(initial):
    # Use at your own risk :P
    open_list = [initial]
    closed_list = []

    while open_list:
        sys.stdout.write(str(len(open_list))+'\r')
        current = least_f(open_list)
        closed_list.append(current)

        if current.is_solved():
            print('Nodes: ' + str(len(open_list)))
            return current

        moves = perform_all_moves(current)
        for move in moves:
            if move not in closed_list:
                new_g = current.g + 1

                flag = False
                for i, item in enumerate(open_list):
                    if item == move and new_g < item.g:
                        flag = True
                        open_list[i].g = new_g
                        open_list[i].f = new_g + item.h
                        open_list[i].parent = current
                if not flag:
                    move.g = new_g
                    move.h = move.manhattan()
                    move.f = move.g + move.h
                    move.parent = current
                    open_list.append(move)
    return None

def pp(board):
    n = len(board)
    for i in range(n):
        for j in range(n):
            print("%02d" % (board[i][j])),
        print('')
    print('')

def print_solution(puzzle):
    if not puzzle:
        return 0
    moves = print_solution(puzzle.parent) + 1
    pp(puzzle.board)
    return moves
board = [[2,3,6],[0,1,8],[4,5,7]]
# board = [[5,2,8],[4,1,7],[0,3,6]]
# board = [[0,1,2],[3,4,5],[6,7,8]]
# board = [[1,2,0],[3,4,5],[6,7,8]]

# a star
board = [
    [4,0,1,2],
    [8,6,7,3],
    [12,15,9,11],
    [13,5,10,14]
]

board = [
        [1,4,15,3],
        [0,5,2,7],
        [8,9,6,10],
        [12,13,14,11]
    ]

# board = [[1, 2, 6, 3],[4, 9, 5, 7], [8, 13, 11, 15],[12, 14, 0, 10]]
initial = Puzzle(board, None)
result = A_Star(initial)
moves = print_solution(result)
print('Number of moves: %d' % moves)
