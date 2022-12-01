#!/usr/bin/env python

import os

dirname = os.path.dirname(__file__)
inputfile = os.path.join(dirname, 'input.txt')

def part1(data):
    # Need to find out the elf with the highest value
    print("Part 1")

    # Default calorie count to zero
    calorie_count = 0

    # Highest calorie count so far
    highest_calorie_count = 0

    for line in range(1,len(data)):
        if(data[line]):
            # Not a blank line, add to calorie_count
            calorie_count += int(data[line])
        else:
            # Blank line, 
            if calorie_count > highest_calorie_count:
                highest_calorie_count = calorie_count

            # Reset calorie_count
            calorie_count = 0     

    print("Highest calorie count: {}".format(highest_calorie_count))

    return highest_calorie_count


def part2(data):
    # Need to find the top three elves
    print("Part 2")

    # Default calorie count to zero
    calorie_count = 0

    # Blank list for each elf to store their calorie count
    elf_calorie_count = []

    for line in range(1,len(data)):
        if(data[line]):
            # Not a blank line, add to calorie_count
            calorie_count += int(data[line])
        else:
            # Blank line, 
            elf_calorie_count.append(calorie_count)

            # Reset calorie_count
            calorie_count = 0     

    # Sort the list
    elf_calorie_count.sort()

    # Get the top three
    top_three = elf_calorie_count[-3:]

    # Print the top three
    print("Top three elves: {}".format(top_three))

    # total the top three
    total = sum(top_three)
    print("Total: {}".format(total))
    
    return

def main():
    # Work out the current day based on the current directory name
    currentDay = os.path.basename(__file__).split('.')[0]
    print(currentDay)

    with open(inputfile) as f:
        data = f.read().splitlines()

        part1(data)
        part2(data)

if __name__ == "__main__":
    main()
