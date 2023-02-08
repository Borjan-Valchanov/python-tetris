import tetris

class GameUI:
	def __init__(self, game: tetris.Game, size=550) -> None:
		self.colours = [
			'#c79e2f',
			'#5db208',
			'#9d28a2',
			'#c45200',
			'#3457ff'
		]
		self.game = game
		self.size = size