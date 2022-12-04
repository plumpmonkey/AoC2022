#!/usr/bin/env python

import os

dirname = os.path.dirname(__file__)
input_file = os.path.join(dirname, 'input.txt')

def part1(data):
    print("Part 1")

    count = 0

    # Read data line by line
    for line in data:
        # Line is in the format of [2-4],6-8]. Split on the comma
        # to get the two ranges
        ranges = line.split(',')
        # Split the ranges on the dash to get the min and max
        range1 = ranges[0].split('-')
        range2 = ranges[1].split('-')

        # Convert the ranges to integers
        min1 = int(range1[0])
        max1 = int(range1[1])
        min2 = int(range2[0])
        max2 = int(range2[1])

        # is min1 and max1 in range2?
        if min1 >= min2 and min1 <= max2 and max1 >= min2 and max1 <= max2:
            print("range1 {} is in range2 {}".format(ranges[0], ranges[1]))
            count += 1

        # is min2 and max2 in range1?
        elif min2 >= min1 and min2 <= max1 and max2 >= min1 and max2 <= max1:
            print("range2 {} is in range1 {}".format(ranges[1], ranges[0]))
            count += 1
            
    # Show number of ranges that overlap
    print("Count: {}".format(count))

    return 


def part2(data):
    print("Part 2")

    count = 0

    # Read data line by line
    for line in data:
        # Line is in the format of [2-4],6-8]. Split on the comma
        # to get the two ranges
        ranges = line.split(',')

        # Split the ranges on the dash to get the min and max
        range1 = ranges[0].split('-')
        range2 = ranges[1].split('-')

        # Convert the ranges to integers
        min1 = int(range1[0])
        max1 = int(range1[1])
        min2 = int(range2[0])
        max2 = int(range2[1])

        # Do the rangers overlap each other?
        if max1 >= min2 and max2 >= min1:
            print("Ranges overlap {} {}".format(ranges[0], ranges[1]))
            count += 1        

    # Show number of ranges that overlap
    print("Count: {}".format(count))

    return

def main():
    # Work out the current day based on the current file name
    currentDay = os.path.basename(__file__).split('.')[0]
    print(currentDay)

    # Read in the input file to a list
    with open(input_file) as f:
        data = f.read().splitlines()

        part1(data)
        part2(data)

if __name__ == "__main__":
    main()
