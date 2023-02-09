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

	# Check whether the active piece is in the 'empty' state, and whether
	# a new one has to be created
	def activePieceIsEmpty(self):
		return self.activePiece.piece_type == -1
	
	# Check whether a given piece is in an 'illegal position',
	# more specifically whether it is outside the bounds of the
	# game board or intersects with a board tile
	def pieceInIllegalPos(self, piece: Piece):
		# To do this, the piece is first 'petrified' which means translating
		# the coordinates in the structure matrix into where they really are on the board
		# By doing this we make the coordinates of the board and the piece 'comparable'
		# which we need to know whether a piece's real coordinate is the same
		# as an active board tile. There is some serious optimisation potential here,
		# as we could also just iterate of the piece's structure matrix and add up the
		# coordinates with x and y position respectively, and then only checking for these
		# coordinates on the board.
		pieceInGrid = piece.petrify()
		# Now we iterate over all tiles of the petrified piece and if at some point there
		# is an active tile on both the board and the petrified piece, we know we have an intersection
		# The same goes for out of bound coordinates, of course.
		for y in range(len(pieceInGrid)):
			for x in range(len(pieceInGrid[y])):
				# We only need to do something during an iteration if the petrified piece
				# even has an active tile there 
				if pieceInGrid[y][x] == 1:
					# First, we check if we are out of bounds. If yes, we exit with result True.
					if not x in range(self.width) or not y in range(self.height):
						return True
					# Then we check whether we intersect with the board. If so, same thing.
					if self.board[y][x][0] == 1:
						return True
		# If we never find anything during our checks, the position must be valid
		# and we return with False (not illegal).
		return False
	
	# Make the active piece a part of the board. This will be called in update() when
	# the active piece hits the ground and can no longer move.
	def activePieceToBoard(self):
		# Again, we petrify. Reasoning behind this is derivable from the
		# pieceInIllegalPos() explanation.
		petrifiedStructure = self.activePiece.petrify()
		# We then iterate over the board, again with huge improvement potential.
		# See the pieceInIllegalPos() explanation for as to why that is.
		for y in range(self.height):
			for x in range(self.width):
				if petrifiedStructure[y][x] == 1:
					# If our soon-not-to-be active piece has a tile at the given position,
					# we activate that tile in the game board and set it's type to the active piece's
					self.board[y][x] = (1, self.activePiece.piece_type)
		# When we're done, we empty the active piece so the update function will create a new one.
		self.emptyActivePiece()

	# This is the update method. Here, the game's state is changed according to the rules of the game.
	def update(self):
		# We will need to move the active piece to its next, lower position (falling)
		# This, however, should only be done if the active piece is not empty 
		if not self.activePieceIsEmpty():
			# First, we will need to check whether the next position will even be a valid one.
			# To do this, we will first create a copy of the active piece.
			nextStagePiece = copy.deepcopy(self.activePiece)
			# We will then move it down by a tile, according to how the active piece will move
			nextStagePiece.pos[1] = nextStagePiece.pos[1] + 1
			# Then, we check whether the resulting piece is in an illegal position.
			if self.pieceInIllegalPos(nextStagePiece):
				# If so, this means we have "hit the ground", so we insert the active piece into
				# the game board
				self.activePieceToBoard()
			else:
				# If this is not the case however, we can safely move the active piece to the
				# new position. We simply do this by assigning our probing piece from before.
				self.activePiece = nextStagePiece
		# Now, we check whether the active piece is empty. This state can be reached either
		# when we hit the ground in the previous piece of code, or we just started/restarted the game.
		if self.activePieceIsEmpty():
			# We now take steps to create a new piece.
			# We will first choose a random piece type (the shape) that will be spawned.
			piece_type = random.randrange(0, len(self.pieces))
			# We then retrieve the dimensions of the piece to determine with what offset it will need to be spawned
			height = len(self.pieces[piece_type])
			width = len(self.pieces[piece_type][0])
			# Here, we determine the spawn offset. We want the piece to be centered horizontally.
			# Thus, our x offset will be half the width of the game board minus half of the piece width,
			# which we can also express as (width_game - width_piece) / 2
			start_x = math.floor((self.width - width) / 2)
			# We then initialise a new piece. Woohoo!
			self.activePiece = Piece((start_x, 0), self.pieces[piece_type], piece_type)
			# If the newly created piece is in an illegal position now, the game board is blocked from accepting
			# any new pieces. We have a game over.
			if (self.pieceInIllegalPos(self.activePiece)):
				# We implement this "Game Over" by just resetting.
				# You can do better, player. Try again.
				self.reset()

	# This is one of the controls needed to interact with the game.
	# We want to be able to turn the piece to hopefully achieve an advantageous game state.
	def turnActivePiece(self, turn):
		# If the amount to be turned is divisble by 4 without a remainder, we will just achieve
		# the same rotation anyways, so we don't need to do anything and can just exit.
		if turn % 4 == 0: return
		# We then do something similar as in the update method:
		# We create a copy of the active piece,
		# Apply the desired manipulation to it,
		# and check whether its position is now illegal.
		# If so, don't apply the manipulation, if not, go ahead.
		turnedPiece = copy.deepcopy(self.activePiece)
		turnedPiece.rotate(turn)
		if self.pieceInIllegalPos(turnedPiece): return
		self.activePiece = turnedPiece

	# This is one of the controls needed to interact with the game.
	# We want to be able to move the piece horizontally to hopefully achieve an advantageous game state.
	def moveActivePiece(self, direction):
		# We then do something similar as in the update method:
		# We create a copy of the active piece,
		# Apply the desired manipulation to it,
		# and check whether its position is now illegal.
		# If so, don't apply the manipulation, if not, go ahead.
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
