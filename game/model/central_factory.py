from model.factory import Factory
from model.starting_player_tile import StartingPlayerTile
from enums.tile_color import TileColor

class CentralFactory(Factory):
    def __init__(self):
        super().__init__()
        self.starting_player_marker_taken = False
        self.tiles.append(StartingPlayerTile())

    
    def remove_and_return_tiles_of_color(self, tile_color):
        if not self.starting_player_marker_taken:
            self.starting_player_marker_taken = True
        return super().remove_and_return_tiles_of_color(tile_color)
    
    def add_starting_player_tile(self):
        self.tiles.append(StartingPlayerTile())