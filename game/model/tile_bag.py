from enums.tile_color import TileColor
from model.tile import Tile
from model.box_lid import BoxLid
import random

class TileBag:
    def __init__(self, box_lid):
        # Initialize the bag with 20 tiles of each color, using the TileColor enum
        self.tiles = [Tile(color) for color in TileColor for _ in range(20)]
        random.shuffle(self.tiles)
        self.box_lid = box_lid

    def draw_tiles(self, number):
        """Draw a specified number of tiles from the bag. Refill from the box lid if empty."""
        if len(self.tiles) < number:  # Check if there are not enough tiles
            if not self.box_lid.tiles:
                # This scenario implies the game might be in a state where no tiles are available to draw
                # which could be a condition to check for game end or a specific game state
                print("Not enough tiles available in the tile bag and the box lid is empty.")
                return []

            # Refill the tile bag from the box lid if the tile bag is empty or has fewer tiles than needed
            print("Refilling tile bag from box lid.")
            self.box_lid.empty_into_tile_bag(self)
            random.shuffle(self.tiles)  # Ensure the tiles are shuffled

        drawn_tiles = self.tiles[:number]
        self.tiles = self.tiles[number:]
        return drawn_tiles

    def add_tiles(self, tiles):
        """Add tiles back to the bag, typically from the box lid."""
        self.tiles.extend(tiles)