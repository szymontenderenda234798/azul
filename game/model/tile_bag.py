from enums.tile_color import TileColor
from model.tile import Tile
import random

class TileBag:
    def __init__(self):
        # Initialize the bag with 20 tiles of each color, using the TileColor enum
        self.tiles = [Tile(color) for color in TileColor for _ in range(20)]
        random.shuffle(self.tiles)

    def draw_tiles(self, number):
        drawn_tiles = []
        for _ in range(number):
            if not self.tiles:
                break
            drawn_tiles.append(self.tiles.pop())
        return drawn_tiles

    def refill(self):
        self.tiles = [Tile(color) for color in TileColor for _ in range(20)]
        random.shuffle(self.tiles)