#!/usr/bin/env python

import os

dirname = os.path.dirname(__file__)
input_file = os.path.join(dirname, 'sample.txt')

def part1(data):
    print("Part 1")

    
    return 


def main():
    # Work out the current day based on the current file name
    currentDay = os.path.basename(__file__).split('.')[0]
    print(currentDay)

    # Read in the input file to a list
    with open(input_file) as f:
        data = f.read().splitlines()

        file_system = {}
        directory_path = []
        current_directory = {}

        for line in data:
            # If line == "$ cd /" then directory path = []
            if line == "$ cd /":
                directory_path = []
            # If line == "$ cd .." then directory path = directory_path[:-1]
            elif line == "$ cd ..":
                directory_path.pop()
            # If line == "$ cd <directory>" then directory path = directory_path + [line.split(' ')[-1]]
            elif line.split(' ')[0] == "$" and line.split(' ')[1] == "cd":
                directory_path.append(line.split(' ')[-1])

            print(directory_path)



        part1(data)

if __name__ == "__main__":
    main()
