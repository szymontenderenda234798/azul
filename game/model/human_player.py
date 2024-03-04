from model.player import Player

class HumanPlayer(Player):
    def take_turn(self):
        print(f"{self.name}'s turn (Human):")
        # Implementation for a human player's turn