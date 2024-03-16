import random
from model.starting_player_tile import StartingPlayerTile
from model.player import Player
from neural_network_interface import NeuralNetworkInterface
from enums.tile_color import TileColor
import numpy as np

class NeuralNetworkPlayer(Player):

    def __init__(self, name, neural_network):
        super().__init__(name)
        self.neural_network = neural_network
        self.nn_interface = NeuralNetworkInterface()

    def make_decision(self):
        output = self.get_output()
        factory_index = self.select_factory(output)
        selected_factory = self.game_engine.central_factory if factory_index == -1 else self.game_engine.factories[factory_index]
        selected_color = self.select_color(selected_factory, output)
        pattern_line_index = self.select_pattern_line(output)

        return factory_index, selected_color, pattern_line_index

    def get_output(self):
        input = self.nn_interface.simplest_input(self.game_engine)
        return self.neural_network.activate(input)

    def select_factory(self, output):
        valid_factories = [i for i, factory in enumerate(self.game_engine.factories, start=1) if factory.tiles]
        # Including central factory as a valid option if it has tiles other than the starting player tile
        central_has_valid_tiles = any(not isinstance(tile, StartingPlayerTile) for tile in self.game_engine.central_factory.tiles)
        if central_has_valid_tiles:
            valid_factories.append(0)  # Using '9' to represent the central factory
        
        # print("All factories: ", self.game_engine.factories)
        # print(f"Valid factories: {valid_factories}")
        # print("Factory preferences: ", output[:10])
        # print("Factory preferences sorted: ", np.argsort(output[:10])[::-1])
        factory_preferences = np.argsort(output[:10])[::-1]  # Sort indices by preference, descending
        for preference in factory_preferences:
            # print(f"Preference: {preference}")
            if preference in valid_factories:
                return preference - 1  # Adjust by -1 to align with list indexing
        return None
    
    def select_color(self, selected_factory, output):
        # Assuming output[10:15] corresponds to color preferences
        color_preferences = np.argsort(output[10:15])[::-1]  # Sort color indices based on preference, descending

        # Map neural network color output indices back to TileColor enum
        color_mapping = list(TileColor)
        available_colors = {tile.color for tile in selected_factory.tiles if not isinstance(tile, StartingPlayerTile)}

        for preference_index in color_preferences:
            preferred_color = color_mapping[preference_index]
            if preferred_color in available_colors:
                return preferred_color  # Return the valid, preferred color based on network output
        return None
    
    def select_pattern_line(self, output):
        return np.argmax(output[15:21])
