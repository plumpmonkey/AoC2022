#!/usr/bin/env python

import os
import numpy as np
from functools import reduce


dirname = os.path.dirname(__file__)
input_file = os.path.join(dirname, 'input.txt')

def part1(orig_data):
    print("Part 1")

    # Read each line data into a numpy array splitting each character into a separate integer
    data = np.array([list(line) for line in orig_data], dtype=int)
            
    # Create a numpy array to hold the result
    visible_map = np.zeros(data.shape, dtype=int)
    
    # Get the size of the numpy array
    Y_Size = data.shape[0]
    X_Size = data.shape[1]

    print(f"X_Size: {X_Size}, Y_Size: {Y_Size}")

    # As we can see the edges,
    # set the first row, last row, first column and last column to 1 in visible_map
    visible_map[0, :] = 1
    visible_map[Y_Size - 1, :] = 1
    visible_map[:, 0] = 1
    visible_map[:, X_Size - 1] = 1

    # loop 4 times and rotate the data 90 degrees clockwise each time
    for i in range(4):
        print("Iteration: " + str(i))

        # Starting from row 1, column 1, loop through the data one row at a time and set the visible_map to 1 if the value is >= to the previous value
        blocked = False

        for y in range(1, Y_Size - 1):
            
            # Set the current highest value
            max_size = data[y,0] 

            for x in range(1, X_Size - 1):
                if data[y, x] > max_size:
                    max_size = data[y, x]
                    visible_map[y, x] = 1
                else:
                    pass

                # DEBUG - SHOW THE VALUES  
                # print(f"x: {x}, y: {y}, data[y, x]: {data[y, x]}, data[y, x - 1]: {data[y, x - 1]}, blocked: {blocked}")
                
        # print(data)
        # print(visible_map)

        # rotate data 90 degrees clockwise
        data = np.rot90(data, 1)
        visible_map = np.rot90(visible_map, 1)

    print("Final")
    
    print(f"data \n{data}")
    print(f"visability map \n{visible_map}")

    # Count the number of 1's in visible_map
    print(f"Count of the number of visible trees {np.count_nonzero(visible_map)}")
    return 


def part2(orig_data):
    print("Part 2")

    # Read each line data into a numpy array splitting each character into a separate integer
    data = np.array([list(line) for line in orig_data], dtype=int)

    # Get the size of the numpy array
    Y_Size = data.shape[0]
    X_Size = data.shape[1]

    print(f"X_Size: {X_Size}, Y_Size: {Y_Size}")

    # Create and array of 4 numpy arrays to hold the result of which trees are visible in each direction
    visible_map_array = [np.zeros(data.shape) for _ in range(4)]

    # Loop through the 4 directions
    for iteration, visible_map in enumerate(visible_map_array):
        grid = np.rot90(data, k=iteration)

        match iteration:
            case 0:
                print("Looking East")
            case 1:
                print("Looking North")
            case 2:
                print("Looking West")
            case 3:
                print("Looking South")

        print(f"grid \n{grid}")

        for row, (trees, visible) in enumerate(zip(grid, visible_map)):
            curr = 0

            print(f"\nrow: {row}, trees: {trees}")

            for col, height in enumerate(trees):
                if col == 0 or height > curr:
                    curr = height

                current_height = height

                counter = 0

                for i in trees[col+1:]:
                    counter += 1
                    if i >= current_height:
                        break
                visible[col] = counter

        print(f"visible_map \n{visible_map}")    


    visible_map_array = [np.rot90(map, k=k) for k, map in enumerate(visible_map_array)]

    print("\\nnFinal")
    for k, map in enumerate(visible_map_array):
        match k:
            case 0:
                print("Looking East")
            case 1:
                print("Looking North")
            case 2:
                print("Looking West")
            case 3:
                print("Looking South")
        print(f"Direction {k} \n{map}")

    print(np.max(reduce(np.multiply, visible_map_array)))

    return


def main():
    # Work out the current day based on the current file name
    currentDay = os.path.basename(__file__).split('.')[0]
    print(currentDay)

    # Read in the input file to a list
    with open(input_file) as f:
        data = f.read().splitlines()

        # part1(data)
        part2(data)

if __name__ == "__main__":
    main()
