#!/usr/bin/env python

import os
import sys

dirname = os.path.dirname(__file__)
input_file = os.path.join(dirname, 'input.txt')

def part1(crates, instructions):
    print("Part 1")

    crate_line = crates.splitlines()
    
    # extract every 4th character and place into a list starting at position 1
    crate_list = [crate_line[i][1::4] for i in range(len(crate_line))]

    # remove last element (the stack number)
    crate_list.pop()

    # change list from horizontal to vertical
    crate_list = list(map(list, zip(*crate_list)))

    # remove any ' ' characters in the create_list
    crate_list = [list(filter((' ').__ne__, crate)) for crate in crate_list]       

    # reverse the lists - top of stack is now at the right end of the list
    crate_list = [crate[::-1] for crate in crate_list]

    for line in instructions.splitlines():
        # split the instruction based on spaces
        instruction = line.split(' ')
        
        number_of_crates = int(instruction[1])
        from_stack = int(instruction[3]) - 1
        to_stack = int(instruction[5]) - 1

        for _ in range(number_of_crates):
            crate_list[to_stack].append(crate_list[from_stack].pop())

            # print(crate_list)

    # Pop the last element off each stack and combine into a string
    result = [stack.pop() for stack in crate_list]
    
    # convert list to string
    result = ''.join(result)
    print(result)    

    return 


def part2(crates, instructions):
    print("Part 2")

    crate_line = crates.splitlines()
    
    # extract every 4th character and place into a list starting at position 1
    crate_list = [crate_line[i][1::4] for i in range(len(crate_line))]

    # remove last element (the stack number)
    crate_list.pop()

    # change list from horizontal to vertical
    crate_list = list(map(list, zip(*crate_list)))

    # remove any ' ' characters in the create_list
    crate_list = [list(filter((' ').__ne__, crate)) for crate in crate_list]       

    # reverse the lists - top of stack is now at the right end of the list
    crate_list = [crate[::-1] for crate in crate_list]

    for line in instructions.splitlines():
        # split the instruction based on spaces
        instruction = line.split(' ')
        
        number_of_crates = int(instruction[1])
        from_stack = int(instruction[3]) - 1
        to_stack = int(instruction[5]) - 1

        # remove the number_of_creates from the from_stack and add to the to_stack preserving the order
        crate_list[to_stack] = crate_list[to_stack] + crate_list[from_stack][-number_of_crates:]
        crate_list[from_stack] = crate_list[from_stack][:-number_of_crates]
        
        # print(crate_list)

    # Pop the last element off each stack and combine into a string as long as list is not empty
    result = [stack.pop() for stack in crate_list if stack]
    
    # convert list to string
    result = ''.join(result)
    print(result)

    return

def main():
    # Work out the current day based on the current file name
    currentDay = os.path.basename(__file__).split('.')[0]
    print(currentDay)

    # Read in the input file to a list
    with open(input_file) as f:
        # Read in the input file to a list splitting the crates from the instructions.
        (crates, instructions) = f.read().split('\n\n')

    part1(crates, instructions)
    part2(crates, instructions)


if __name__ == "__main__":
    main()

