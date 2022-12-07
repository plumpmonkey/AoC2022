#!/usr/bin/env python

import os

dirname = os.path.dirname(__file__)
input_file = os.path.join(dirname, 'input.txt')

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

        for line in data:
            print(line[0])

        part1(data)

if __name__ == "__main__":
    main()
