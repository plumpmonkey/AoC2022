#!/usr/bin/env python

import os

dirname = os.path.dirname(__file__)
input_file = os.path.join(dirname, 'input.txt')

priorities = {  'a' : 1, 'b' : 2, 'c' : 3, 'd' : 4, 'e' : 5, 'f' : 6, 'g' : 7, 'h' : 8, 'i' : 9, 'j' : 10, 'k' : 11, 'l' : 12, 'm' : 13, 'n' : 14, 'o' : 15, 'p' : 16, 'q' : 17, 'r' : 18, 's' : 19, 't' : 20, 'u' : 21, 'v' : 22, 'w' : 23, 'x' : 24, 'y' : 25, 'z' : 26, 
                'A' : 27, 'B' : 28, 'C' : 29, 'D' : 30, 'E' : 31, 'F' : 32, 'G' : 33, 'H' : 34, 'I' : 35, 'J' : 36, 'K' : 37, 'L' : 38, 'M' : 39, 'N' : 40, 'O' : 41, 'P' : 42, 'Q' : 43, 'R' : 44, 'S' : 45, 'T' : 46, 'U' : 47, 'V' : 48, 'W' : 49, 'X' : 50, 'Y' : 51, 'Z' : 52 }

def part1(data):
    print("Part 1")

    sum_of_priorities = 0

    for letters in data:

        # Split the variable letters into two havles
        first_half = letters[:len(letters)//2]
        second_half = letters[len(letters)//2:]
        
        # Determine which letter is in both first and second half#
        for letter in first_half:
            if letter in second_half:
                # print(letter)
                break
    
        # Add priority of letter to sum_of_priorities
        sum_of_priorities += priorities[letter]

    # Print the sum of priorities
    print(sum_of_priorities)

    return 


def part2(data):
    print("Part 2")

    sum_of_badge_priorities = 0

    # Read data three lines at a time
    for i in range(0, len(data), 3):
        # Determine which letter is in all three lines
        for letter in data[i]:
            if letter in data[i+1] and letter in data[i+2]:
                # print(letter)
                sum_of_badge_priorities += priorities[letter]

                break

    # Print the sum of bade priorities
    print(sum_of_badge_priorities)

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
