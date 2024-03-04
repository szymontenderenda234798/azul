from model.player_board import PlayerBoard

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.board = PlayerBoard()

    def place_tile_in_pattern_line(self, tile_color, row, tile_count):
        self.board.place_tile_in_pattern_line(tile_color, row, tile_count)
    
    def place_starting_player_tile_on_floor_line(self):
        self.board.place_starting_player_tile_on_floor_line()

    def take_turn(self):
        pass  # This will be implemented in subclasses

    def print_board(self):
        print(f"{self.name}'s board:")
        self.board.print_board()

    def has_starting_player_tile(self):
        return self.board.has_starting_player_tile()