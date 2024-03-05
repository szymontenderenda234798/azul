import numpy as np

class NeuralNetworkInterface:
    def __init__(self, game_engine):
        self.game_engine = game_engine

    def game_state_to_network_input(self):
        """
        Transforms the current game state into the input format required by the neural network.
        """
        # Assuming 5 tile colors and 5 factories + 1 central factory
        num_colors = 5
        num_factories = 5
        input_vector = []

        # Encode tiles in factories
        for factory in self.game_engine.factories + [self.game_engine.central_factory]:
            for color in range(num_colors):
                input_vector.append(factory.tiles.count(color) / 4.0)  # Normalize by max number of tiles

        # Encode the player's pattern lines (simplified)
        for line in range(1, 6):  # Assuming 5 pattern lines
            for color in range(num_colors):
                # Check if this color is in the pattern line and normalize counts
                color_count = self.game_engine.player.board.pattern_lines[line-1].count(color)
                input_vector.append(color_count / line)  # Normalize by line capacity

        # Encode the player's wall (binary: tile placed or not)
        for row in self.game_engine.player.board.wall:
            for tile_placed in row:
                input_vector.append(float(tile_placed is not None))

        # Convert to a format suitable for the neural network (e.g., NumPy array)
        print(np.array(input_vector))
        return np.array(input_vector)