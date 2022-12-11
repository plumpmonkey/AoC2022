#!/usr/bin/env python

import os

HHEIGHT = 6
VHEIGHT = 6

dirname = os.path.dirname(__file__)
input_file = os.path.join(dirname, 'input.txt')

directions = {
    "R" : [1,0],
    "L" : [-1,0],
    "U" : [0,1],
    "D" : [0,-1]
}

def initialise_grid(visited={}):
    grid = []

    # print(f"visited: {visited}")

    for y in range(0, VHEIGHT):
        row = []
        for x in range(0, HHEIGHT):
            if (x,y) in visited:
                row.append("X")
            else:
                row.append(".")
        grid.append(row)

    return grid

def render_grid(grid):
    print("\n".join(["".join(row) for row in grid[::-1]]))


def part1(data):
    print("Part 1")

    # Define head and tail starting positions
    head = [0,0]

    # Take a copy of the head list to use as the tail
    tail = head.copy()
    
    tail_visited = set()

    # Initialise the grid for visulisation
    grid = initialise_grid()

    for step, action in enumerate(data):
        # Get the direction and number of steps, split by a space   
        direction, number_of_steps = action.split(' ')

        # print(f"step: {step}, direction: {direction}, number_of_steps: {number_of_steps}")

        # loop for the number of steps
        for i in range(int(number_of_steps)):
            # Initialise the grid with any old tail positions
            # grid = initialise_grid(tail_visited)

            # Update head position based on the direction
            head[0] += directions[direction][0]
            head[1] += directions[direction][1]
          
            
            delta_x = head[0] - tail[0]
            delta_y = head[1] - tail[1]

            # print(f"delta_x: {delta_x}, delta_y: {delta_y}")

            if abs(delta_x) > 1 or abs(delta_y) > 1:
                if delta_x >= 1:
                    tail[0] += 1
                elif delta_x <= -1:
                    tail[0] -= 1

                if delta_y >= 1:
                    tail[1] += 1
                elif delta_y <= -1:
                    tail[1] -= 1
                
           

            # print(f"tail: {tail}")

            # Add the tail position to the set of visited positions
            tail_visited.add((tail[0], tail[1]))

            # # Log the head position in the grid
            # grid[head[1]][head[0]] = "H"
            # # print(f"HEAD: {head[0]+int(START_X)}, {head[1]}")

            # # Log the tail position in the grid
            # grid[tail[1]][tail[0]] = "T"
    
            # # Render the grid
            # render_grid(grid)
            
    # print(f"tail_visited = {tail_visited}")
    print(f"Number of visited positions = {len(tail_visited)}")

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
        data = f.read().splitlines()

        part1(data)
        # part2(data)

if __name__ == "__main__":
    main()
