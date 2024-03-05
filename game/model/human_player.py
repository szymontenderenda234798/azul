from model.player import Player
from model.starting_player_tile import StartingPlayerTile
from enums.tile_color import TileColor

class HumanPlayer(Player):

    def make_decision(self):
        factory_index = self.select_factory()
        selected_factory = self.game_engine.central_factory if factory_index == -1 else self.game_engine.factories[factory_index]
        selected_color = self.select_color(selected_factory)
        pattern_line_index = self.select_pattern_line()

        return factory_index, selected_color, pattern_line_index

    def select_factory(self):
        # Determine if the central factory has tiles other than just the starting player tile
        central_has_valid_tiles = any(not isinstance(tile, StartingPlayerTile) for tile in self.game_engine.central_factory.tiles)

        # List non-empty factories and include the central factory if it has valid tiles
        non_empty_factories = [(i, factory) for i, factory in enumerate(self.game_engine.factories, start=1) if factory.tiles]
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