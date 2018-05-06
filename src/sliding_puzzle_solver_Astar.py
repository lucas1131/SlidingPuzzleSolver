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
import numpy as np
from queue import PriorityQueue
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

# Define functions
def PrintBoard(board):
	print(np.matrix(board))
	# for row in board:
	# 	print("\t" + str(row))

def SwapTiles(board, tile1, tile2):
	''' 
	Swaps the values of board[tile1.x, tile1.y] and board[tile2.x, tile2.y]

	Parameters:
		board: the board's matrix to swap values
		tile1: a tuple with the coordinates of the first value
		tile12: a tuple with the coordinates of the second value
	'''

	# Slow - using python list of lists
	# Swap values
	# tmp = board[tile1[0]][tile1[1]]
	# board[tile1[0]][tile1[1]] = board[tile2[0]][tile2[1]]
	# board[tile2[0]][tile2[1]] = tmp

	# Using numpy matrix
	tmp = board[tile1[0], tile1[1]]
	board[tile1[0], tile1[1]] = board[tile2[0], tile2[1]]
	board[tile2[0], tile2[1]] = tmp

	return board

def GenerateObjective(n):

	board = []
	count = 0
	
	for i in range(0, size):

		row = []
		for j in range(0, size):
			count += 1
			row.append(count)
		board.append(row)

	board[size-1][size-1] = 0

	return board

def Heuristic(board, heuristic_func, normal_func):
	"""
	Template function that apply the given heuristic for each tile and a 
	normalization for the total calculated cost.
	
	Parameters:
		board: puzzle's board
		heuristic_func: takes 2 tuples as parameters: current row and col, 
			target row and col
		normal_func: takes 1 parameter, the sum of heuristic_func over all 
			entries, and returns int. This is the final value of the heuristic 
			function
	"""

	size = board.shape[0]
	cost = 0

	for row in range(size):
		for col in range(size):
			
			val = board[row, col] - 1 # Subtract 1 just for simples arithmetics
			target = (int(val/size), val%size)

			# 0's position is last row, last col
			if val < 0: 
				target = (size-1, target[1])

			dist = heuristic_func((row, col), target)
			cost += dist

	return normal_func(cost)

# Possible heuristics: Hamming distance, Manhattan Distance, Euclidean Distance
def ManhattanDistance(board):
	''' 
	Calculates the Manhattan distance from the current board to the solved board state
	Parameters:
		board: puzzle's board
	'''
	return Heuristic(board,
                lambda pos, target: abs(pos[0] - target[0]) + abs(pos[1] - target[1]),
                lambda x : x)


def GetMoves(board, depth):

	"""Returns list of tuples with the board after the movement and its depth"""
	
	# Find 0 position
	size = board.shape[0]
	pos0 = (-1, -1)
	for row in range(size):
		for col in range(size):
			if board[row, col] == 0:
				pos0 = (row, col)


	if pos0[0] < 0 or pos0[1] < 0:
		raise Exception("0 space not found!")
	
	new_boards = []
	# Generate and apply possible moves
	if pos0[0] > 0:
		move = (pos0[0]-1, pos0[1]) # Up
		copy = board.copy()
		new_boards.append( (SwapTiles(copy, pos0, move), depth+1) )
		
	if pos0[0] < size-1:
		move = (pos0[0]+1, pos0[1]) # Down
		copy = board.copy()
		new_boards.append( (SwapTiles(copy, pos0, move), depth+1) )
		
	if pos0[1] > 0:
		move = (pos0[0], pos0[1]-1) # Left
		copy = board.copy()
		new_boards.append( (SwapTiles(copy, pos0, move), depth+1) )
		
	if pos0[1] < size-1:
		move = (pos0[0], pos0[1]+1) # Right
		copy = board.copy()
		new_boards.append( (SwapTiles(copy, pos0, move), depth+1) )
	
	return new_boards

def SolveAStar(board, heuristic=ManhattanDistance, verbosity=False, debug=False):
	'''
	Solves the puzzle using A* search algorithm with given heuristic

	Parameters:
		board: puzzle's board
		heuristic: heuristic function to use
		verbosity: if true, print each iteration of the algorithm
	'''

	if not isinstance(board, np.matrix):
		board = np.matrix(board)

	# Open set (to visit) - start with initial board
	current_hcost = heuristic(board)
	open_set = [ (board, 0, current_hcost) ]
	# Closed set (visited nodes)
	closed_set = []
	move_count = 0

	while len(open_set) > 0:
		
		# if debug:
		# 	print("Current open set:")
		# 	for i in range(len(open_set)):
		# 		print("\t" + str(open_set[i]))

		# Open set can be used as a stack to avoid recursion
		current_board, depth, move_hcost = open_set.pop(0)
		move_count += 1
		
		# if move_count > 1000:
		# 	return [], -1 # failure

		if np.array_equal(current_board, objective):
			if len(closed_set) > 0:
				return current_board, move_count
			else: # This case means the input board was already solved
				return [current_board], 0

		moves = GetMoves(current_board, depth)
		idx_open = -1
		idx_closed = -1
		
		# if move_count%100 == 0:
		if verbosity: 
			print("\n Iteration %s" % move_count)
			print(" Depth: %s" % depth)
			PrintBoard(current_board)
		if debug:
			input()

		for move, depth in moves:

			# Heuristic cost
			move_hcost = heuristic(move)

			if move in open_set:
				idx_open = open_set.index(move, depth, move_hcost)
			else:
				idx_open = -1
			
			if move in closed_set:
				idx_closed = closed_set.index(move, depth, move_hcost)
			else:
				idx_closed = -1

			# Heuristic + real cost (until now)
			estimated_cost = move_hcost + depth
			if debug and move_count%100 == 0:
				print("\n\t")
				PrintBoard(move)
				print("\tHeuristic cost: " + str(move_hcost))
				print("\tMove's real cost: " + str(depth))
				print("\tTotal estimated cost: " + str(estimated_cost))

			# If node has never been visited
			if idx_closed == -1 and idx_open == -1:
				# open_set.append( (move_hcost, (move, depth)) )
				open_set.append((move, depth, move_hcost))
		
			# If node is in open set, we can update its entry for future visit
			elif idx_open > -1:
				cp, cp_depth = open_set[idx_open]
				
				if depth < cp_depth:
					# Copy move's values over existing
					cp_depth = depth
		
			# Node is in closed set, we already visited
			elif idx_closed > -1:
				cp, cp_depth = closed_set[idx_closed]
				
				if depth < cp_depth:
					closed_set = [i for i in closed_set if i[0] == cp]
					# closed_set.remove( (cp, cp_depth) )
					# open_set.append( (move, depth, move_hcost) )

		# Add current node to closed (visited) set
		# closed_set.append( (current_board, depth, current_hcost) )
		closed_set.append((current_board, depth, current_hcost))

		# Sort open set by estimated cost to objective + real cost up to now
		# This is a priority queue (heap)
		open_set = sorted(open_set, key=lambda pair: pair[2] + pair[1])

	# If finished state not found, return failure
	return [], -1


# Create globals
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


# Main
# Used for checking if board has been solved
global objective
objective = np.matrix(GenerateObjective(size))

# Only show board if user asked
# if args.verbosity or args.verbosity2:
	# print("\nBoard:")
	# PrintBoard(board)
	# print("\nObjective:")
	# PrintBoard(objective)

# exit
start_time = time.time()

solved, steps = SolveAStar(board, ManhattanDistance, args.verbosity2, args.step)

if steps < 0:
	print("No solution found.")

else: 
	print("Solution found after %s steps." % steps)
	PrintBoard(solved)
	print("Execution time: %ss." % (time.time() - start_time))
