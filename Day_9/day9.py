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


def part1and2(data):
    print("Part 1 and 2")

    # Define head and tail starting positions
    head = [0,0]

    # Take a copy of the head list to use as the tail
    tail = head.copy()
    
    # Part2 - model tail_two through tail_nine
    tail_two = head.copy()
    tail_three = head.copy()
    tail_four = head.copy()
    tail_five = head.copy()
    tail_six = head.copy()
    tail_seven = head.copy()
    tail_eight = head.copy()
    tail_nine = head.copy()

    # Part 1 - Monitor tail position
    tail_visited = set()

    # Part 2 - Monitor tail 9 positions
    tail_nine_visited = set()


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
          
            # Part 1 - Move the tail based on the head position
            move_tail(head, tail)

            # Add the tail position to the set of visited positions
            tail_visited.add((tail[0], tail[1]))

            # Part 2 - move tail two through 9 based on the tail element before it
            move_tail(tail, tail_two)
            move_tail(tail_two, tail_three)
            move_tail(tail_three, tail_four)
            move_tail(tail_four, tail_five)
            move_tail(tail_five, tail_six)
            move_tail(tail_six, tail_seven)
            move_tail(tail_seven, tail_eight)
            move_tail(tail_eight, tail_nine)

            # Add the tail_nine position to the set of visited positions
            tail_nine_visited.add((tail_nine[0], tail_nine[1]))

            # # Log the head position in the grid
            # grid[head[1]][head[0]] = "H"
            # # print(f"HEAD: {head[0]+int(START_X)}, {head[1]}")

            # # Log the tail position in the grid
            # grid[tail[1]][tail[0]] = "T"
    
            # # Render the grid
            # render_grid(grid)
            
    # print(f"tail_visited = {tail_visited}")
    print(f"Part 1 - Number of visited positions = {len(tail_visited)}")
    print(f"Part 2 - Number of visited tail_nine positions = {len(tail_nine_visited)}")

    return

def move_tail(head, tail):
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

def main():
    # Work out the current day based on the current file name
    currentDay = os.path.basename(__file__).split('.')[0]
    print(currentDay)

    # Read in the input file to a list
    with open(input_file) as f:
        data = f.read().splitlines()

        part1and2(data)

if __name__ == "__main__":
    main()
