#!/usr/bin/env python

import os


dirname = os.path.dirname(__file__)
input_file = os.path.join(dirname, 'input.txt')

def part1(data):
    print("Part 1")

    cycle_count = 0

    total = 0

    X = 1

    for instruction in data:
        # print(f"Instruction: {instruction}")

        # if the instruction is "noop", increment the cycle count
        if instruction == "noop":
            cycle_count += 1

            # If cycle count == 20 or 20 + cycle_count % 40 then print X
            if cycle_count == 20 or (cycle_count - 20) % 40 == 0:
                print(f"cycle_count {cycle_count}, X: {X}")
            
                # Signal strength is X * cycle count
                print(f"Signal strength: {X * cycle_count}")

                # Add the signal strength to a total
                total += X * cycle_count
            
        elif instruction[:4] == "addx":
            # get the value to add to X from the instruction. The value is split from the instruction by a space
            value = int(instruction.split(" ")[1])
            
            cycle_count += 1

            # If cycle count == 20 or 20 + cycle_count % 40 then print X
            if cycle_count == 20 or (cycle_count - 20) % 40 == 0:
                print(f"cycle_count {cycle_count}, X: {X}")
            
                # Signal strength is X * cycle count
                print(f"Signal strength: {X * cycle_count}")

                # Add the signal strength to a total
                total += X * cycle_count

            cycle_count += 1

            # If cycle count == 20 or 20 + cycle_count % 40 then print X
            if cycle_count == 20 or (cycle_count - 20) % 40 == 0:
                print(f"cycle_count {cycle_count}, X: {X}")
                
                # Signal strength is X * cycle count
                print(f"Signal strength: {X * cycle_count}")

                # Add the signal strength to a total
                total += X * cycle_count
                            
            # add the value to X
            X += value


    print(f"Total: {total}")

    return 


def part2(data):
    print("Part 2")

    CRT_ROWS = 6
    CRT_COLS = 40
    NUM_CYCLES = 240

    cycle_count = 0

    X = 1

    # Create a list with NUM_CYCLES elements
    X_list = [0] * (NUM_CYCLES + 1)
        
    # For Part 2, we will create a list with the value of X at each cycle,
    # then we can parse the list to print to the screen.
    for instruction in data:
        # print(f"Instruction: {instruction}")

        if instruction == "noop":
            X_list[cycle_count] = X
            cycle_count += 1

            # print(f"X_list[{cycle_count}]: {X_list[cycle_count]}")

        elif instruction[:4] == "addx":
            X_list[cycle_count] = X
            cycle_count += 1

            # print(f"X_list[{cycle_count}]: {X_list[cycle_count]}")

            # get the value to add to X from the instruction. The value is split from the instruction by a space
            value = int(instruction.split(" ")[1])

            X_list[cycle_count] = X

            # print(f"X_list[{cycle_count}]: {X_list[cycle_count]}")
            
            cycle_count += 1

            X += value

    # print(X_list)

    # Print to the screen
    for row in range(CRT_ROWS):
        for pixel in range(CRT_COLS):

            # We must print a # if the current X value +/-1 is equal to the current pixel value
            # 
            # ((row*40) + pixel) gives us an index into the X_list
            # 
            # if we then take the signal value, and subtract the current pixel value, 
            # then if it is -1, 0 or 1, we match our criteria of +/- 1.
            # Therefore, if we abs() the result, we can check if it is <= 1
            #
            if abs(X_list[row*40 + pixel] - int(pixel)) <= 1:
                char_to_print = '#'
            else:
                # Print a space (not a dot -for readability)
                char_to_print = ' '

            # Print the character, do not print a new line
            print(char_to_print, end='')

        print()
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
