#TODO: Add all the remaining tiles into the boxlid
class BoxLid:
    def __init__(self):
        self.tiles = []

    def add_tiles(self, tiles):
        """Add tiles to the box lid."""
        self.tiles.extend(tiles)

    def empty_into_tile_bag(self, tile_bag):
        """Empty all tiles from the box lid into the tile bag and shuffle."""
        tile_bag.add_tiles(self.tiles)
        self.tiles = []