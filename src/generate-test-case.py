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

''' Generate test case for n sliding puzzle solvers '''

import argparse
import random

# Prepare command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("n", help="Test case size.")
parser.add_argument("-o", "--output", help="Output file name. Defaults to 'test.out'")
args = parser.parse_args()

#               UP      DOWN    LEFT    RIGHT
movements = [ (-1, 0), (1, 0), (0, -1), (0, 1) ]

# Define functions
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


def Swap(board, pos1, pos2):
	# Swap values
	tmp = board[pos1[0]][pos1[1]]
	board[pos1[0]][pos1[1]] = board[pos2[0]][pos2[1]]
	board[pos2[0]][pos2[1]] = tmp


def ScrambleBoard(board):
	''' 0 is assumed to be at last column and last row'''

	size = len(board)
	iterations = size*size*size    # Arbitrary
	pos0 = (size-1, size-1)
	lastMove = pos0                # Dont allow coming back to same place

	if iterations < 100:
		iterations = 100

	while iterations > 0:
		iterations -= 1

		invalidMove = True

		# Keep trying until a valid movement is found
		while invalidMove:
			
			# Get one random movement
			move = random.sample(movements, 1)[0]
			res = (pos0[0] + move[0], pos0[1] + move[1])

			try:
				Swap(board, pos0, res)
				invalidMove = False
				lastMove = pos0        # Update last movement
				pos0 = res             # Update empty space position

			except:
				invalidMove = True

	return board
		


def PrintBoard(board):
	for row in board:
		print("\t" + str(row))



# Open output file
if args.output:
	file = open(args.output, "w")
else:
	file = open("test.out", "w")

size = int(args.n)
board = GenerateObjective(size)

# PrintBoard(board)
board = ScrambleBoard(board)
# print()
PrintBoard(board)


file.writelines(args.n.join("\n"))
for row in board:
	file.writelines(str(row).join("\n"))

file.close()