import random
from model.starting_player_tile import StartingPlayerTile
from model.player import Player

class RandomPlayer(Player):
    def make_decision(self):
        factory_index = self.select_factory()
        selected_factory = self.game_engine.central_factory if factory_index == -1 else self.game_engine.factories[factory_index]
        selected_color = self.select_color(selected_factory)
        pattern_line_index = self.select_pattern_line()

        return factory_index, selected_color, pattern_line_index

    def select_factory(self):
        # Filter out empty factories and the central factory if it only has the starting player tile
        valid_factories = [i for i, factory in enumerate(self.game_engine.factories, start=1) if factory.tiles]
        if any(not isinstance(tile, StartingPlayerTile) for tile in self.game_engine.central_factory.tiles):
            valid_factories.append(0)  # Adding '0' to represent the central factory

        if not valid_factories:
            print("No valid factories to select from.")
            return None

        # Randomly choose a factory from valid options
        return random.choice(valid_factories) - 1  # Adjust by -1 to align with list indexing

    def select_color(self, selected_factory):
        # Exclude the StartingPlayerTile from selectable colors
        available_colors = {tile.color for tile in selected_factory.tiles if not isinstance(tile, StartingPlayerTile)}
        
        if not available_colors:
            print("No valid colors to select from in the chosen factory.")
            return None

        # Randomly choose a color from available options
        return random.choice(list(available_colors))

    def select_pattern_line(self):
        # Randomly choose a pattern line index (0-4 for lines 1-5)
        return random.randint(0, 4)