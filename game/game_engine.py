from model.factory import Factory
from model.tile_bag import TileBag
from model.central_factory import CentralFactory
from model.starting_player_tile import StartingPlayerTile
from model.box_lid import BoxLid
from enums.tile_color import TileColor

class GameEngine:
    def __init__(self, players):
        self.players = players
        self.player_count = len(players)
        self.game_over = False
        self.box_lid = BoxLid()
        self.tile_bag = TileBag(self.box_lid)
        self.factories = []
        self.current_player_index = 0
        self.setup_game()

    def setup_game(self):
        # Initialize tiles, distribute them to factories, etc.

        # Determine the number of factory displays based on player count
        factory_display_count = {2: 5, 3: 7, 4: 9}.get(self.player_count, 0)

        # Initialize factories with Factory instances
        self.factories = [Factory() for _ in range(factory_display_count)]

        # Fill each factory with tiles
        for factory in self.factories:
            factory.add_tiles(self.tile_bag.draw_tiles(4))

        self.central_factory = CentralFactory()

        for player in self.players:
            player.board.box_lid = self.box_lid

        #Assign game engine to players
        for player in self.players:
            player.game_engine = self

    def next_player(self):
        self.current_player_index = (self.current_player_index + 1) % self.player_count

    def play_round(self):
        while True:
            current_player = self.players[self.current_player_index]

            current_player.take_turn()  # Delegating the turn-taking actions

            # Move to the next player
            self.current_player_index = (self.current_player_index + 1) % self.player_count

            # Check for end of round condition
            if all(not factory.tiles for factory in self.factories) and not self.central_factory.tiles:
                break  # End the round


    def check_game_over(self):
        # Check if the game has met its end conditions
        pass

    def print_game_state(self):
        print("\nCurrent Game State:\n")

        # Show available factories
        for i, factory in enumerate(self.factories, start=1):
            print(f"Factory {i}: {[tile.name for tile in factory.tiles]}")
        # Show the central factory
        print(f"Central Factory: {[tile.name for tile in self.central_factory.tiles]}\n")

        # Show players' boards
        for player in self.players:
            player.print_board()
            print("")  # Extra newline for spacing

        print(f"Player {self.current_player_index + 1}'s turn")


        
    def end_round(self):
        """Handle the end of a round: Move tiles, score points, and check game over condition."""
        for i, player in enumerate(self.players):
            if player.has_starting_player_tile():  # You need to implement this method in PlayerBoard
                # Assuming the CentralFactory has a method to add the starting player tile
                self.central_factory.add_starting_player_tile()

                # Set this player as the starting player for the next round
                self.current_player_index = i
                self.starting_player_index = i  # Keep track of the new starting player
                break  # Only one player can have the starting player tile, so break once found


        for player in self.players:
            score = player.move_tiles_to_wall_and_score()  # Assuming this method returns the score for the round
            player.score += score  # Assuming each player has a 'score' attribute
            print(f"{player.name} scored {score} points this round.")

        self.refresh_factories()
        self.check_game_over()

    #TODO: Implement the following methods
    def refresh_factories(self):
        """Refill the factories with tiles from the tile bag for the new round."""
        # Check if the tile bag is empty and needs to be refilled with discarded tiles
        # This part depends on your TileBag implementation. 
        # For simplicity, assuming tile_bag automatically handles refills
        self.central_factory.clear()  # Clear the central factory for the new round
        for factory in self.factories:
            factory.add_tiles(self.tile_bag.draw_tiles(4))