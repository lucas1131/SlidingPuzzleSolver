#!/usr/bin/python
# coding=utf8
# Encoding declared to support python2

# Gabriel Simmel Nascimento             9050232
# Giovanna Oliveira Guimarães           9293693
# José Augusto Noronha de Menezes Neto  9293049
# Julia Diniz Ferreira                  9364865
# Lucas Alexandre Soares                9293265
# Otávio Luis Aguiar                    9293518
# Rafael Augusto Monteiro               9293095

''' Python n² sliding puzzle solver using A*

    For board creation, the value 0 is considered to be the empty space
    the board will have size n^2

'''

import argparse
import time
import heapq

# Prepare program arguments
parser = argparse.ArgumentParser()

''' Arguments:
    FILENAME    name of the file to read the input from
    VERBOSITY   show some more info
    FILENAME    name of the file to read the input from
'''

parser.add_argument("-f", "--filename", help="File with input board")
parser.add_argument("-v", "--verbosity", 
    help="Verbosity level 1 (print initial board)",
    action="store_true")
parser.add_argument("-vv", "--verbosity2", 
    help="Verbosity level 2 (implies -v; print board after each movement)",
    action="store_true")

# For debugging
parser.add_argument("-s", "--step", 
    help="Run algorithm step by step",
    action="store_true")

args = parser.parse_args()


class SlidingPuzzle:
    
    # Used for checking if board has been solved
    objective = None
    _objective_created = False

    def __init__(self, board, pos0=-1, n=-1):

        if n == -1: n = len(board)

        # If board is a list of list, transform to a single list
        if isinstance(board[0], list):
            n2 = n*n
            _board = list(range(0, n2))
            j = 0
            for i in range(0, n2, n):
                _board[i:i+n] = board[j]
                j += 1
        
        else: _board = list(board)
            

        self._heuristic_cost = 0
        self._real_cost = 0
        self.size = n
        self.board = _board
        
        # Parent node in search path
        self._parent = None

        # Movement that generated this board configuration
        self._generator_move = ""

        # Quick access to 0 position
        if pos0 == -1: self._pos0 = self._find_zero()
        else: self._pos0 = pos0

        if not SlidingPuzzle._objective_created:
            SlidingPuzzle._objective_created = True
            SlidingPuzzle.objective = SlidingPuzzle(GenerateObjective(self.size))

    def __eq__(self, other):
        if self.__class__ != other.__class__: return False
        else: return self.board == other.board

    def __ne__(self, other):
        if self.__class__ != other.__class__: return False
        else: return not self.board == other.board

    def __lt__(self, other):
        if self.__class__ != other.__class__: return False
        else: 
            this_cost = self._real_cost + self._heuristic_cost
            that_cost = other._real_cost + other._heuristic_cost
            return this_cost < that_cost

    def __le__(self, other):
        if self.__class__ != other.__class__: return False
        else: 
            this_cost = self._real_cost + self._heuristic_cost 
            that_cost = other._real_cost + other._heuristic_cost
            return this_cost <= that_cost

    def __gt__(self, other):
        if self.__class__ != other.__class__: return False
        else: 
            this_cost = self._real_cost + self._heuristic_cost
            that_cost = other._real_cost + other._heuristic_cost
            return this_cost > that_cost

    def __ge__(self, other):
        if self.__class__ != other.__class__: return False
        else: 
            this_cost = self._real_cost + self._heuristic_cost 
            that_cost = other._real_cost + other._heuristic_cost
            return this_cost >= that_cost

    def __str__(self):
        res = ""
        i = 0
        for value in self.board:
            res += "%-2s " % value
            i += 1
            if i%self.size == 0:
                res += "\r\n"

        return res

    def __getitem__(self, index):
        x, y = index
        return self.board[x*self.size + y]

    def __tmp__str__(self): return str(self.board)

    def _find_zero(self):

        # Find 0 position
        pos0 = (-1, -1)
        for row in range(self.size):
            for col in range(self.size):
                if self[row, col] == 0:
                    pos0 = (row, col)

        if pos0[0] < 0: raise Exception("0 space not found!")
        else:
            self._pos0 = pos0
            return self._pos0

    def Clone(self): 
        copy = SlidingPuzzle(self.board, n=self.size, pos0=self._pos0)
        
        copy._heuristic_cost = self._heuristic_cost
        copy._real_cost = self._real_cost
        copy._parent = self._parent

        return copy

    def Swap(self, tile1, tile2, generator=""):
        ''' 
        Swaps the values of board[tile1.x, tile1.y] and board[tile2.x, tile2.y]

        Parameters:
            tile1: a tuple with the coordinates of the first value
            tile12: a tuple with the coordinates of the second value
        '''
        p1 = tile1[0]*self.size + tile1[1]
        p2 = tile2[0]*self.size + tile2[1]

        tmp = self.board[p1]
        self.board[p1] = self.board[p2]
        self.board[p2] = tmp

        # Increment cost
        self._real_cost += 1
        self._hash_up_to_date = False

        self._generator_move = generator

        if self[tile1[0], tile1[1]] == 0: self._pos0 = tile1
        elif self[tile2[0], tile2[1]] == 0: self._pos0 = tile2

    def GetMoves(self):

        """Returns list of tuples with the board after the movement and its depth"""
        
        new_boards = []
        # Generate and apply possible moves
        if self._pos0[0] > 0 and self._generator_move != "D":
        # if self._pos0[0] > 0:
            move = (self._pos0[0]-1, self._pos0[1]) # Up
            copy = self.Clone()
            copy.Swap(self._pos0, move, generator="U")
            copy._parent = self
            new_boards.append(copy)
            
        if self._pos0[0] < self.size-1 and self._generator_move != "U":
        # if self._pos0[0] < self.size-1:
            move = (self._pos0[0]+1, self._pos0[1]) # Down
            copy = self.Clone()
            copy.Swap(self._pos0, move, generator="D")
            copy._parent = self
            new_boards.append(copy)
            
        if self._pos0[1] > 0 and self._generator_move != "R":
        # if self._pos0[1] > 0:
            move = (self._pos0[0], self._pos0[1]-1) # Left
            copy = self.Clone()
            copy.Swap(self._pos0, move, generator="L")
            copy._parent = self
            new_boards.append(copy)
            
        if self._pos0[1] < self.size-1 and self._generator_move != "L":
        # if self._pos0[1] < self.size-1:
            move = (self._pos0[0], self._pos0[1]+1) # Right
            copy = self.Clone()
            copy.Swap(self._pos0, move, generator="R")
            copy._parent = self
            new_boards.append(copy)
        
        return new_boards

    def Solve(self, heuristic, verbosity=False, debug=False):
        '''
        Solves the puzzle using A* search algorithm with given heuristic

        Parameters:
            self: puzzle's self
            heuristic: heuristic function to use
            verbosity: if true, print each iteration of the algorithm
        '''

        # Open set (to visit) - start with initial self
        # open_set = PriorityQueue()
        # open_set.put(self)
        open_set = [self]
        move_count = 0

        # while not open_set.empty():
        while len(open_set) > 0:
            
            # Open set can be used as a stack to avoid recursion
            # current_board = open_set.get()
            current_board = heapq.heappop(open_set)

            # Puzzle is done!
            if current_board == SlidingPuzzle.objective:
                return current_board._get_path(), move_count

            moves = current_board.GetMoves()
            move_count += 1
            idx_open = -1
            idx_closed = -1
            
            if verbosity: 
                print("\n Iteration %s" % move_count)
                print(" Depth: %s" % current_board._real_cost)
                print(current_board)
            if debug: input()

            for move in moves:
                heuristic_cost = heuristic(move)
                move._heuristic_cost = heuristic_cost
                heapq.heappush(open_set, move)


        # If finished state not found, return failure
        return [], -1

    def _get_path(self):

        aux = self
        path = ""
        while aux:
            path += aux._generator_move
            aux = aux._parent

        return path
        # if self._parent == None:
        #     return path
        # else:
        #     path.append(self)
        #     return self._parent._get_path(path)

def GenerateObjective(n):

    board = []
    count = 0
    
    for i in range(0, n):

        row = []
        for j in range(0, n):
            count += 1
            row.append(count)
        board.append(row)

    board[n-1][n-1] = 0

    return board

# Possible heuristics: Hamming distance, Manhattan Distance, Euclidean Distance
def ManhattanDistance(puzzle):
    ''' 
    Calculates the Manhattan distance from the current puzzle to the solved puzzle state
    Parameters:
        puzzle: puzzle's puzzle
    '''
    cost = 0

    for row in range(puzzle.size):
        for col in range(puzzle.size):
            val = puzzle[row, col] - 1 # Subtract 1 just for simpler arithmetics
            target = (int(val/puzzle.size), val%puzzle.size)

            # 0's position is last row, last col
            if val < 0: 
                target = (puzzle.size-1, target[1])

            dist = abs(row - target[0]) + abs(col - target[1])
            cost += dist

    return cost


def main():

    board = []

    # Get input
    # If a filename was supplied, dont ask for input
    if args.filename:

        try:
            file = open(args.filename, "r")
        except:
            print("Error: file not found.")
            raise

        lines = file.readlines();

        try:
            size = int(lines[0]) # Board size

            # Get board values
            for i in range(1, len(lines)):
                line = lines[i]

                # Split line by spaces and create an array with all digit values
                board.append([int(s) for s in line.split() if s.isdigit()])

                # If any line length is different than supplied board size, error
                if len(board[i-1]) != size:
                    raise Exception("Non conforming board shape (is the board squared?)")

            # If the number of lines is different than supplied board size, error
            if len(board) != size:
                raise Exception("Non conforming board shape (is the board squared?)")

        except ValueError:
            print("Error: failed to parse file at line " + i)

    # No file supplied, ask for input from user
    else:

        size = int(input("Board size: "))

        for i in range(0, size):
            line = str(input("Enter board " + str(i) + " row: "))
        
            # Split line by spaces and create an array with all digit values
            board.append([int(s) for s in line.split() if s.isdigit()])

    # Only show board if user asked
    # if args.verbosity or args.verbosity2:
        # print("\nBoard:")
        # print(board)
        # print("\nObjective:")
        # print(objective)

    puzzle = SlidingPuzzle(board)

    start_time = time.time()

    # Here path is returned in reverse order because of recursion
    path, steps = puzzle.Solve(heuristic=ManhattanDistance, 
                                verbosity=args.verbosity2, 
                                debug=args.step)
    print("Time to solve: %ss." % (time.time() - start_time))

    if steps < 0:
        print("No solution found.")

    else: 
        print("Solution found after %s steps." % steps)
        print("Steps: " + path)

if __name__ == '__main__':
    main()