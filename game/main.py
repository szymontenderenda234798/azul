from game_engine import GameEngine
from model.human_player import HumanPlayer
from model.ai_players.random_player import RandomPlayer
from model.tile import Tile
from neural_network_interface import NeuralNetworkInterface
from enums.tile_color import TileColor
from model.starting_player_tile import StartingPlayerTile

import sys

if __name__ == "__main__":
    # game_engine = GameEngine([HumanPlayer("Player 1"), HumanPlayer("Player 2")])
    file = open("console_output.txt", "w")
    sys.stdout = file
    game_engine = GameEngine([RandomPlayer("Random Player 1"), RandomPlayer("Random Player 2"), RandomPlayer("Random Player 3"), RandomPlayer("Random Player 4")])
    game_engine.play_game()
    sys.stdout = sys.__stdout__
    file.close()