import argparse

''' Python n² sliding puzzle solver 

	For board creation, the value 0 is considered to be the empty space
	the board will have size n^2

'''

# Prepare program arguments
parser = argparse.ArgumentParser()

parser.add_argument("-f", "--filename", help="File with input board")
parser.add_argument("-v", "--verbosity", 
	help="Verbosity level 1 (print initial)",
	action="store_true")
parser.add_argument("-vv", "--verbosity2", 
	help="Verbosity level 2 (print board after each movement)",
	action="store_true")

args = parser.parse_args()

# Define functions
def PrintBoard(board):
	print("\nBoard:")
	for row in board:
		print("\t" + str(row))

# Possible heuristics: Hamming distance, Manhattan Distance
def ManhattanDistance(board):
	pass

def SolveAStar(board, heuristic, verbosity):
	pass


# Create globals
board = []
movements = {
	"up": (-1, 0), 
	"down": (1, 0), 
	"left": (0, -1), 
	"right": (0, 1)
}

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

	size = input("Board size: ")

	for i in range(0, 3):
		line = str(input("Enter board " + str(i) + " row: "))
	
		# Split line by spaces and create an array with all digit values
		board.append([int(s) for s in line.split() if s.isdigit()])

	# print("Board size: " + str(size))

	# print("\nBoard:")
	# for row in board:
	# 	print("\t" + str(row))

# Main

# Only show board if user asked
if args.verbosity or args.verbosity2:
	PrintBoard(board)

# board = SolveIDAStar(board, ManhattanDistance, args.verbosity2)
# PrintBoard()




