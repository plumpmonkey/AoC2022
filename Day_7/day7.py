#!/usr/bin/env python

import os
from collections import defaultdict


dirname = os.path.dirname(__file__)
input_file = os.path.join(dirname, 'input.txt')

def part1(directory_sizes):
    print("Part 1")

    # Loop through directory sizes and sum all the values of all directories < 1000000
    total_size = 0
    for directory, size in directory_sizes.items():
        if size <= 100000:
            total_size += size

    print(total_size)

    return 


def part2(directory_sizes):
    print("Part 2")

    free_space = 70000000 - directory_sizes['/']
    print("Free space: " + str(free_space))
    
    space_needed = 30000000 - free_space
    print("Space Needed == 30000000 - " + str(free_space) + " = " + str(space_needed))

    # Sort the directory sizes by size
    sorted_directory_sizes = sorted(directory_sizes.items(), key=lambda x: x[1], reverse=False)

    # Loop through the sorted directory sizes and find the first directory that is >= 30000000
    for directory, size in sorted_directory_sizes:
        if size >= space_needed:
            print(size)
            break

    return


def main():
    # Work out the current day based on the current file name
    currentDay = os.path.basename(__file__).split('.')[0]
    print(currentDay)

    # Read in the input file to a list
    with open(input_file) as f:
        data = f.read().splitlines()

            # Hold in a dictionary the size of each directory
        directory_sizes = defaultdict(int)

        # Create a list to store the directory path
        directory_path = ['/']

        # Create a variable to store the current directory
        current_directory = {'/'}

        for line in data:
            # If line == "$ cd /" then directory path = []
            if line == "$ cd /":
                directory_path = ['/']
            # If line == "$ cd .." then directory path = directory_path[:-1]
            elif line == "$ cd ..":
                # Remove last element from directory path
                directory_path.pop()

                if directory_path:
                    current_directory = directory_path[-1]
                    # print("Changed directory to: " + current_directory)
                else:
                    current_directory = "/"
                    # print("Changed directory to: " + current_directory)


            # If line == "$ cd <directory>" then directory path = directory_path + [line.split(' ')[-1]]
            elif line.split(' ')[0] == "$" and line.split(' ')[1] == "cd":
                current_directory = line.split(' ')[2]
                directory_path.append(current_directory)
                # print("Changed directory to: " + current_directory)
            elif line == "$ ls":
                #Ignore - does nothing
                pass
            elif "dir" in line:
                # Telling us there is a new directory called <directory>. We dont need to do anything with this
                pass
            else:
                # split the line into an integer and a string split by a space
                size, file_name = line.split(' ')
                
                # Convert the size to an integer
                size = int(size)
                
                for i in range(len(directory_path)):
                    # print("Adding " + str(size) + " to " + '/'.join(directory_path[:i+1]))
                    directory_sizes['/'.join(directory_path[:i+1])] += size

        part1(directory_sizes)
        part2(directory_sizes)

if __name__ == "__main__":
    main()
