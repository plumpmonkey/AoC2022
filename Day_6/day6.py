#!/usr/bin/env python

import os

dirname = os.path.dirname(__file__)
input_file = os.path.join(dirname, 'input.txt')

def part1and2(data, numberofunqiuechars):
    print("Part 1")

    for index in range(len(data[0]) - numberofunqiuechars + 1):
        substring  = data[0][index:index+numberofunqiuechars]

        # check if substring contains any duplicate characters
        if len(substring) == len(set(substring)):
            print(index + numberofunqiuechars)
            break

    return 


def main():
    # Work out the current day based on the current file name
    currentDay = os.path.basename(__file__).split('.')[0]
    print(currentDay)

    # Read in the input file to a list
    with open(input_file) as f:
        data = f.read().splitlines()

        part1and2(data, 4)
        part1and2(data, 14)

if __name__ == "__main__":
    main()
