from game_engine import GameEngine
from model.human_player import HumanPlayer

if __name__ == "__main__":
    game_engine = GameEngine([HumanPlayer("Player 1"), HumanPlayer("Player 2")])
    game_engine.play_round()