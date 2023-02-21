# Tetris (Python)
> Note: This is WIP and not a ready-to-play game.

This is a hobbyist side-project of mine that aims to be a proof-of-concept implementation of the well known 90's game Tetris.

## Project State
Currently, this project is still undergoing heavy development and is not yet ready for use. There are implementations of the basic concepts, though they are not yet fully documented, optimised and interactable with.

## Structuring
This project contains two modules called `tetris` and `tetrisui`.

`tetris` is for the classes and functions necessary for an abstract represantation of the Game, while `tetrisui` contains the classes and functions for user-comprehensible interaction with the game, i. e. displaying the game state and taking input.

`tetrisui.GameUI` utilises the `turtle` module for graphics and input.

There is also a file called `main.py` that is intended to be used later on as a way to easily start the game without the need for the user to interact directly with the modules.

## Implementation specifics
> This only describes the module `tetris`, i. e. the abstract implementation of Tetris and does **NOT** include any kind of input handling or user interface.

This implementation understands Tetris game states as a combination of two entities: a board (`tetris.Game.board`), and a so-called 'active piece' (`tetris.Game.activePiece`).

> The active piece is the piece that is currently falling and that the player can control.
>
> The board is a two-dimensional array of 'tiles' of size m*n, where m is the width of the play area (10 by default) and n is it's height (20 by default)

The aforementioned 'tiles' are not a dedicated class. We will understand a tile as a tuple of an integer describing whether the tile is 'active' or not, which just means whether there is a block of a piece that previously fell there or if it is empty.

**TODO:** Finish README