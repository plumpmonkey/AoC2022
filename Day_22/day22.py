#!/usr/bin/env python
import os
from dataclasses import dataclass
from enum import Enum
import re

dirname = os.path.dirname(__file__)
input_file = os.path.join(dirname, 'input.txt')

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

# Similar to Day 17. define a point class and use vectors. We can
# add vector coordinates.
@dataclass(frozen=False)
class Point:
    # Define the x,y coordinates that make a point
    x: int
    y: int

    # Define the vector operations
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __repr__(self) -> str:
        return( f"({self.x}, {self.y})" )

MOVE = {
    '<': Point(-1, 0),
    '>': Point(1, 0),
    '^': Point(0, -1),
    'v': Point(0, 1),
}

Direction = {0 : '>', 1 : 'v', 2 : '<', 3 : '^'}

# Utility function to return the direction value from the direction
def return_direction_value(direction):
    for key, value in Direction.items():
        if value == direction:
            return key


# define a class for the instructions
class Instructions:

    def __init__(self, instruction_string):
        self.instruction_string = instruction_string
        self.instruction_list = self.__process_instructions(instruction_string)
        self.index = 0

    def __process_instructions(self, instruction : str):
        # The instructions are a string of characters of an example format:
        # 10R5L5R10L4R5L5
        # This means move 10 steps, then turn right, then move 5 steps, then turn left, etc.
        # We need to split this into a list of instructions of the form distance, direction
        # e.g. [10, R, 5, L, 5, R, 10, L, 4, R, 5, L, 5]
        # We can use a regular expression to do this
        
        # Split the string into a list of numbers and letters
        instruction = re.findall(r'\d+|\D+', instruction)

        return instruction

    def next_instruction(self):
        # Return the next instruction
        instruction = self.instruction_list[self.index]
        self.index += 1
        return instruction


# Define a class to store the map
class Map:

    def __init__(self, map_data):
        self.original_map_data = map_data
        
        # Height is the number of lines in the map
        self.height = len(map_data)
        # The line lengths are not all the same, so we need to find the longest line
        self.width = max([len(line) for line in map_data])
        self.last_instruction = ""

        # Pad the lines to the same length and store the map data
        self.map_grid = self.__pad_lines(map_data)

        # Define the start position
        self.start_position = self.__find_start_position()
        self.current_position = self.start_position

        # Initialise the direction
        self.direction = '>'

        # Generate a list of the columns in the map        
        self.column_list = self.__generate_column_list()
        
        print(f"Map Initialised to size: {self.width} x {self.height}, start position: {self.start_position}")
        
    def __pad_lines(self, map_data):
        # Pad the lines to the same length with spaces
        for i in range(0, len(map_data)):
            map_data[i] = map_data[i].ljust(self.width, ' ')

        return map_data

    def __find_start_position(self):
        # Find the start position on the map. It is the first position that is not a space
        for x in range(0, self.width):
            if self.map_grid[0][x] != ' ':
                return Point(x, 0)
        
    def __generate_column_list(self):
        # Generate a list of the columns in the map
        columnlist= list(zip(*self.map_grid))
        return ["".join(str(char) for char in column) for column in columnlist]



def part1(data):
    print("Part 1")

    return 


def part2(data):
    print("Part 2")

    return


def main():
    # Work out the current day based on the current file name
    currentDay = os.path.basename(__file__).split('.')[0]
    print(currentDay)

    # Read in the input file to a list
    with open(input_file) as f:
        # The data is split into two components. The map and a list of instructions.
        # They are split by a blank line
        map_data, instructions = f.read().split('\n\n')

        # Split the map data into a list of lines
        map_data = map_data.splitlines()

        map_stuff = Map(map_data)

        # Instantiate the instructions class
        instructions = Instructions(instructions)

        # Loop through the instructions and print them out
        for i in range(0, len(instructions.instruction_list)):

            inst = instructions.next_instruction()

            print(f"\n{Colours.MAGENTA.value}Current Direction: {map_stuff.direction}, current position: {map_stuff.current_position}{Colours.NORMAL.value}")

            if inst.isdigit():
                print(f"{Colours.BOLD.value}{Colours.RED.value}Instruction {i}: {inst}{Colours.NORMAL.value}")
                for j in range(0, int(inst)):
                    # Find the next candidate position
                    candidate_position = map_stuff.current_position + MOVE[map_stuff.direction]

                    # Check if we are off the map
                    if candidate_position.x >= map_stuff.width:
                        candidate_position.x = 0
                    elif candidate_position.x < 0:
                        candidate_position.x = map_stuff.width - 1
                    elif candidate_position.y >= map_stuff.height:
                        candidate_position.y = 0
                    elif candidate_position.y < 0:
                        candidate_position.y = map_stuff.height - 1
                        
                    # Check if the candidate position is a space
                    if map_stuff.map_grid[candidate_position.y][candidate_position.x] == ' ':
                        print(f"Found a space at {candidate_position}, wrapping around to the other side of the map at ", end="")

                        # If its a space, we must wrap around to the other side of the map
                        if map_stuff.direction == '>':
                            candidate_position.x = 0
                        elif map_stuff.direction == '<':
                            candidate_position.x = map_stuff.width - 1
                        elif map_stuff.direction == '^':
                            candidate_position.y = map_stuff.height - 1
                        elif map_stuff.direction == 'v':
                            candidate_position.y = 0

                        print(candidate_position)

                        # If the new candidate position is a space, we need to update the current position
                        # until we hit a non-space character
                        while map_stuff.map_grid[candidate_position.y][candidate_position.x] == ' ':
                            candidate_position = candidate_position + MOVE[map_stuff.direction]
                            print(f"Moved to {candidate_position},")
                            if map_stuff.direction == '>':
                                candidate_position.x += 1
                                print(f"> - Updating to {candidate_position}")
                            elif map_stuff.direction == '<':
                                candidate_position.x -= 1
                                print(f"< - Updating to {candidate_position}")
                            elif map_stuff.direction == '^':
                                candidate_position.y -= 1
                                print(f"^ - Updating to {candidate_position}")
                            elif map_stuff.direction == 'v':
                                candidate_position.y += 1
                                print(f"V - Updating to {candidate_position}")


                    # If the new candiate position is a wall (#) we do not update the current position and break
                    # out of the loop. If its a ".", we update the current position
                    if map_stuff.map_grid[candidate_position.y][candidate_position.x] == '#':
                        print(f"{Colours.BOLD.value}{Colours.RED.value}Hit a wall at {candidate_position}{Colours.NORMAL.value}")
                        break
                    else:
                        map_stuff.current_position = candidate_position
                

                    print(f"Current Direction: {map_stuff.direction}, current position: {map_stuff.current_position}")
            else:
                print(f"{Colours.BOLD.value}{Colours.GREEN.value}Instruction {i}: {inst}{Colours.NORMAL.value}")

                # Turn the direction
                if inst == 'R':
                    map_stuff.direction = Direction[(return_direction_value(map_stuff.direction) + 1) % 4]
                else:
                    map_stuff.direction = Direction[(return_direction_value(map_stuff.direction) - 1) % 4]

                
        # print the final position, which is +1 on the x and y coordinates
        final_position = map_stuff.current_position + Point(1, 1)
        print(f"Final position: {final_position}")

        # Final score is row * 1000 + column * 4
        final_score = final_position.y * 1000 + final_position.x * 4

        # add a direction value to the final score. 0 = >, 1 = v, 2 = <, 3 = ^
        final_score += return_direction_value(map_stuff.direction)
        
        print(f"Final score: {final_score}")       
            





if __name__ == "__main__":
    main()
