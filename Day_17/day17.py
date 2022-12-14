#!/usr/bin/env python
import os
from dataclasses import dataclass
from enum import Enum
import itertools
import time

DRAW_BOARD = False

dirname = os.path.dirname(__file__)
input_file = os.path.join(dirname, 'input.txt')

# A enum for the different types of shapes 
# contains a set of all the points that the shape occupies
# All points are relative to the top left corner of the shape
class ShapeType(Enum):
    HLINE = {(0,0), (1,0), (2,0), (3,0)}
    PLUS = {(1,0), (0,1), (1,1), (2,1), (1,2)}
    REVERSE_L = {(2,0), (2,1), (2,2), (0,0), (1,0)}
    VLINE = {(0,0), (0,1), (0,2), (0,3)}
    SQUARE = {(0,0), (0,1), (1,0), (1,1)}

# Define the offsets for each direction. Left and Right are
# in the input data. "V" is down.
MOVE = {
    '<': (-1, 0),   # Left
    '>': (1, 0),    # Right
    'V': (0, -1)     # Down
}


# Define the colours used for text printing
class Colours(Enum):
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BOLD = "\033[1m"
    NORMAL = "\033[0m"
         
CACHE_CHECK_RANGE = 20

# A class to add a vector and return a new Point. 
# Called to blow a shape left, right, or let it fall
# (defined as a dataclass - new in Python 3.7 - https://realpython.com/python-data-classes/)
@dataclass(frozen=True)
class Point:
    # Define the x,y coordinates that make a point
    x: int
    y: int

    # Add a vector to the point and return a new point
    def __add__(self, vector_point):
        return Point(self.x + vector_point.x, self.y + vector_point.y)

    # Use the __repr__ function to print the point
    def __repr__(self) -> str:
        return (f'({self.x}, {self.y})')


# Shape class 
#   - Has a set of points that make up the shape
#   - Method to create a shape by type and starting position

class Shape:
    # Define the points that make up the shape
    def __init__(self, points: set[Point], shape_type, at_rest=False):
        self.shape_type = shape_type
        self.points = points
        self.at_rest = at_rest

        
    # Move the shape left, right, or down
    # Returns boolean: True if the shape moved, False if it cant move
    def move(self, direction, resting_points):
        if direction == '<':
            # print(Colours.YELLOW.value + 'Move left' + Colours.NORMAL.value)

            # find minimum x value in self.points 
            min_x = min(point.x for point in self.points)

            if min_x == Board.L_WALL + 1:
                # print(Colours.RED.value + 'Hit left wall' + Colours.NORMAL.value)
                return False            
            
        elif direction == '>':
            # print(Colours.YELLOW.value + 'Move right' + Colours.NORMAL.value)

            # find maximum x value in self.points
            max_x = max(point.x for point in self.points)

            if max_x == Board.R_WALL - 1:
                # print(Colours.RED.value + 'Hit right wall' + Colours.NORMAL.value)
                return False

        elif direction == 'V':
            # print(Colours.YELLOW.value + 'Move down' + Colours.NORMAL.value)
            
            # find minimum y value in self.points
            min_y = min(point.y for point in self.points)

            if min_y == Board.FLOOR + 1:
                # print(Colours.RED.value + 'Hit floor' + Colours.NORMAL.value)
                self.at_rest = True
                return False
        else:
            print(f'Invalid direction {direction}')

        candidate_points = {point + Point(*MOVE[direction]) for point in self.points}

        # Check if there is a collision in the two sets of points
        if candidate_points & resting_points:
            # print(Colours.RED.value + 'Collision' + Colours.NORMAL.value)
            return False
        else:
            # Move the shape by the direction
            self.points = {point + Point(*MOVE[direction]) for point in self.points}

            # print(f"Updated coords: {self.shape_type} {self.points}")

            return True
    
    # Create a shape instance by type and starting position
    @classmethod
    def create_shape_by_type(self, shape_type, offset : set[Point]):

        # print(f"Creating new shape at offset {offset}")

        # Create a new shape instance
        # Loop through the points in the shape type and add the starting position offset
        # to each point to get the absolute position of the shape

        return self({(Point(*coords) + offset) for coords in shape_type.value}, shape_type, at_rest=False)


    # Use the __repr__ function to print the shape details
    def __repr__(self) -> str:
        return (f'{self.shape_type} at {self.points}, at_rest={self.at_rest}')



class Board:
    # A grid of unknown height, but a fixed width of 7 columns plus a left and right wall
    WIDTH = 7
    L_WALL = 0
    R_WALL = 8
    FLOOR = 0

    # All rocks drop at top left corner location of (0,3) (plus L_WALL)
    START_X = 3

    # All rocks start at 4 rows above the bottom of the grid
    START_Y = 4

    class PrintableChars(Enum):
        FALLING = Colours.YELLOW.value + '@' + Colours.NORMAL.value
        RESTING = Colours.BLUE.value + '#' + Colours.NORMAL.value
        EMPTY = '.'
        CORNER = Colours.WHITE.value + '+' + Colours.NORMAL.value
        WALL = Colours.WHITE.value + '|' + Colours.NORMAL.value
        FLOOR = Colours.WHITE.value + '-' + Colours.NORMAL.value


    def __init__(self, jetPattern):
        self.top = Board.FLOOR                                          # Location of the current highest rock
        self.shape_generator = itertools.cycle(enumerate(ShapeType))    # A generator to cycle through the shapes (loops)
        self.jetPattern = itertools.cycle(enumerate(jetPattern))        # A generator to cycle through the jet pattern (loops)
        self.rock_origin = Point(Board.START_X, Board.START_Y)          # The starting position of a new rock taking into account left wall and floor
        self.active_shape = None                                        # The current shape that is falling
        self.resting_shapes = set()                                     # A set of shapes that are resting on the board
        self.resting_points = set()                                     # A set of points that are occupied by resting shapes
        self.find_repeating_pattern = False                             # Flag to indicate if a repeating pattern should be found
        self.repeat_found = False                                       # Flag to indicate if a repeating pattern has been found
        self.pattern_cache = {}                                         # A cache of patterns that have been seen (key = shape index, jet index, string of last 20 rows)
        self.debug = False

    def new_shape(self):
        shape_index, shape_type = next(self.shape_generator)

        self.active_shape = Shape.create_shape_by_type(shape_type, self.rock_origin)

        if self.debug:
            print(f'New shape: {self.active_shape}')

        # Loop through the jet pattern until the shape is at rest
        while not self.active_shape.at_rest:
            # Get the next jet pattern
            jet_index, jet_direction = next(self.jetPattern)

            # print(f'Jet: {jet_index} - {jet_direction}')

            # Move the shape for the jet direction
            self.active_shape.move(jet_direction, self.resting_points)

            # Draw the board
            self.draw_board()

            # Move the shape down
            if not self.active_shape.move('V', self.resting_points):
                # Failed to move the shape down

                # Add the shape to the set of resting shapes
                self.resting_shapes.add(self.active_shape)

                # Add the list of shape points to resting points on the board
                self.resting_points.update(self.active_shape.points)

                # Determine where the top of board currently is.
                # If the shape is above the current top, then update the top
                # to the new shape location
                shape_max_y = max(point.y for point in self.active_shape.points) 
                
                if shape_max_y > self.top:
                    self.top = shape_max_y
                        
                    # print(f"New top: {self.top}")

                    # Update the rock origin to the new top of board
                    self.rock_origin = Point(Board.START_X, Board.START_Y + self.top)

                # 
                # Part 2 functionality
                # 
                # Check if this shape index, jet index and the last CACHE_CHECK_RANGE rows of the board match a previously seen
                # pattern. If so, then we have found a repeating pattern and can stop the game.
                #
                # The pattern is stored as a string of the last CACHE_CHECK_RANGE rows of the board, with each row being
                # a string of the printable characters for each point on the board.
                #
                def check_cache(shape_index, jet_index, board):
                    pattern = []

                    # Loop through the last 20 rows of the board
                    for y in range(board.top - CACHE_CHECK_RANGE, board.top + 1):
                        row = []

                        self.row_to_string(y, row)

                        pattern.append(''.join(row))

                    pattern_string = ("\n".join(pattern[::-1]))

                    if (shape_index, jet_index, pattern_string) in self.pattern_cache:
                        # Found a repeating pattern
                        self.repeat_found = True
                        print(f"self.pattern_cache[(shape_index, jet_index, pattern_string)] = {self.pattern_cache[(shape_index, jet_index, pattern_string)]}")

                        return (True, self.pattern_cache[(shape_index, jet_index, pattern_string)])
                    else:
                        # Add the pattern to the cache.
                        # Data is the current board top, and the number of shapes and jets that have been processed
                        # Store in the cache with the key (shape_index, jet_index, pattern_string):
                        #   - The current board height
                        #   - The number of shapes processed
                        self.pattern_cache[(shape_index, jet_index, pattern_string)] = (self.top, len(self.resting_shapes))

                        # print(self.pattern_cache[(shape_index, jet_index, pattern_string)])
                        return (False, None)

                if self.find_repeating_pattern:

                    if self.top > CACHE_CHECK_RANGE:
                        # Check if the cache check returns true
                        cache_response = check_cache(shape_index, jet_index, self)

                        # cache_response[0] = True if a repeating pattern was found
                        # cache_response[1] = The data from the cache (top of board, number of shapes processed)
                        if cache_response[0] == True:
                            # Found a repeating pattern

                            print(f"Repeat found at shape number {len(self.resting_shapes)} with a board height of {self.top}")

                            # Height of repeating pattern is the current board height minus the board height when the pattern was first seen
                            height_of_repeating_pattern = self.top - cache_response[1][0]
                            print(f"Height of repeating pattern = {height_of_repeating_pattern} (Repeat @ {len(self.resting_shapes)} - Cache hit @ {cache_response[1][0]})")

                            # Number of shapes in repeating pattern is the number of shapes processed minus the number of shapes processed when the pattern was first seen
                            num_shapes_in_repeating_pattern = len(self.resting_shapes) - cache_response[1][1]
                            print(f"Number of shapes in repeating pattern = {num_shapes_in_repeating_pattern}")

                            # Remaining drops is 1 trillion minus the number of shapes currently processed 
                            num_remaining_drops = 1000000000000 - len(self.resting_shapes)
                            print(f"Number of remaining drops = {num_remaining_drops}")
                    
                            # Repeats required is the number of remaining drops divided by the number of shapes in the repeating pattern
                            num_repeats_required = num_remaining_drops // num_shapes_in_repeating_pattern
                            print(f"Number of repeats required = {num_repeats_required}")

                            # Height of repeated pattern is the number of repeats required multiplied by the height of the repeating pattern
                            height_of_repeated_pattern = num_repeats_required * height_of_repeating_pattern
                            print(f"Height of repeated pattern = {height_of_repeated_pattern}")

                            # The remaining drops we need to manually process is the number of remaining drops modulo the number of shapes in the repeating pattern
                            num_remaining_drops %= num_shapes_in_repeating_pattern
                            print(f"Number of remaining drops to process = {num_remaining_drops}")

                            # Adjust the height to include the repeated pattern
                            self.height_offset_required = height_of_repeated_pattern
                            print(f"Height offset required = {self.height_offset_required}")

                            # Set the value of the number of remaining drops we need to manually process
                            self.num_remaining_drops = num_remaining_drops
                            

                # Quit moving this shape
                break

            # Draw the board
            self.draw_board()


    def draw_board(self):
        if DRAW_BOARD:
            os.system('cls' if os.name == 'nt' else 'clear')

            print(str(self))

            time.sleep(0.25)     


    def __str__(self) -> str:
        # Prints out the current board state

        rows = []

        top_row = self.top + Board.START_Y + 2

        # Loop through the rows from top to bottom

        for y in range (Board.FLOOR, top_row + 1):
            row = []

            # Print the row number to 3 digits left of the row
            row.append(f"{y:3d}")

            if y == Board.FLOOR:
                    # Floor row
                row.append(Board.PrintableChars.CORNER.value)
                row.extend([Board.PrintableChars.FLOOR.value] * Board.WIDTH)
                row.append(Board.PrintableChars.CORNER.value)
            else:
                    # Loop through the columns
                for x in range(Board.L_WALL, Board.R_WALL + 1):
                    if x == Board.L_WALL or x == Board.R_WALL:
                            # Draw the left and right walls
                        row.append(Board.PrintableChars.WALL.value)
                    elif Point(x,y) in self.active_shape.points:
                            # Draw the active shape
                        row.append(Board.PrintableChars.FALLING.value)
                    elif Point(x,y) in self.resting_points:
                            # Draw the resting shapes
                        row.append(Board.PrintableChars.RESTING.value)
                    else:
                        row.append(Board.PrintableChars.EMPTY.value)

            rows.append(row)

        # return the rows as a string in reverse order
        return (f"{repr(self)}" + "\n".join("".join(row) for row in reversed(rows)))


    def row_to_string(self, y, row):
        #
        # Helper function to convert a row to a string.
        #
                # Loop through the columns
            for x in range(Board.L_WALL, Board.R_WALL + 1):
                if Point(x,y) in self.active_shape.points:
                        # Draw the active shape
                    row.append('#')
                elif Point(x,y) in self.resting_points:
                        # Draw the resting shapes
                    row.append('@')
                else:
                    row.append('.')


    def __repr__(self) -> str:
        return (f"{Colours.BOLD.value}Board: current height = {self.top} {Colours.NORMAL.value} \n")


def main():
    # Work out the current day based on the current file name
    currentDay = os.path.basename(__file__).split('.')[0]
    print(currentDay)

    # Read in the input file to a list
    with open(input_file) as f:
        data = f.read()

    if data:
        print("Part 1")
        # Part 1 will create a new board and add shapes to it until the
        # number of shapes dropped == 2022. The board will then print out
        # the current height of the board

        board = Board(data)

        NUM_SHAPES = 2022

        # Loop for NUM_SHAPES
        for x in range(NUM_SHAPES):
            board.new_shape()
        
        print(f"Part 1 - Top of board: {board.top}")


        print("Part 2")
        # Part 2 will start again, but looking to find a repeating pattern
        # to determine how tall the board will be after 1,000,000,000 shapes 
        # have been dropped

        board = Board(data)
        board.find_repeating_pattern = True

        while board.repeat_found == False:
            board.new_shape()

        # We now know that the pattern repeats and how big this pattern is
        # The height of the repeating pattern to get us near 1 trillion drops
        # has been calculated and stored in board.height_offset_required
        #
        # board.num_remaining_drops is the number of shapes we need to manually
        # process to get to 1 trillion drops        

        # Disable the find repeat pattern flag
        board.find_repeating_pattern = False

        # Set the number of shapes to drop to the number of remaining drops
        NUM_SHAPES = board.num_remaining_drops
  
        # Manually add in the remaining shapes
        for x in range(NUM_SHAPES):
            board.new_shape()

        # Board height = current board height + the height of the offset
        print(f"Part 2 - Top of board: {board.top + board.height_offset_required}")

   
if __name__ == "__main__":
    main()
