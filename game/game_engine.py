from model.factory import Factory
from model.tile_bag import TileBag
from model.central_factory import CentralFactory
from model.starting_player_tile import StartingPlayerTile
from model.box_lid import BoxLid
from enums.tile_color import TileColor
from neural_network_interface import NeuralNetworkInterface

class GameEngine:
    def __init__(self, players):
        self.players = players
        self.player_count = len(players)
        self.game_over = False
        self.box_lid = BoxLid()
        self.tile_bag = TileBag(self.box_lid)
        self.neural_network_interface = NeuralNetworkInterface()
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
            player.board.box_lid = self.box_lid

    def play_game(self):
        print("Starting the game...")

        self.round_number = 0
        # while not self.game_over:
        while self.round_number < 1:
            self.round_number += 1
            print(f"\n-------------------------------------\nRound {self.round_number}\n-------------------------------------")
            self.play_round()
            # self.log_points()
            # After each round, check if the game should end
            self.check_game_over()
        self.print_final_scores()

    # def log_points(self):
    #     with open('game/logs/example.txt', 'a') as file:
    #         file.write(f"Points after round: {self.round_number} \n")
    #         for player in self.players:
    #             file.write(f"{player.name}: {player.score} points\n")

    def next_player(self):
        self.current_player_index = (self.current_player_index + 1) % self.player_count

    def play_round(self):
        while True:
            current_player = self.players[self.current_player_index]
            print(self.neural_network_interface.game_state_to_network_input(self))
            print(len(self.neural_network_interface.game_state_to_network_input(self)))
            self.play_turn(current_player)

            # Move to the next player
            self.current_player_index = (self.current_player_index + 1) % self.player_count

            # Check for end of round condition
            if all(not factory.tiles for factory in self.factories) and not self.central_factory.tiles:
                self.end_round()
                break  # End the round

    def play_turn(self, player):
        print(f"\n-------------------------------------\n{player.name}'s turn\n-------------------------------------")

        self.print_game_state()
        factory_index, selected_color, pattern_line_index = player.make_decision()

        selected_factory = self.central_factory if factory_index == -1 else self.factories[factory_index]
        
        if any(isinstance(tile, StartingPlayerTile) for tile in selected_factory.tiles):
                print("Starting player marker taken!")
                selected_factory.starting_player_marker_taken = True
                for tile in selected_factory.tiles:
                    if isinstance(tile, StartingPlayerTile):
                        selected_factory.tiles.remove(tile)
                        break
                player.board.place_starting_player_tile_on_floor_line()

        # Applying the decisions
        selected_tiles = selected_factory.remove_and_return_tiles_of_color(selected_color)
        remaining_tiles = selected_factory.get_and_clear_remaining_tiles()
        self.central_factory.add_tiles(remaining_tiles)
        player.place_tile_in_pattern_line(selected_color, pattern_line_index, len(selected_tiles))
        print(f"{player.name} placed {len(selected_tiles)} {selected_color.name} tiles in pattern line {pattern_line_index + 1}.")

    def check_game_over(self):
        for player in self.players:
            if player.has_completed_row_on_wall():
                self.game_over = True
                break

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

        
    def end_round(self):
        """Handle the end of a round: Move tiles, score points, and check game over condition."""
        print(f"\n-------------------------------------\nEND OF ROUND\n-------------------------------------")

        for player in self.players:
            print(f"\n{player.name} board before moving, but after last move:")
            player.board.print_board()

        self.set_new_starting_player()
        
        print(f"\n-------------------------------------\nSCORING AND MOVING TO WALL\n-------------------------------------")
        for player in self.players:
            score = player.move_tiles_to_wall_and_score()  # Assuming this method returns the score for the round
            player.score += score  # Assuming each player has a 'score' attribute
            print(f"\n{player.name} scored {score} points this round.")
            print(f"{player.name} board after moving:")
            player.board.print_board()

        self.refresh_factories()
        self.check_game_over()

    def set_new_starting_player(self):
        for i, player in enumerate(self.players):
            if player.has_starting_player_tile():  # You need to implement this method in PlayerBoard
                # Set this player as the starting player for the next round
                self.current_player_index = i
                self.starting_player_index = i  # Keep track of the new starting player
                break  # Only one player can have the starting player tile, so break once found

    #TODO: Implement the following methods
    def refresh_factories(self):
        """Refill the factories with tiles from the tile bag for the new round."""
        # Check if the tile bag is empty and needs to be refilled with discarded tiles
        # This part depends on your TileBag implementation. 
        # For simplicity, assuming tile_bag automatically handles refills
        self.central_factory.clear()  # Clear the central factory for the new round
        self.central_factory.add_starting_player_tile()  # Add the starting player tile to the central factory
        for factory in self.factories:
            factory.add_tiles(self.tile_bag.draw_tiles(4))

    def print_final_scores(self):
        """Print the final scores of all players."""
        print(f"\n-------------------------------------\nFINAL SCORES\n-------------------------------------")
        for player in self.players:
            print(f"{player.name}: {player.score} points")
        
        # Determine the winner (could be multiple in case of a tie)
        highest_score = max(player.score for player in self.players)
        winners = [player.name for player in self.players if player.score == highest_score]
        if len(winners) > 1:
            print(f"Tie between: {', '.join(winners)}")
        else:
            print(f"Winner: {winners[0]}")

    # def count_tiles_in_game(self):
    #     """Count the number of tiles in the factories, central factory, tile bag, and players' boards."""
    #     factory_tile_count = sum(len(factory.tiles) for factory in self.factories)
    #     print(f"Factory tile count (excluding StartingPlayerTile): {factory_tile_count}")

    #     central_factory_tile_count = len([tile for tile in self.central_factory.tiles if not isinstance(tile, StartingPlayerTile)])
    #     print(f"Central factory tile count (excluding StartingPlayerTile): {central_factory_tile_count}")

    #     tile_bag_tile_count = len(self.tile_bag.tiles)
    #     print(f"Tile bag tile count: {tile_bag_tile_count}")

    #     box_lid_tile_count = len(self.box_lid.tiles)
    #     print(f"Box lid tile count: {box_lid_tile_count}")

    #     players_tile_count = sum(player.board.count_placed_tiles() for player in self.players)
    #     print(f"Players' boards tile count: {players_tile_count}")

    #     tile_count_sum = factory_tile_count + central_factory_tile_count + tile_bag_tile_count + players_tile_count + box_lid_tile_count
    #     print(f"Total tile count (excluding StartingPlayerTile): {tile_count_sum}")

    #     # Log the total tile count to a file
    #     with open('game/logs/example.txt', 'a') as file:
    #         file.write(f"{tile_count_sum}\n")

    #     return tile_count_sum