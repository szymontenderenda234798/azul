from model.player_board import PlayerBoard

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.board = PlayerBoard()
        self.game_engine = None

    def place_tile_in_pattern_line(self, tile_color, row, tile_count):
        self.board.place_tile_in_pattern_line(tile_color, row, tile_count)
    
    def place_starting_player_tile_on_floor_line(self):
        self.board.place_starting_player_tile_on_floor_line()

    def make_decision(self):
        pass

    def select_factory(self):
        pass

    def select_color(self, factory):
        pass

    def select_pattern_line(self):
        pass

    def print_board(self):
        print(f"{self.name}'s board:")
        self.board.print_board()

    def has_starting_player_tile(self):
        return self.board.has_starting_player_tile()
    
    def has_completed_row_on_wall(self):
        return self.board.has_completed_row_on_wall()
    
    def move_tiles_to_wall_and_score(self):
        return self.board.move_tiles_to_wall_and_score()