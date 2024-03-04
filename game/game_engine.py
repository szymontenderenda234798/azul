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

    def next_player(self):
        self.current_player_index = (self.current_player_index + 1) % self.player_count

    def play_round(self):
        # Simplified version of round play
        while True:  # Loop until break condition met
            current_player = self.players[self.current_player_index]

            self.print_game_state()

            factory_index = self.select_factory()
            selected_factory = self.central_factory if factory_index == -1 else self.factories[factory_index]
            selected_color = self.select_color(selected_factory)
            pattern_line_index = self.select_pattern_line()

            # Process the selection
            if factory_index >= 0:
                selected_factory = self.factories[factory_index]
            else:
                selected_factory = self.central_factory
                if any(isinstance(tile, StartingPlayerTile) for tile in selected_factory.tiles):
                    print("Starting player marker taken!")
                    selected_factory.starting_player_marker_taken = True
                    for tile in selected_factory.tiles:
                        if isinstance(tile, StartingPlayerTile):
                            selected_factory.tiles.remove(tile)
                            break
                    current_player.place_starting_player_tile_on_floor_line()

            selected_tiles = selected_factory.remove_and_return_tiles_of_color(selected_color)
            remaining_tiles = selected_factory.get_and_clear_remaining_tiles()
            self.central_factory.add_tiles(remaining_tiles)

            # Attempt to place tiles on player's board (simplified)
            current_player.place_tile_in_pattern_line(selected_color, pattern_line_index, len(selected_tiles))

            # Move to the next player
            self.current_player_index = (self.current_player_index + 1) % self.player_count

            # Check for end of round condition (simplified)
            if all(not factory.tiles for factory in self.factories) and not self.central_factory.tiles:
                break  # End the round if all factories and central are empty


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

    def select_factory(self):
        # Determine if the central factory has tiles other than just the starting player tile
        central_has_valid_tiles = any(not isinstance(tile, StartingPlayerTile) for tile in self.central_factory.tiles)

        # List non-empty factories and include the central factory if it has valid tiles
        non_empty_factories = [(i, factory) for i, factory in enumerate(self.factories, start=1) if factory.tiles]
        non_empty_factory_indices = [str(i) for i, factory in non_empty_factories]

        central_factory_option = ""
        if central_has_valid_tiles:  # Only add central factory as an option if it has valid tiles
            central_factory_option = "0,"

        if not non_empty_factories and not central_has_valid_tiles:
            print("No valid tile selection options available. Please check the game state.")
            return None

        while True:
            try:
                selection_prompt = f"Choose a factory by number (Options: {central_factory_option} {', '.join(non_empty_factory_indices)}): "
                factory_index = input(selection_prompt).strip()
                if factory_index == "0" and central_has_valid_tiles:
                    return -1  # Convention to represent the central factory as a valid selection
                factory_index = int(factory_index) - 1
                if str(factory_index + 1) in non_empty_factory_indices:
                    return factory_index
                else:
                    print("Selected factory is empty, does not exist, or only contains the Starting Player Tile. Please choose from the available options.")
            except ValueError:
                print("Invalid input. Please enter a valid option.")

    def select_color(self, selected_factory):
        available_colors = {tile.color.name.upper() for tile in selected_factory.tiles if not isinstance(tile, StartingPlayerTile)}
        print(f"Available colors: {', '.join(sorted(available_colors))}")
        while True:
            color_input = input("Choose a color from the available options: ").upper()
            if color_input in available_colors:
                return TileColor[color_input]
            else:
                print("Invalid color. Please choose from the available options.")

    def select_pattern_line(self):
        while True:
            try:
                pattern_line_index = int(input("Choose a pattern line (1-5): ")) - 1
                if 0 <= pattern_line_index < 5:
                    return pattern_line_index
                else:
                    print("Please enter a number between 1 and 5.")
            except ValueError:
                print("Invalid input. Please enter a number.")