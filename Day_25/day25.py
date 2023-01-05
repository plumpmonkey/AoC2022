#!/usr/bin/env python
import os

dirname = os.path.dirname(__file__)
input_file = os.path.join(dirname, 'input.txt')

# Create a dictionary to convert between the SNAFU number system and the decimal number system and vice versa
snafu_decimal_conversion = {
    '2': 2,
    '1': 1,
    '0': 0,
    '-' : -1,
    '=' : -2,

    2 : '2',
    1 : '1',
    0 : '0',
    -1 : '-',
    -2 : '=' }


def decimal_to_snafu(decimal_value):

    # Convert the decimal value to a text string SNAFU value.
    # 
    # The SNAFU number system is base 5, but with a twist. The digits are 2, 1, 0, -, =
    #
    # The column 
    snafu_value = ""
    
    carry_value = 0
    column = 0

    while decimal_value != 0 or carry_value:
        # We carried one from the previous column, so add it to the current column
        if carry_value:
            decimal_value += carry_value

        # Get the remainder of the decimal value divided by base 5
        remainder = decimal_value % 5

        # Divide the decimal value by base 5 and floor the output
        decimal_value = decimal_value // 5

        # If the remainder is greater than 2, then we need to carry a 1 to the next column
        # and subtract 5 from the remainder.
        if remainder > 2:
            remainder -= 5
            carry_value = 1
        else:
            # No carry required
            carry_value = 0

        # print(f"remainder: {remainder}, decimal_value: {decimal_value}, snafu_value: {snafu_value}")

        # Convert and add the SNAFU character to the start of the string
        snafu_value = snafu_decimal_conversion[remainder] + snafu_value

    # print("SNAFU value: ", snafu_value)

    return snafu_value


def snafu_to_decimal(snafu_value):

    decimal_value = 0

    # For each line, loop through each character in the line starting at the right 
    # end of the line (units) and work left.
    # 
    # Using enumerate, the column index (starting at 0 for the units), gives
    # us the power value. The power value is the (column number * 5) as we are in base 5
    for power, character in enumerate(snafu_value[::-1]):
        
        # print(f"character: {character}, column: {power}, power: {5**power}, decimal: {5 ** power * snafu_decimal_conversion[character]}") 

        decimal_value += 5 ** power * snafu_decimal_conversion[character]

    return decimal_value
        
def part1(data):
    print("Part 1")

    final_sum = 0
    # Loop through each line in the input file
    for line in data:
        # print("\nSNAFU line: ", line)

        # Convert each snafu line to a decimal value
        decimal_value = snafu_to_decimal(line)

        # print("Decimal value: ", decimal_value)
            
        # Add the decimal value to the final sum
        final_sum += decimal_value

    # Print out the Decimal value of the final sum
    print(f"Final Sum of Decimal values: {final_sum}")
    
    # Convert the final sum to SNAFU
    summed_snafu = decimal_to_snafu(final_sum)

    # Print out the SNAFU value of the final sum
    print(f"Summed SNAFU: {summed_snafu}")
    
    return 


def main():
    # Work out the current day based on the current file name
    currentDay = os.path.basename(__file__).split('.')[0]
    print(currentDay)

    # Read in the input file to a list
    with open(input_file) as f:
        data = f.read().splitlines()

        part1(data)

if __name__ == "__main__":
    main()
