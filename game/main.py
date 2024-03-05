from game_engine import GameEngine
from model.human_player import HumanPlayer
from model.ai_players.random_player import RandomPlayer

if __name__ == "__main__":
    # game_engine = GameEngine([HumanPlayer("Player 1"), HumanPlayer("Player 2")])
    game_engine = GameEngine([RandomPlayer("Random Player 1"), RandomPlayer("Random Player 2"), RandomPlayer("Random Player 3"), RandomPlayer("Random Player 4")])
    game_engine.play_game()