import math
import random

# This class describes the Tetris game from an abstract point of view
class Game:
	def __init__(self, width=10, height=20) -> None:
		self.board = list[list[width]]
		self.width = width
		self.height = height
		self.pieces = [
			[
			[0,1,0],
			[1,1,1],
			[0,0,0]
			],
			[
			[0,1,0],
			[1,1,0],
			[1,0,0]
			],
			[
			[1,0,0],
			[1,1,0],
			[0,1,0]
			],
			[
			[1,1],
			[1,1]
			],
			[
			[0,1,0,0],
			[0,1,0,0],
			[0,1,0,0],
			[0,1,0,0]
			]
		]
		# I already defined the colours because I wanted to, but this
		# will have to go in the tetris UI package's GameUI class
		"""
		self.colours = [
			'#c79e2f',
			'#5db208',
			'#9d28a2',
			'#c45200',
			'#3457ff'
		]
		"""
		self.emptyActivePiece()

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

	def update(self):
		if (self.activePieceIsEmpty()):
			piece_type = random.randrange(0, len(self.pieces))
			dimension = len(self.pieces[piece_type])
			start_x = math.floor((self.width - dimension) / 2)
			start_y = math.ceil(dimension / 2)
			if (self.pieceInIllegalPos(self.activePiece)):
				pass

# This class describes a piece in Tetris
class Piece:
	def __init__(self, pos: tuple[int,int], structure: list[list[int]], piece_type: int):
		self.pos = pos
		self.structure = structure
		self.piece_type = piece_type
	
	def petrify(self):
		petrifiedStructure: list[list[int]] = []
		for y in range(len(self.structure)):
			for x in range(len(self.structure[y])):
				blockCoord = (x,y)
				blockValue = self.structure[y][x]
				if blockValue == 1:
					petrifiedStructure[y+self.pos[1]][x+self.pos[0]] = 1
		return petrifiedStructure
