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
        if self.is_color_on_wall(tile_color, pattern_line_index):
            # Redirect the tiles to the floor line
            self.add_tiles_to_floor_line([Tile(tile_color)] * tile_count)
        else:
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

    def is_color_on_wall(self, tile_color, pattern_line_index):
        """
        Check if a tile of the specified color is already on the wall in the row
        corresponding to the pattern line index.
        """
        # This method assumes the wall_pattern defines the placement rules for tiles
        # and that self.wall[row][col] is None if no tile is placed at that position.
        color_position = self.wall_pattern[pattern_line_index].index(tile_color)
        return self.wall[pattern_line_index][color_position] is not None

    def place_starting_player_tile_on_floor_line(self):
        """Place the starting player tile on the floor line."""
        self.floor_line.append(StartingPlayerTile())

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
        self.print_pattern_lines()
        print()
        self.print_wall()
        print()
        self.print_floor_line()

    def print_pattern_lines(self):
        print("Pattern Lines:")
        for index, line in enumerate(self.pattern_lines):
            # Represent each tile or empty space in the pattern line
            line_representation = [tile.name if tile is not None else 'None' for tile in line[:index+1]]
            print(f"Line {index + 1}: {line_representation}")

    def print_wall(self):
        print("Wall:")
        for row in self.wall:
            # Represent each tile or empty space on the wall
            row_representation = [tile.name if tile is not None else 'None' for tile in row]
            print(row_representation)

    def print_floor_line(self):
        print("Floor Line:")
        # Represent tiles in the floor line
        floor_line_representation = [tile.name for tile in self.floor_line]
        print(floor_line_representation or 'Empty')



    # Additional methods for scoring, handling the floor line, etc., can be added here.
        
    def add_tiles_to_floor_line(self, tiles):
        """
        Add tiles to the floor line, respecting the maximum capacity of 7 tiles.
        Excess tiles are added to the box lid.
        
        :param tiles: A list of Tile objects to be added to the floor line.
        """
        max_capacity = 7
        # Calculate available space on the floor line
        available_space = max_capacity - len(self.floor_line)

        if available_space > 0:
            # If there's space, add tiles up to the available space
            tiles_to_add = tiles[:available_space]
            self.floor_line.extend(tiles_to_add)
            excess_tiles = tiles[available_space:]
        else:
            # If no space is available, all tiles are considered excess
            excess_tiles = tiles

        # Add any excess tiles to the box lid
        if excess_tiles:
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            print(f"Floor line is full! Adding {len(excess_tiles)} excess tiles to the box lid.")
            print(f"box lid tiles: {len(self.box_lid.tiles)}")
            self.box_lid.add_tiles(excess_tiles)
            print(f"box lid tiles after adding: {len(self.box_lid.tiles)}")


    def move_tiles_to_wall_and_score(self):
        """
        Move tiles from completed pattern lines to the wall, score points, and move remaining tiles to the box lid.
        """
        score = 0
        for row_index, pattern_line in enumerate(self.pattern_lines):
            # Identify completed pattern lines
            if None not in pattern_line[:row_index + 1]:
                # Assume the tile color is the same for all in the line, take the first one
                tile_color = pattern_line[0].color if pattern_line[0] is not None else None
                
                if tile_color is not None:
                    # Find the correct position on the wall based on the color pattern
                    column_index = self.wall_pattern[row_index].index(tile_color)
                    
                    # Move one tile to the wall
                    if self.wall[row_index][column_index] is None:  # Ensure the spot is empty
                        self.wall[row_index][column_index] = Tile(tile_color)
                        # Calculate score for this move
                        score += self.calculate_score_for_tile(row_index, column_index)
                    
                    # Move the remaining tiles in the completed line to the box lid
                    excess_tiles = [tile for tile in pattern_line if tile is not None][1:]  # Skip the first tile which was moved to the wall
                    if excess_tiles:
                        print(f"box lid size before moving: {len(self.box_lid.tiles)}")
                        print(f"Moving {len(excess_tiles)} excess tiles to the box lid.")
                        print(f"box lid size after moving: {len(self.box_lid.tiles)}")
                        print(f"excess tiles: {[tile.name for tile in excess_tiles]}")

                        self.box_lid.add_tiles(excess_tiles)
                
                # Clear the pattern line after moving tiles to the wall and box lid
                self.pattern_lines[row_index] = [None] * 5

        # Score the floor line and clear it
        score += self.score_floor_line()
        print("Floor line after scoring: ", [tile.name for tile in self.floor_line])
        tiles_to_box_lid = [tile for tile in self.floor_line if not isinstance(tile, StartingPlayerTile)]
        self.box_lid.add_tiles(tiles_to_box_lid)
        self.floor_line = []

        # Return the total score for this round
        return score
    
    def calculate_score_for_tile(self, row, column):
        """
        Calculate the score for placing a tile on the wall, considering adjacent tiles.
        """
        score = 1  # Base score for placing a tile
        
        # Check horizontally
        row_score = 1  # Start with 1 for the placed tile
        # Check left
        moving_col = column - 1
        while moving_col >= 0 and self.wall[row][moving_col] is not None:
            row_score += 1
            moving_col -= 1
        # Check right
        moving_col = column + 1
        while moving_col < 5 and self.wall[row][moving_col] is not None:
            row_score += 1
            moving_col += 1
        if row_score > 1:  # If there are adjacent tiles horizontally, add to score
            score += row_score - 1  # Subtract 1 because the tile itself was counted twice
        
        # Check vertically
        column_score = 1  # Start with 1 for the placed tile
        # Check up
        moving_row = row - 1
        while moving_row >= 0 and self.wall[moving_row][column] is not None:
            column_score += 1
            moving_row -= 1
        # Check down
        moving_row = row + 1
        while moving_row < 5 and self.wall[moving_row][column] is not None:
            column_score += 1
            moving_row += 1
        if column_score > 1:  # If there are adjacent tiles vertically, add to score
            score += column_score - 1  # Subtract 1 for the same reason
        
        return score
    
    def score_floor_line(self):
        penalties = [1, 1, 2, 2, 2, 3, 3]  # Base penalties for the first 7 tiles
        score = -sum(penalties[:len(self.floor_line)])  # Calculate penalties for up to the first 7 tiles
        print(f"Penalties for the floor line: {score} points.")
        if len(self.floor_line) > 7:  # For more than 7 tiles, each additional tile incurs -3 points
            score -= (len(self.floor_line) - 7) * 3
        return score
    
    def has_starting_player_tile(self):
        """Check if this player board has the starting player tile on the floor line."""
        return any(isinstance(tile, StartingPlayerTile) for tile in self.floor_line)
    
    def has_completed_row_on_wall(self):
        for row in self.wall:
            if None not in row:
                return True
        return False
    
    def count_placed_tiles(self):
        """Count the number of tiles placed on the pattern lines and wall."""
        wall_tiles_count = sum(tile is not None for row in self.wall for tile in row)
        pattern_lines_tiles_count = sum(tile is not None for line in self.pattern_lines for tile in line)
        floor_line_tiles_count = len([tile for tile in self.floor_line if not isinstance(tile, StartingPlayerTile)])

        # Sum the counts from the wall and pattern lines
        total_placed_tiles = wall_tiles_count + pattern_lines_tiles_count + floor_line_tiles_count
        return total_placed_tiles