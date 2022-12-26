#!/usr/bin/env python
import os
import sys

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


def get_monkeyA_and_monkeyB_values(human_value, monkey_dictionary):

    # Set the value of 'humn' to the value passed in
    monkey_dictionary['humn'] = human_value

    # Calculate the value of the monkeyA and monkeyB
    monkeyA_value = calculate_monkey_value(monkey_dictionary, monkey_dictionary['root'][0])
    monkeyB_value = calculate_monkey_value(monkey_dictionary, monkey_dictionary['root'][2])

    print(f"MonkeyA {int(monkeyA_value)} , MonkeyB {int(monkeyB_value)}")

    return monkeyA_value, monkeyB_value

def part2(data):
    print("Part 2")

    # Parse the data into a dictionary
    monkey_dictionary = parse_data(data)

    iterations = 0

    # Find initial difference between monkeyA and monkeyB
    monkeyA_value, monkeyB_value = get_monkeyA_and_monkeyB_values(monkey_dictionary['humn'], monkey_dictionary)

    diff = monkeyA_value - monkeyB_value
    print(f"Initial diff {int(diff)}, monkeyA {int(monkeyA_value)}, monkeyB {int(monkeyB_value)}")

    low = 0
    high = sys.maxsize
    modifier = int(low+high / 2)
    
    increment = True
    while True:
        iterations += 1

        # Change the human value by the modifier
        monkey_dictionary['humn'] += int(modifier + 1) if increment else int(-modifier - 1)
        print(f"Human value {monkey_dictionary['humn']}, modifier {modifier}, increment {increment}")

        monkeyA_value, monkeyB_value = get_monkeyA_and_monkeyB_values(monkey_dictionary['humn'], monkey_dictionary)

        # We have found the final value, quit
        if monkeyA_value == monkeyB_value:
            print(f"Human value {monkey_dictionary['humn']}")
            break

        new_diff = monkeyA_value - monkeyB_value

        # If the new difference is greater than the old difference, we have overshot the target
        # So reverse the direction and reduce the modifier
        if abs(new_diff) > abs(diff):
            increment = not increment
            modifier /= 4
                    
        diff = new_diff

    # Solved in iterations
    print(f"Solved in {iterations} iterations")
        
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
