#!/usr/bin/env python
import os
from dataclasses import dataclass
from enum import Enum
import re

dirname = os.path.dirname(__file__)
# Change filename to input.txt for the real input or sample.txt for the sample input
filename = "input.txt"
input_file = os.path.join(dirname, filename)

DEBUG = False

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
@dataclass(frozen=True)
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

        # Store the list of points we passed through and direction       
        self.path_points = {self.current_position : self.direction}
        
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


    def score(self):
        # print the final position, which is +1 on the x and y coordinates
        final_position = self.current_position + Point(1, 1)
        print(f"Final position: {final_position}")

        # Final score is row * 1000 + column * 4
        final_score = final_position.y * 1000 + final_position.x * 4

        # add a direction value to the final score. 0 = >, 1 = v, 2 = <, 3 = ^
        final_score += return_direction_value(self.direction)

        return final_score

    def __str__(self) -> str:
        # Print the map
        # Create a list of printable lines in the map
        lines = []

        for y in range(0, self.height):
            line = ""
            for x in range(0, self.width):
                grid_point = Point(x, y)

                # Check if the current position is the start position
                if self.start_position.x == x and self.start_position.y == y:
                    line += (Colours.GREEN.value) + ">" + (Colours.NORMAL.value)
                elif self.current_position.x == x and self.current_position.y == y:
                    line += (Colours.RED.value) + self.direction + (Colours.NORMAL.value)
                elif grid_point in self.path_points:
                    line += (Colours.BLUE.value) + self.path_points[grid_point] + (Colours.NORMAL.value)
                else:
                    line += self.map_grid[y][x]

            lines.append(line)

        return "\n".join(lines)


class CubeMap(Map):
    def __init__(self, map_data, cube_geometry, face_transitions):
        super().__init__(map_data)

        # Store the cube geometry and face transitions data
        self.__cube_geometry = cube_geometry
        print(self.__cube_geometry)
        self.face_transitions = face_transitions

        # Determine how many faces wide our map is (Its different for sample data and real data)
        self.__map_faces_wide = max(x for x,y in self.__cube_geometry) + 1

        print(f"Map is {self.__map_faces_wide} faces wide")

        # Determine how many faces high our map is (Its different for sample data and real data)
        self.__map_faces_high = max(y for x,y in self.__cube_geometry) + 1

        print(f"Map is {self.__map_faces_high} faces high")

        # Determine the width of each face
        self.__face_width = self.width // self.__map_faces_wide

        # Determine the height of each face
        self.__face_height = self.height // self.__map_faces_high

        print(f"Face width: {self.__face_width}, Face height: {self.__face_height}")


    def get_face_for_location(self, location):
        # Get the face for the given location (actual face value, not the index)
        # 
        # Dividing the current real map location by a face width and height will
        # give us the index of the face in the cube geometry list
        # We can map that to an actual face 

        face_x = location.x // self.__face_width
        face_y = location.y // self.__face_height

        # Get the face index from the cube geometry list
        face_value = self.__cube_geometry.index((face_x, face_y)) + 1

        return face_value

    def get_point_on_face(self,location):
        # Take the real map location and convert it to a point on the face
       
        face_x = location.x % self.__face_width
        face_y = location.y % self.__face_height

        return Point(face_x, face_y)


    def convert_face_point_to_map_point(self, face, point):
        # Convert a point on a face to a point on the real map

        # Get the face index from the cube geometry list
        face_location = (self.__cube_geometry[face - 1])

        # Get the real map location of the face
        map_x = face_location[0] * self.__face_width + point.x
        map_y = face_location[1] * self.__face_height + point.y

        return Point(map_x, map_y)

    def is_valid_face_position(self, face_point):
        if(face_point.x < 0 or face_point.y < 0 or face_point.x >= self.__face_width or face_point.y >= self.__face_height):
            return False
        else:
            return True

    def get_face_transition(self, face, direction):
        # Get the face transition for the given face and direction
        # 
        # The face transitions are stored as a dictionary with the key being
        # the face and direction, and the value being the face to transition to

        return self.__face_transitions[(face, direction)]

    def get_next_face_point(self, face, face_point):
        # We have moved off the current face
        # Convert our current face position to a map position
        current_map_position = self.convert_face_point_to_map_point(face, face_point)
        # We then need to work out which face we are moving to
        # 
        # Use the current face and direction to get the new face and direction
        new_face, new_direction = self.face_transitions[(face, self.direction)]

        if DEBUG:
            print(f"{Colours.BLUE.value}Moving from current map position {current_map_position} face {face} to face {new_face} in direction {new_direction}{Colours.NORMAL.value}")
            
        # Determine the current direction so we know which direction to save
        if self.direction == 'v':
            if new_direction == 'v':
                # We  were moving down and are still moving down
                new_face_point = Point(face_point.x, 0)
            elif new_direction == '^':
                # We were moving down and are now moving up
                new_face_point = Point(self.__face_width - 1 - face_point.x, self.__face_height - 1)
            elif new_direction == '<':
                # We were moving down and are now moving left
                new_face_point = Point(self.__face_width - 1, face_point.x)
            elif new_direction == '>':
                # We were moving down and are now moving right
                new_face_point = Point(self.__face_height - 1 - face_point.x, 0)
        elif self.direction == '^':
            if new_direction == 'v':
                # We  were moving up and are now moving down
                new_face_point = Point(self.__face_width - 1 - face_point.x, 0)
            elif new_direction == '^':
                # We were moving up and are still moving up
                new_face_point = Point(face_point.x, self.__face_height - 1)   
            elif new_direction == '<':
                new_face_point = Point(self.__face_width - 1, self.__face_height - 1 - face_point.x)
            elif new_direction == '>':
                new_face_point = Point(0, face_point.x)
        elif self.direction == '<':
            if new_direction == 'v':
                new_face_point = Point(face_point.y, 0)
            elif new_direction == '^':
                new_face_point = Point(self.__face_width - 1 - face_point.y, self.__face_height - 1)
            elif new_direction == '<':
                new_face_point = Point(self.__face_width - 1, face_point.y)
            elif new_direction == '>':
                new_face_point = Point(0, self.__face_height - 1 - face_point.y)    
        elif self.direction == '>':
            if new_direction == 'v':
                new_face_point = Point(self.__face_width - 1 - face_point.y, 0)
            elif new_direction == '^':
                new_face_point = Point(face_point.y, self.__face_height - 1)
            elif new_direction == '<':
                new_face_point = Point(self.__face_width - 1, self.__face_height - 1 - face_point.y)
            elif new_direction == '>':
                new_face_point = Point(0, face_point.y)


        # Convert the new face point to a map point
        candidate_map_position = self.convert_face_point_to_map_point(new_face , new_face_point)

        if DEBUG:
            print(f"{Colours.BLUE.value}Old face point {face_point} face point: {new_face_point}{Colours.NORMAL.value}")
            print(f"candidate_map_position: {candidate_map_position} - contents: {self.map_grid[candidate_map_position.y][candidate_map_position.x]}")

        if self.map_grid[candidate_map_position.y][candidate_map_position.x] == '#':
            # new position is a wall. Return false
            return False
        else:
            # new position is not a wall.
            # Update the new position set the new direction and return true
            if DEBUG:
                print(f"Setting new direction to {new_direction} and new position to {candidate_map_position}")

            self.direction = new_direction
            self.current_position = candidate_map_position
            self.path_points[self.current_position] = self.direction

            
            return True


def part1(flat_map_data, instructions):
    print("Part 1")

    # Loop through the instructions and print them out
    for i in range(0, len(instructions.instruction_list)):

        inst = instructions.next_instruction()

        if DEBUG:
            print(f"\n{Colours.MAGENTA.value}Current Direction: {flat_map_data.direction}, current position: {flat_map_data.current_position}{Colours.NORMAL.value}")

        if inst.isdigit():
            if DEBUG:
                print(f"{Colours.BOLD.value}{Colours.RED.value}Instruction {i}: {inst}{Colours.NORMAL.value}")

            for j in range(0, int(inst)):
                # Find the next candidate position
                candidate_position = flat_map_data.current_position + MOVE[flat_map_data.direction]

                # Check if we are off the map
                if candidate_position.x >= flat_map_data.width:
                    candidate_position = Point(0, candidate_position.y)
                elif candidate_position.x < 0:
                    candidate_position  = Point(flat_map_data.width - 1, candidate_position.y)
                elif candidate_position.y >= flat_map_data.height:
                    candidate_position = Point(candidate_position.x, 0)
                elif candidate_position.y < 0:
                    candidate_position = Point(candidate_position.x, flat_map_data.height - 1)
                    
                # Check if the candidate position is a space
                if flat_map_data.map_grid[candidate_position.y][candidate_position.x] == ' ':
                    if DEBUG:
                        print(f"Found a space at {candidate_position}, wrapping around to the other side of the map at ", end="")

                    # If its a space, we must wrap around to the other side of the map
                    if flat_map_data.direction == '>':
                        candidate_position = Point(0, candidate_position.y)
                    elif flat_map_data.direction == '<':
                        candidate_position = Point(flat_map_data.width - 1, candidate_position.y)
                    elif flat_map_data.direction == '^':
                        candidate_position = Point(candidate_position.x, flat_map_data.height - 1)
                    elif flat_map_data.direction == 'v':
                        candidate_position = Point(candidate_position.x, 0)

                    # If the new candidate position is a space, we need to update the current position
                    # until we hit a non-space character
                    while flat_map_data.map_grid[candidate_position.y][candidate_position.x] == ' ':
                        candidate_position = candidate_position + MOVE[flat_map_data.direction]
                        if flat_map_data.direction == '>':
                            candidate_position = Point(candidate_position.x + 1, candidate_position.y)
                        elif flat_map_data.direction == '<':
                            candidate_position = Point(candidate_position.x - 1, candidate_position.y)
                        elif flat_map_data.direction == '^':
                            candidate_position = Point(candidate_position.x, candidate_position.y - 1)
                        elif flat_map_data.direction == 'v':
                            candidate_position = Point(candidate_position.x, candidate_position.y + 1)

                # If the new candiate position is a wall (#) we do not update the current position and break
                # out of the loop. If its a ".", we update the current position
                if flat_map_data.map_grid[candidate_position.y][candidate_position.x] == '#':
                    if DEBUG:
                        print(f"{Colours.BOLD.value}{Colours.RED.value}Hit a wall at {candidate_position}{Colours.NORMAL.value}")
                    break
                else:
                    # Update the current position
                    flat_map_data.current_position = candidate_position

                    # Store the current position in the path
                    flat_map_data.path_points[flat_map_data.current_position] = flat_map_data.direction
            
                if DEBUG:
                    print(f"Current Direction: {flat_map_data.direction}, current position: {flat_map_data.current_position}")
        else:
            if DEBUG:
                print(f"{Colours.BOLD.value}{Colours.GREEN.value}Instruction {i}: {inst}{Colours.NORMAL.value}")

            # Turn the direction
            if inst == 'R':
                # Add or subtract 1 from the direction value, then mod 4 to wrap around the list                
                flat_map_data.direction = Direction[(return_direction_value(flat_map_data.direction) + 1) % 4]
            else:
                flat_map_data.direction = Direction[(return_direction_value(flat_map_data.direction) - 1) % 4]  

    print(f"Final score: {flat_map_data.score()}")       
    
    print(flat_map_data)
    return 


def part2(cube_map_data, instructions):
    print("Part 2")

    # Part 2 turns the map into a cube
    # The sample cube has a different geometry to the real input data, so we need a way
    # to represent the cube face positions in the input data and how the faces map to
    # each other so we can dynamically work out the transition from face to face.

    # The sample cube is defined as:
    #         1111
    #         1111
    #         1111
    #         1111
    # 222233334444
    # 222233334444
    # 222233334444
    # 222233334444
    #         55556666
    #         55556666
    #         55556666
    #         55556666
    # 
    # On a grid system we can represent this as:
    #
    #     0   1   2   3
    #   |---|---|---|---|
    # 0 |   |   | 1 |   |
    #   |---|---|---|---|
    # 1 | 2 | 3 | 4 |   |
    #   |---|---|---|---|
    # 2 |   |   | 5 | 6 |
    #   |---|---|---|---|
    #
    # So face 1 is at (2, 0) and face 2 is at (0, 1), face 3 is at (1, 1) and so on.
    #
    # We can also define the transition between faces. This needs to be done in a (face, direction) tuple
    # mapping to a (face, new_direction) tuple. For example, if we are on face 1 and move move up, 
    # we move to face 2 moving down. If we are on face 2 and move left, we move to face 6 moving up. 
    # 
    # The transition mapping is:
    # (1, '^') -> (2, 'v')
    # (1, '>') -> (6, '<')
    # (1, 'v') -> (4, 'v')
    # (1, '<') -> (3, 'v')
    
    sample_data_cube_geometry = [(2,0), (0,1), (1,1), (2,1), (2,2), (3,2)]

    sample_data_face_transition = {
        (1, '^'): (2, 'v'),
        (1, '>'): (6, '<'),
        (1, 'v'): (4, 'v'),
        (1, '<'): (3, 'v'),
        (2, '^'): (1, 'v'),
        (2, '>'): (3, '>'),
        (2, 'v'): (5, '^'),
        (2, '<'): (6, '^'),
        (3, '^'): (1, '>'),
        (3, '>'): (4, '>'),
        (3, 'v'): (5, '>'),
        (3, '<'): (2, '<'),
        (4, '^'): (1, '^'),
        (4, '>'): (6, 'v'),
        (4, 'v'): (5, 'v'),
        (4, '<'): (3, '<'),
        (5, '^'): (4, '^'),
        (5, '>'): (6, '>'),
        (5, 'v'): (2, '^'),
        (5, '<'): (3, '^'),
        (6, '^'): (4, '<'),
        (6, '>'): (1, '<'),
        (6, 'v'): (2, '>'),
        (6, '<'): (5, '<'),
    }

    real_data_cube_geometry = [(1,0), (2,0), (1,1), (0,2), (1,2), (0,3)]

    real_data_face_transition = {
        (1, '^'): (6, '>'),
        (1, '>'): (2, '>'),
        (1, 'v'): (3, 'v'),
        (1, '<'): (4, '>'),
        (2, '^'): (6, '^'),
        (2, '>'): (5, '<'),
        (2, 'v'): (3, '<'),
        (2, '<'): (1, '<'),
        (3, '^'): (1, '^'),
        (3, '>'): (2, '^'),
        (3, 'v'): (5, 'v'),
        (3, '<'): (4, 'v'),
        (4, '^'): (3, '>'),
        (4, '>'): (5, '>'),
        (4, 'v'): (6, 'v'),
        (4, '<'): (1, '>'),
        (5, '^'): (3, '^'),
        (5, '>'): (2, '<'),
        (5, 'v'): (6, '<'),
        (5, '<'): (4, '<'),
        (6, '^'): (4, '^'),
        (6, '>'): (5, '^'),
        (6, 'v'): (2, 'v'),
        (6, '<'): (1, 'v'),
    }

    if filename == 'sample.txt':
        cube_map = CubeMap(cube_map_data, sample_data_cube_geometry, sample_data_face_transition)
    else:
        cube_map = CubeMap(cube_map_data, real_data_cube_geometry, real_data_face_transition)

    # Test functions
    #
    # cube_map.get_face_for_location(Point(5,5))
    # cube_map.get_point_on_face(Point(5,5))
    # print(cube_map.convert_face_point_to_map_point(1, Point(0,0)))
    # print(cube_map.convert_face_point_to_map_point(2, Point(0,0)))
    # print(cube_map.convert_face_point_to_map_point(3, Point(0,0)))
    # print(cube_map.convert_face_point_to_map_point(4, Point(0,0)))
    # print(cube_map.convert_face_point_to_map_point(5, Point(0,0)))
    # print(cube_map.convert_face_point_to_map_point(6, Point(0,0)))
    
    # Loop through the instructions and print them out
    for i in range(0, len(instructions.instruction_list)):

        inst = instructions.next_instruction()

        if DEBUG:
            # Convert the current position to a position on the face
            face_point = cube_map.get_point_on_face(cube_map.current_position)

            # Get the current face number
            face_number = cube_map.get_face_for_location(cube_map.current_position)

            print(f"\n{Colours.MAGENTA.value}Current Direction: {cube_map.direction}, current map position: {cube_map.current_position}, Face {face_number}, face_position{face_point}{Colours.NORMAL.value}")

        if inst.isdigit():
            if DEBUG:
                print(f"{Colours.BOLD.value}{Colours.RED.value}Instruction {i}: {inst}{Colours.NORMAL.value}")

            # Loop for the required number of steps
            for j in range(0, int(inst)):
                # Convert the current position to a position on the face
                face_point = cube_map.get_point_on_face(cube_map.current_position)

                # Get the current face number
                face_number = cube_map.get_face_for_location(cube_map.current_position)

                # Get a candidate position on the face for the next move
                face_candidate_position = face_point + MOVE[cube_map.direction]

                # Validate the candidate position is still on this face
                if cube_map.is_valid_face_position(face_candidate_position):
                    # We are still on the same face
                    # Check we havent hit a wall. Convert the candidate position to a map position
                    candidate_map_position = cube_map.convert_face_point_to_map_point(face_number, face_candidate_position)

                    if DEBUG:
                        print(f"candidate_map_position: {candidate_map_position} - contents: {cube_map.map_grid[candidate_map_position.y][candidate_map_position.x]}")
                    
                    if cube_map.map_grid[candidate_map_position.y][candidate_map_position.x] == '#':
                        # We have hit a wall
                        if DEBUG:
                            print(f"{Colours.BOLD.value}{Colours.RED.value}Hit a wall at {candidate_map_position}{Colours.NORMAL.value}")
                        break
                    else:
                        # Convert the candidate position to a map position
                        cube_map.current_position = cube_map.convert_face_point_to_map_point(face_number, face_candidate_position)

                        # Store the current position in the path
                        cube_map.path_points[cube_map.current_position] = cube_map.direction
                else:
                    # We have moved off the current face
                    # Pass the current face number and the current face point to get the next face number and point
                    # The function will determine the the transition point and the next face number
                    # and will return false if the transition point is invalid (Eg, there is a wall in the way)
                    # If it returns True, then the current position will be updated to the new face point
                    if cube_map.get_next_face_point(face_number, face_point):
                        # We have moved to a new face
                        if DEBUG:
                            print(f"{Colours.BOLD.value}{Colours.RED.value}Moved to a new face{Colours.NORMAL.value}")
                    else: 
                        # We have hit a wall
                        if DEBUG:
                            print(f"{Colours.BOLD.value}{Colours.RED.value}Hit a wall on the new face{Colours.NORMAL.value}")
                        break
        else:
            if DEBUG:
                print(f"{Colours.BOLD.value}{Colours.GREEN.value}Instruction {i}: {inst}{Colours.NORMAL.value}")

            # Turn the direction
            if inst == 'R':
                # Add or subtract 1 from the direction value, then mod 4 to wrap around the list                
                cube_map.direction = Direction[(return_direction_value(cube_map.direction) + 1) % 4]
            else:
                cube_map.direction = Direction[(return_direction_value(cube_map.direction) - 1) % 4]  

    print(cube_map)
    print(f"Final score: {cube_map.score()}")       


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

        flat_map_instance = Map(map_data)

        # Instantiate the instructions class
        instructions = Instructions(instructions)

        # part1(flat_map_instance, instructions)

        part2(map_data, instructions)

            

if __name__ == "__main__":
    main()
