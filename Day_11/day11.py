#!/usr/bin/env python
import os
from tqdm import tqdm
from enum import Enum
from collections import Counter

DEBUG = True

dirname = os.path.dirname(__file__)
input_file = os.path.join(dirname, 'input.txt')

# Define the colours used for text printing
class Colours(Enum):
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BOLD = "\033[1m"
    NORMAL = "\033[0m"


class Monkey:
    def __init__(self, monkey_id: int, items_list: list, operator: str, divisible_value: int, true_monkey: int, false_monkey: int ):
        self.monkey_id = monkey_id
        self.items_list = items_list
        self.operator = operator
        self.divisible_value = divisible_value
        self.true_monkey = true_monkey
        self.false_monkey = false_monkey
        self.inspected_count = 0

    def add_item(self, item):
        self.items_list.append(item)

    def remove_item(self, item):
        self.items_list.remove(item)    

    def __repr__(self) -> str:
        return  f"Monkey ID: {self.monkey_id}, Items: {self.items_list}, Operator: {self.operator}, Divisible Value: {self.divisible_value}, Throw True: {self.true_monkey}, Throw False: {self.false_monkey}"


    def inspect(self, monkey_dict: dict):

        # Pop the first item off the list
        item = int(self.items_list.pop(0))

        # Store the original worry level of this item incase we need to use the "old" value in the operation
        original_worry_level = item
        
        if DEBUG:
            print(f"{Colours.YELLOW.value} \nMonkey {self.monkey_id} is inspecting item {item} {Colours.NORMAL.value}")

        # Increment the inspection count
        self.inspected_count += 1

        # The operator could be "new = old <something> OLD"
        # if the last part of the operator is "old", then we need to use the original worry level
        if self.operator[1] == "old":
            rhs_operator = item
        else:
            rhs_operator = int(self.operator[1])

        # For clariry, rename the operator to the lhs and rhs
        lhs_operator = self.operator[0]

        # Perform the operation
        if lhs_operator == "*":
            item *= rhs_operator
        elif lhs_operator == "+":
            item += rhs_operator
        else:
            print(f"Unknown operator {lhs_operator}")
      
        if DEBUG:
            print(f"Monkey {self.monkey_id} has inspected item {original_worry_level}, performing operation {lhs_operator} {rhs_operator} and it is now {item}")

        # The item has now been inspected. The monkey gets bored so divide by 3 and floor the result
        item = int(item) // 3

        if DEBUG:
            print(f"Monkey {self.monkey_id} is bored so divides the worry level by 3 and it is now {item}")

        # Determine if item is divisible by the divisible value
        if item % self.divisible_value == 0:
            # True
            if DEBUG:
                print(f"Current worry level is divisible by {self.divisible_value}")
            monkey_dict[self.true_monkey].add_item(item)

        else:  
            # False
            if DEBUG:
                print(f"Current worry level is not divisible by {self.divisible_value}")
            monkey_dict[self.false_monkey].add_item(item)   

        if DEBUG:
            print(f"Monkey {self.monkey_id} has thrown item {item} to monkey {self.true_monkey if item % self.divisible_value == 0 else self.false_monkey}")
            
        

def create_monkeys(data):
    # Split the data into blocks separated by a blank line. EG.
    #
    # Monkey 0:
    #   Starting items: 79, 98
    #   Operation: new = old * 19
    #   Test: divisible by 23
    #     If true: throw to monkey 2
    #     If false: throw to monkey 3
    #

    # Create a dictionary to hold the monkeys
    monkeys= {}

    blocks = data.split('\n\n')

    items = []
    operator = ""
    divisible_value = 0
    true_monkey = 0
    false_monkey = 0
    
    # Loop through each monkey block
    for block in blocks:
        # Parse each line in the block
        for line in block.splitlines():
            if line.startswith('Monkey'):
                # Monkey 0:
                monkey_id = int(line.split(' ')[1].strip(':'))

            elif 'Starting items' in line:
                # Starting items: 79, 98
                items = line.split(':')[1].strip().split(',')

            elif 'Operation' in line:
                # Operation: new = old * 19
                operator = line.split(" ")

                # We do not care about "Operation: new = old", grab the last two parts 
                # only by deleting the first 6 (including the indent)
                del operator[:6]

            elif 'Test' in line:
                # Test: divisible by 23
                divisible_value = int(line.split(':')[1].strip().split(' ')[2])

            elif 'If true' in line:
                # If true: throw to monkey 2
                true_monkey = int(line.split(':')[1].strip().split(' ')[3])

            elif 'If false' in line:
                # If false: throw to monkey 3
                false_monkey = int(line.split(':')[1].strip().split(' ')[3])

            else:
                print(f"Unknown line: {line}")

        # Create a new monkey object
        monkey = Monkey(monkey_id, items, operator, divisible_value, true_monkey, false_monkey)

        monkeys[monkey_id] = monkey

    return monkeys
    
    
def part1(data):
    print("Part 1")

    monkey_dict = create_monkeys(data)

    print(monkey_dict)

    # run for 20 rounds
    for i in range(20):
        print(f"Round {i+1}")
        for monkey in monkey_dict.values():
            while monkey.items_list:
                monkey.inspect(monkey_dict)

        # show the monkey items
        if DEBUG:
            print(f"\nAt the end of round {i+1}")
            
            for monkey in monkey_dict.values():
                print(f"Monkey {monkey.monkey_id} has {(monkey.items_list)} items")

            print()

        # Show the monkey inspection counts
        inspections = []
        for monkey in monkey_dict.values():
            inspections.append(monkey.inspected_count)
            print(f"Monkey {monkey.monkey_id} has inspected {monkey.inspected_count} items")

        # Sort the inspections list
        inspections.sort()

        # Multiply the last two (highest) values  in the list
        print(f"Multiplying the last two values in the list: {inspections[-1]} * {inspections[-2]} = {inspections[-1] * inspections[-2]}")

    return 


def part2(data):
    print("Part 2")

    return


def main():
    # Work out the current day based on the current file name
    currentDay = os.path.basename(__file__).split('.')[0]
    print(currentDay)

    # Read in the input file to a list
    with open(input_file) as f:
        data = f.read()

        part1(data)
        part2(data)

if __name__ == "__main__":
    main()
