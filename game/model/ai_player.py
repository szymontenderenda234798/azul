from model.player import Player

class AIPlayer(Player):
    def take_turn(self):
        print(f"{self.name}'s turn (AI):")
        # Implementation for an AI player's turn