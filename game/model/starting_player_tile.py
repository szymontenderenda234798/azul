from model.tile import Tile
from enums.tile_color import TileColor

class StartingPlayerTile(Tile):
    def __init__(self):
        super().__init__(None)
        self.isStartingPlayerTile = True
