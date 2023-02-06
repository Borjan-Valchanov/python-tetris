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

		pass