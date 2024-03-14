from game_engine import GameEngine
from model.human_player import HumanPlayer
from model.ai_players.random_player import RandomPlayer
from model.tile import Tile
from neural_network_interface import NeuralNetworkInterface
from enums.tile_color import TileColor
from model.starting_player_tile import StartingPlayerTile
from neat_package.neat import run_neat, run

import sys
import os

if __name__ == "__main__":
    # game_engine = GameEngine([HumanPlayer("Player 1"), HumanPlayer("Player 2")])
    # console_to_file = False
    # game_engine = GameEngine([RandomPlayer("Random Player 1"), RandomPlayer("Random Player 2"), RandomPlayer("Random Player 3")])

    # if console_to_file:
    #     file = open("console_output.txt", "w")
    #     sys.stdout = file
    #     game_engine.play_game()
    #     sys.stdout = sys.__stdout__
    #     file.close()
    # else:
    #     game_engine.play_game()
    run('C:\\Users\\tende\\OneDrive\\Desktop\\inzynierka\\azul\\game\\neat_package\\neat_config.txt')
