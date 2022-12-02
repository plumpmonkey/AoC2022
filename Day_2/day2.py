#!/usr/bin/env python

import os

dirname = os.path.dirname(__file__)
input_file = os.path.join(dirname, 'input.txt')

class Result:
    LOSE = 0
    DRAW = 3
    WIN = 6
    
def part1(data):
    print("Part 1")

    score_sum = 0

    scores_dict = {"X": 1, "Y": 2, "Z" : 3}
     
    # Define a dictionary of the input data and return the result score
    # Results based on player 2 winning
    result_dict = {
        # Rock - Rock
        ( "A", "X" ): Result.DRAW,
        # Rock - Paper
        ( "A", "Y" ): Result.WIN,
        # Rock - Scissors
        ( "A", "Z" ): Result.LOSE,

        # Paper - Rock
        ( "B", "X" ): Result.LOSE,
        # Paper - Paper
        ( "B", "Y" ): Result.DRAW,
        # Paper - Scissors
        ( "B", "Z" ): Result.WIN,
        
        # Scissors - Rock
        ( "C", "X" ): Result.WIN,
        # Scissors - Paper
        ( "C", "Y" ): Result.LOSE,
        # Scissors - Scissors
        ( "C", "Z" ): Result.DRAW,
    }

    for line in data:
        # Split the line into two variables
        player1, player2 = line.split(' ')
        
        # Show the score for each player
        #print(player1, player2, result_dict[(player1, player2)])
        
        # Add the score to the total - Win/Draw/Lose + value for player 2 choice
        score_sum += result_dict[(player1, player2)] + scores_dict[player2]

    # Print the final score
    print(score_sum)

    return 


def part2(data):
    print("Part 2")

    # Default the score
    score_sum = 0

    # Set up three dictionaries for each of the possible player 1 outcomes
    win_scores = {'A': 2, 'B': 3, 'C': 1}
    draw_scores = {'A': 1, 'B': 2, 'C': 3}
    lose_scores = {'A': 3, 'B': 1, 'C': 2}

    # Player 2 entry denotes win/lose/draw (Z/X/Y), so we can use this to determine the score

    # Loop through the data
    for line in data:
        # Split the line into two variables
        player1, expected_result = line.split(' ')

        if expected_result == 'Z':      # Win - additional 6 points
            score_sum += win_scores[player1] + Result.WIN 
        elif expected_result == 'X':    # Lose - additional 0 points
            score_sum += lose_scores[player1] + Result.LOSE
        elif expected_result == 'Y':    # Draw - additional 1 points
            score_sum += draw_scores[player1] + Result.DRAW

    # Print the final score
    print(score_sum)

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
