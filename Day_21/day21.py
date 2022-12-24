#!/usr/bin/env python
import os
import re

dirname = os.path.dirname(__file__)
input_file = os.path.join(dirname, 'input.txt')

def parse_data(data):
    # Create a dictionary of the data
    monkey_dictionary = {}

    # Loop through the data and add it to the dictionary
    for line in data:
        # Split the line into monkey and value.
        # Value is either an integer, or two monkeys and an operator (monkeyA +-/* monkeyB)
        monkey, value = line.split(': ')

        match value.split():
            case [integer]:                  
                # If the value is an integer, add it to the dictionary
                monkey_dictionary[monkey] = int(integer)

            case [monkeyA, operator, monkeyB]:
                # If the value is an operation, add it to the dictionary
                monkey_dictionary[monkey] = [monkeyA, operator, monkeyB]

    return monkey_dictionary


def calculate_monkey_value(monkey_dictionary, monkey):
    # If the monkey value is an integer and already known, return it
    if type(monkey_dictionary[monkey]) == int:
        return monkey_dictionary[monkey]

    # If the monkey is an operation, recursively calculate the value
    else:
        # Get the operation
        monkeyA, operator, monkeyB = monkey_dictionary[monkey]

        # Get the values of the monkeys
        monkeyA_value = calculate_monkey_value(monkey_dictionary, monkeyA)
        monkeyB_value = calculate_monkey_value(monkey_dictionary, monkeyB)

        # Calculate the value of the operation
        if operator == '+':
            return monkeyA_value + monkeyB_value   
        elif operator == '-':
            return monkeyA_value - monkeyB_value
        elif operator == '*':
            return monkeyA_value * monkeyB_value
        elif operator == '/':
            return monkeyA_value / monkeyB_value

        # If the operator is not recognised, raise an exception
        # This should never happen
        else:
            raise Exception(f"ERROR: Monkey calculation error {monkey}: {monkey_dictionary[monkey]}")
        

def part1(data):
    print("Part 1")

    # Parse the data into a dictionary
    monkey_dictionary = parse_data(data)
        
    # Calculate the value of the monkey 'root'
    print(int(calculate_monkey_value(monkey_dictionary, 'root')))

    return


def part2(data):
    print("Part 2")

    # Parse the data into a dictionary
    monkey_dictionary = parse_data(data)

    # Change the value of the monkey 'humn' to None
    monkey_dictionary['humn'] = None
    
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
