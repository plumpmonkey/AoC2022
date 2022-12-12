#!/usr/bin/env python
import os
from string import ascii_lowercase


dirname = os.path.dirname(__file__)
input_file = os.path.join(dirname, 'input.txt')

def read_data_into_nodes_dictionary(data):
    # We will construction a dictionary of (x,y) coordinates based on the input
    # giving the value between 0-25 for a-z and 26 for the end point E.
    
    # We will use a dictionary to store the nodes
    nodes_dict = {}

    # We will use a list to store the starting points for part 2
    a_starting_nodes = []

    # Edge cases. Mark our Starting point as height 0 and our end point as height 26
    edge_cases = {"E": 26, "S" : 0}

    # Read the grid in a line at a time
    for x, line in enumerate(data):
        
        # For each line, extract the  node point
        for y, value in enumerate(line):
            if value == "S":
                # We have found the starting location coordinate. Log it
                start_point = (x, y)
            elif value == "E":
                # We have found our end coordinate. Log it
                end_point = (x, y)
            elif value == "a":
                # We have found other possible starting points for Part 2. Log it
                a_starting_nodes.append((x, y))

            # Add the node to the dictionary
            nodes_dict[(x, y)] = ascii_lowercase.index(value) if value in ascii_lowercase else edge_cases[value]

    return nodes_dict, start_point, end_point, a_starting_nodes


def get_neighbours(current_node, nodes_dict):
    # print("Getting Neighbours for: ", current_node)

    # Yeild the neighbours for the current node 
    # Only yeild neighbours up, down, left and right
    # We will not yeild diagonals

    neighbours = ((1,0), (-1,0), (0,1), (0,-1))

    # Determine the boundry of the input grid
    max_Y, max_X = max(nodes_dict)

    for dx, dy in neighbours:
        # Get the new coordinates
        new_x = current_node[0] + dx
        new_y = current_node[1] + dy

        # print(f"Checking neighbour {new_x},{new_y}")

        # Check if the new coordinates are within the grid
        if (new_x, new_y) in nodes_dict:
            # print(f"Neighbour {new_x},{new_y} is in the grid")

            # Check that the new coordiates is less then 1 higher than the current node
            if nodes_dict[(new_x, new_y)] - nodes_dict[current_node] <= 1:
                # print(f"Yeilding neighbour {new_x},{new_y}")
                yield (new_x, new_y)

def part1(nodes_dict, start_point, end_point):
    
    visited = {start_point:0}
    queue = [start_point]

    while queue:
        # print(f"\nqueue: {queue}")
        current_node = queue.pop(0)
        # print(f"\nvisiting node {current_node}")

        current_step = visited[current_node]

        # Djikstra's algorithm
        for dx, dy  in get_neighbours(current_node, nodes_dict):   
            if (dx, dy) not in visited:
                visited[(dx, dy)] = current_step + 1

                # print(f"visited: {visited}")

                # Add the neighbour to the queue
                # print(f"Adding neighbour {dx},{dy} to the queue")
                queue.append((dx, dy))

                if (dx, dy) == end_point:
                    # print(f"Found end point {dx},{dy} in {visited[(dx, dy)]} steps")
                    
                    return visited[(dx, dy)]
            
    return 

def part2(nodes, a_starting_nodes, end_point):
    print("Part 2")

    min_steps = 9999999999999

    for start_point in a_starting_nodes:
        # print(f"Starting from {start_point}")
        steps = part1(nodes, start_point, end_point)

        if steps and steps < min_steps:
            min_steps = steps

    print(f"Min steps: {min_steps}")

    return


def main():
    # Work out the current day based on the current file name
    currentDay = os.path.basename(__file__).split('.')[0]
    print(currentDay)

    # Read in the input file to a list
    with open(input_file) as f:
        data = f.read().splitlines()

        nodes, start_point, end_point, a_starting_nodes = read_data_into_nodes_dictionary(data)

        print("Part 1")
        print(f"Part 1 steps {part1(nodes, start_point, end_point)}")

        part2(nodes, a_starting_nodes, end_point)

if __name__ == "__main__":
    main()
