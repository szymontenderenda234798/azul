class Factory:
    def __init__(self):
        self.tiles = []

    def add_tiles(self, tiles):
        self.tiles.extend(tiles)

    def remove_and_return_tiles_of_color(self, tile_color):
        """Remove and return all tiles of a specific color, leaving the rest."""
        selected_tiles = [tile for tile in self.tiles if tile.color == tile_color]
        self.tiles = [tile for tile in self.tiles if tile.color != tile_color]
        return selected_tiles
    
    def get_and_clear_remaining_tiles(self):
        """Return and clear all remaining tiles."""
        remaining_tiles = self.tiles[:]
        self.tiles = []
        return remaining_tiles