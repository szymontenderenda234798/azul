from model.tile import Tile
from model.starting_player_tile import StartingPlayerTile
from enums.tile_color import TileColor

class PlayerBoard:
    def __init__(self):
        self.pattern_lines = [[None, None, None, None, None] for _ in range(5)]  # 5 pattern lines, up to 5 tiles each
        self.wall = [[None for _ in range(5)] for _ in range(5)]  # 5x5 grid, initially empty
        self.floor_line = []  # Will hold tiles that overflow or are not placed

        # Define the fixed color pattern on the wall
        self.wall_pattern = [
            [TileColor.BLUE, TileColor.YELLOW, TileColor.RED, TileColor.BLACK, TileColor.WHITE],
            [TileColor.WHITE, TileColor.BLUE, TileColor.YELLOW, TileColor.RED, TileColor.BLACK],
            [TileColor.BLACK, TileColor.WHITE, TileColor.BLUE, TileColor.YELLOW, TileColor.RED],
            [TileColor.RED, TileColor.BLACK, TileColor.WHITE, TileColor.BLUE, TileColor.YELLOW],
            [TileColor.YELLOW, TileColor.RED, TileColor.BLACK, TileColor.WHITE, TileColor.BLUE]
        ]

    def place_tile_in_pattern_line(self, tile_color, pattern_line_index, tile_count):
        """
        Attempt to place tiles in a specified pattern line.
        
        :param tile_color: The color of the tiles being placed.
        :param pattern_line_index: The index of the pattern line (0-4).
        :param tile_count: The number of tiles being placed.
        """
        pattern_line = self.pattern_lines[pattern_line_index]
        line_capacity = pattern_line_index + 1  # The capacity matches the row index + 1
        existing_tiles = sum(1 for tile in pattern_line if tile is not None)
        space_left = line_capacity - existing_tiles

        # Calculate how many tiles can be actually placed in the pattern line
        tiles_to_place = min(space_left, tile_count)

        if existing_tiles == 0 or (pattern_line[0] is not None and pattern_line[0].color == tile_color):
            # Place as many tiles as possible into the pattern line
            for i in range(existing_tiles, existing_tiles + tiles_to_place):
                pattern_line[i] = Tile(tile_color)
            # Any excess tiles go to the floor line
            excess_tiles = tile_count - tiles_to_place
            if excess_tiles > 0:
                self.add_tiles_to_floor_line([Tile(tile_color)] * excess_tiles)
        else:
            # If the pattern line has tiles of a different color, use the new method to add all tiles to the floor line
            self.add_tiles_to_floor_line([Tile(tile_color)] * tile_count)

    def place_starting_player_tile_on_floor_line(self):
        """Place the starting player tile on the floor line."""
        self.add_tiles_to_floor_line([StartingPlayerTile()])

    def move_tiles_to_wall(self):
        """Move tiles from the pattern lines to the wall, based on the rules."""
        for row_index, row in enumerate(self.pattern_lines):
            if len(row) == row_index + 1:  # Check if the row is full
                tile_color = row[0]
                # Find the correct column based on the wall pattern
                column_index = self.wall_pattern[row_index].index(tile_color)
                if self.wall[row_index][column_index] is None:  # If space is empty
                    self.wall[row_index][column_index] = tile_color
                    self.pattern_lines[row_index] = []  # Clear the pattern line
                else:
                    # If the space on the wall is already filled, this should be handled as per game rules (e.g., move to floor line)
                    pass

    def print_board(self):
        print("Pattern Lines:")
        for index, line in enumerate(self.pattern_lines):
            # Represent each tile or empty space in the pattern line
            line_representation = [tile.name if tile is not None else 'None' for tile in line[:index+1]]
            print(f"Line {index + 1}: {line_representation}")

        print("\nWall:")
        for row in self.wall:
            # Represent each tile or empty space on the wall
            row_representation = [tile.name if tile is not None else 'None' for tile in row]
            print(row_representation)

        print("\nFloor Line:")
        # Represent tiles in the floor line
        floor_line_representation = [tile.name for tile in self.floor_line]
        print(floor_line_representation or 'Empty')

    # Additional methods for scoring, handling the floor line, etc., can be added here.
        
    def add_tiles_to_floor_line(self, tiles):
        """
        Add tiles to the floor line, respecting the maximum capacity of 7 tiles.
        
        :param tiles: A list of Tile objects to be added to the floor line.
        """
        max_capacity = 7
        # Calculate available space on the floor line
        available_space = max_capacity - len(self.floor_line)

        if available_space <= 0:
            return  # If no space is available, ignore the tiles

        # If there's more tiles than available space, only add up to the available space
        tiles_to_add = tiles[:available_space]
        self.floor_line.extend(tiles_to_add)