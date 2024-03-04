from enums.tile_color import TileColor

class Tile:
    def __init__(self, color):
        self.color = color
        self.isStartingPlayerTile = False
        self.name = color.value if color else "starting player tile"