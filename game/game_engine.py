from model.factory import Factory
from model.tile_bag import TileBag
from model.central_factory import CentralFactory
from model.starting_player_tile import StartingPlayerTile
from enums.tile_color import TileColor

class GameEngine:
    def __init__(self, players):
        self.players = players
        self.player_count = len(players)
        self.game_over = False
        self.tile_bag = TileBag()
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

    def next_player(self):
        self.current_player_index = (self.current_player_index + 1) % self.player_count

    def play_round(self):
        # Simplified version of round play
        while True:  # Loop until break condition met
            current_player = self.players[self.current_player_index]
            print(f"Player {self.current_player_index + 1}'s turn")

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

    def select_factory(self):
        while True:
            try:
                factory_index = int(input(f"Choose a factory (1-{len(self.factories)}) or 0 for Central Factory: ")) - 1
                if -1 <= factory_index < len(self.factories):
                    return factory_index
                else:
                    print(f"Please enter a number between 0 and {len(self.factories)}.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def select_color(self, selected_factory):
        available_colors = {tile.color.name for tile in selected_factory.tiles}
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