from game_engine import GameEngine
from model.human_player import HumanPlayer
from model.ai_players.random_player import RandomPlayer
from model.tile import Tile
from neural_network_interface import NeuralNetworkInterface
from enums.tile_color import TileColor
from model.starting_player_tile import StartingPlayerTile
from neat_package.neat import run_with_logging
from logs.dual_logger import DualLogger


if __name__ == "__main__":             
    run_with_logging('config_one_round_one_board.txt')
    
