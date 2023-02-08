import math
import copy
import random

# This class describes the Tetris game from an abstract point of view
class Game:
	# The constructor. Saves parameters such as board dimensions in
	# fields for later use, defines piece shapes,
	# prepares for first run of update()
	def __init__(self, width=10, height=20) -> None:
		# Save the board dimensions.
		self.width = width
		self.height = height
		# Define the pieces that may spawn.
		# A 1 indicates a block and a 0 emptiness.
		self.pieces = [
			[
			[0,1,0],
			[1,1,1]
			],
			[
			[0,1],
			[1,1],
			[1,0]
			],
			[
			[1,0],
			[1,1],
			[0,1]
			],
			[
			[1,1],
			[1,1]
			],
			[
			[1],
			[1],
			[1],
			[1]
			]
		]
		# Call the reset function which puts the game in a usable, initial state. 
		self.reset()

	# Put the game in its intended initial state
	def reset(self):
		# This line may be omitted, just makes things clearer.
		# The game board is a list of lists (rows) of tuples,
		# where the first item indicates whether there is a block
		# at that position, and the second indicates the colour
		self.board = list[list[tuple[int, int]]]
		# Iterate over every possible coordinate on the board
		# and make sure it is accessible. This is needed
		# when the active piece becomes part of the board
		# or the validity of a position must be checked.
		for y in range(self.height):
			for x in range(self.width):
				self.board.append((0, -1))
		# Put the active piece (the one you're controlling) in a state
		# in which it is recognised as 'empty'
		self.emptyActivePiece()

	# Make the active piece appear 'empty', so a new one is created
	def emptyActivePiece(self):
		self.activePiece = Piece((0,0),[[0]],-1)

	def activePieceIsEmpty(self):
		return self.activePiece.piece_type == -1
	
	def pieceInIllegalPos(self, piece: Piece):
		pieceInGrid = piece.petrify()
		for y in range(len(pieceInGrid)):
			for x in range(len(pieceInGrid[y])):
				if pieceInGrid[y][x] == 1:
					if not x in range(self.width) or not y in range(self.height):
						return False
					if self.board[y][x] == 1:
						return False
		return True
	
	def activePieceToBoard(self):
		petrifiedStructure = self.activePiece.petrify()
		for y in range(self.height):
			for x in range(self.width):
				if petrifiedStructure[y][x] == 1:
					self.board[y][x] = (1, self.activePiece.piece_type)
		self.emptyActivePiece()

	def update(self):
		if not self.activePieceIsEmpty():
			nextStagePiece = copy.deepcopy(self.activePiece)
			nextStagePiece.pos[1] = nextStagePiece.pos[1] + 1
			if self.pieceInIllegalPos(nextStagePiece):
				self.activePieceToBoard()
		if self.activePieceIsEmpty():
			piece_type = random.randrange(0, len(self.pieces))
			height = len(self.pieces[piece_type])
			width = len(self.pieces[piece_type][0])
			start_x = math.floor((self.width - width) / 2)
			start_y = math.ceil(height / 2)
			if (self.pieceInIllegalPos(self.activePiece)):
				self.reset()

	
	def turnActivePiece(self, turn):
		if turn == 0: return
		turnedPiece = copy.deepcopy(self.activePiece)
		turnedPiece.rotate(turn)
		if self.pieceInIllegalPos(turnedPiece): return
		self.activePiece = turnedPiece
	
	def moveActivePiece(self, direction):
		movedPiece = copy.deepcopy(self.activePiece)
		movedPiece.pos = (movedPiece.pos[0] + direction - 1, movedPiece[1] + (direction % 2))
		if self.pieceInIllegalPos(movedPiece): return
		self.activePiece = movedPiece

# This class describes a piece in Tetris
class Piece:
	def __init__(self, pos: tuple[int,int], structure: list[list[int]], piece_type: int):
		self.pos = pos
		self.structure = structure
		self.piece_type = piece_type
	
	def petrify(self):
		petrifiedStructure: list[list[int]] = []
		width = len(self.structure[0])
		height = len(self.structure)
		petrifiedStructure = initialiseMNMatrix(width + self.pos.x, height + self.pos.y)
		for y in range(len(self.structure)):
			for x in range(len(self.structure[y])):
				blockCoord = (x,y)
				blockValue = self.structure[y][x]
				if blockValue == 1:
					petrifiedStructure[y+self.pos[1]][x+self.pos[0]] = 1
		return petrifiedStructure
	
	def rotate(self, turn):
		if turn == 0: return
		if turn > 0:
			for i in range(turn):
				self.structure = rotateMatrixCW(self.structure)
		else:
			for i in range(-turn):
				self.structure = rotateMatrixCCW(self.structure)
		pass

def initialiseMNMatrix(m, n):
	matrix = []
	for i in range(n):
		matrix.append([m])
	return matrix

def rotateMatrixCW(matrix: list[list[int]]):
	rotatedMatrix: list[list[int]]
	max_y = len(matrix[0]) - 1
	max_x = len(matrix) - 1
	rotatedMatrix = initialiseMNMatrix(max_x + 1, max_y + y)
	for y in range(max_y + 1):
		for x in range(max_x + 1):
			rotatedMatrix[x][y] = matrix[y][x]
	return rotatedMatrix

def rotateMatrixCCW(matrix: list[list[int]]):
	rotatedMatrix: list[list[int]]
	max_y = len(matrix[0]) - 1
	max_x = len(matrix) - 1
	rotatedMatrix = initialiseMNMatrix(max_x + 1, max_y + y)
	for y in range(max_y + 1):
		for x in range(max_x + 1):
			rotatedMatrix[max_y - x][y]
	return rotatedMatrix
