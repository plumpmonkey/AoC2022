#!/usr/bin/env python
import os
import numpy as np
import pygame
from pygame.locals import *


dirname = os.path.dirname(__file__)
input_file = os.path.join(dirname, 'input.txt')

ROCK = '#'
SAND = 'o'
EMPTY = '.'

# Model the sand as a particle that falls down the cave in its own class
class SandParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.falling = True

    def __str__(self):
        return f"SandParticle({self.x}, {self.y})"

    def __repr__(self):
        return self.__str__()

    def moveParticle(self, cave):
        # print(f"SandParticle.move({self.x}, {self.y})")
        # print(f"SandParticle.move: Falling: {self.falling}, Stopped: {self.stopped}")

        # If we are falling, then we need to check if we can move down
        if cave[self.y + 1, self.x] == EMPTY:
            # We can move down
            self.y += 1
            return self.falling

        # We are falling, but we cannot move down. Check if we can move left or right
        if cave[self.y + 1, self.x - 1] == EMPTY:
            # We can move left
            self.x -= 1
            return self.falling

        if cave[self.y + 1, self.x + 1] == EMPTY:
            # We can move right
            self.x += 1
            return self.falling

        # We cannot move down, left or right. We are stopped
        self.falling = False
        
        return self.falling

    def drawParticle(self, scale, surface):
        # sand colour is yellow
        sandColour = (255, 255, 0)

        # Draw the particle on the surface
        pygame.draw.rect(surface, sandColour, pygame.Rect(self.x * scale, self.y * scale, scale, scale))


# Work out the points in the line between the start and end points
def points_in_line(x1, y1, x2, y2):
    xrange = range(x1, x2 + 1) if x2 >= x1 else range(x1, x2 - 1, -1)
    yrange = range(y1, y2 + 1) if y2 >= y1 else range(y1, y2 - 1, -1)
    
    # print(f"xrange: {xrange}")
    # print(f"yrange: {yrange}")

    return [(x, y) for x in xrange for y in yrange]


# find the min and max x and y values in rocks
def find_min_max(rocks):
    min_x = min_y = 999999999
    max_x = max_y = 0
    for start, end in rocks:
        min_x = min(min_x, int(start[0]), int(end[0]))
        min_y = min(min_y, int(start[1]), int(end[1]))
        max_x = max(max_x, int(start[0]), int(end[0]))
        max_y = max(max_y, int(start[1]), int(end[1]))
    return min_x, min_y, max_x, max_y


def draw_ascii_cave(cave):
    for row in cave:
        print(''.join(row))
    return


def drawCave(surface, scale, cave):
    
    # Fill the background with black
    surface.fill((0, 0, 0))

    # rock colour is grey
    rockColour = (125, 125, 125)

    # sand colour is yellow
    sandColour = (255, 255, 0)

    # determine max x and y values from np array cave
    max_y = cave.shape[0]
    max_x = cave.shape[1]

    # Loop through the cave and draw the rocks and sand
    for y in range(0, max_y):
        for x in range(0, max_x):    
            if cave[y, x] == ROCK:
                pygame.draw.rect(surface, rockColour, pygame.Rect(x * scale, y * scale, scale, scale))
            elif cave[y, x] == SAND:
                pygame.draw.rect(surface, sandColour, pygame.Rect(x * scale, y * scale, scale, scale))

    # Draw a block to show where the sand is originating from in red
    pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(500 * scale, 0, scale, scale))

    return 

# Input data is in the format
# 
# 512,106 -> 512,108 -> 505,108 -> 505,114 -> 518,114 -> 518,108 -> 516,108 -> 516,106
# 532,129 -> 537,129
# 501,16 -> 506,16
# 
# So we need to find the min and max x and y values and create a grid of that size
# Then we need to fill in the grid with rocks and sand
def read_data(data):
    # Read in the data and return a list of points for each rock
    rocks = []

    for line in data:
        print('')

        # Split the line into a list of coordinates
        coords_list = line.split(' -> ')
        
        print(coords_list)

        # Create a list of tuples of start and end points for each rock.
        for i in range(0, len(coords_list) - 1):
            start = coords_list[i].split(',')
            end = coords_list[i + 1].split(',')
            rocks.append((start, end))

    # Defining our cave size. We need to find the min and max x and y values from the rocks
    # and then round them down to the nearest 100 and up to the nearest 100

    min_x, min_y, max_x, max_y = find_min_max(rocks)

    print(f"min_x: {min_x}, min_y: {min_y}, max_x: {max_x}, max_y: {max_y}")

    # round down min_x and min_y to nearest 100
    rounded_min_x = min_x - (min_x % 100)
    rounded_min_y = min_y - (min_y % 100)

    # round up max_x and max_y to nearest 100
    rounded_max_x = max_x + (100 - (max_x % 100))
    rounded_max_y = max_y + (100 - (max_y % 100))
    
    print(f"rounded_min_x: {rounded_min_x}, rounded_min_y: {rounded_min_y}, rounded_max_x: {rounded_max_x}, rounded_max_y: {rounded_max_y}")

    # X needs to be x2 for part 2
    cave = np.full((max_y+20, (max_x+3) * 2), EMPTY)

    print(cave.shape)

    # Fill in the cave with rocks
    for (start, end) in rocks:
        points = points_in_line(int(start[0]), int(start[1]), int(end[0]), int(end[1]))
        for point in points:
            cave[point[1], point[0]] = ROCK


    return cave, max_y


def part1(data):
    print("Part 1")

    scale = 3

    cave, cave_bottom = read_data(data)

    surface = pygame.display.set_mode((cave.shape[1] * scale, cave.shape[0] * scale + 100))

    # keep a log of the number of grains of sand we have
    sand_count = 0

    below_floor = False

    while not below_floor:
        pygame.event.pump()

        # Create sand particles one at a time and loop until the sand is below the bottom of the cave
    
        sandGrain = SandParticle(500, 0)

        # Whilst the sand is moving in the cave, draw frame by frame
        while sandGrain.falling:
            # Delay for drawing
            # pygame.time.wait(10)

            # Draw the base cave and rocks
            # drawCave(surface, scale, cave)

            # Move the sand particle 1 step
            sandGrain.moveParticle(cave)

            # Draw the sand particle
            sandGrain.drawParticle(scale, surface)
    
            # Flip the display
            # pygame.display.flip()

            if sandGrain.y > cave_bottom:
                below_floor = True
                sandGrain.falling = False

        # Sand is at rest. Add it to the cave
        cave[sandGrain.y, sandGrain.x] = SAND

        # Increment the sand count
        sand_count += 1

    # Remove the last grain of sand from the count
    sand_count -= 1

    drawCave(surface, scale, cave)
    pygame.display.flip()


    print(f"Sand count: {sand_count}")

    while True:
        event=pygame.event.wait()
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == KEYDOWN:
            break                
                
    return 


def part2(data):
    print("Part 2")

    # In part two, the cave bottom is 2 + the max y value. Fill the sand until 
    # it hits the bottom of the cave and stacks all the way up to the starting point
    # Then count the number of sand tiles

    scale = 3

    cave, cave_bottom = read_data(data)

    # Adjust cave bottom to be 2 rows above the max y value
    cave_bottom += 1

    surface = pygame.display.set_mode((cave.shape[1] * scale, cave.shape[0] * scale))

    print(f"Cave bottom: {cave_bottom}, cave shape: {cave.shape}")

    # keep a log of the number of grains of sand we have
    sand_count = 0

    reached_top = False

    while not reached_top:
        pygame.event.pump()

        # Create sand particles one at a time and loop until the sand is below the bottom of the cave
    
        sandGrain = SandParticle(500, 0)

        # Whilst the sand is moving in the cave, draw frame by frame
        while sandGrain.falling:
            # Delay for drawing
            # pygame.time.wait(10)

            # Draw the base cave and rocks
            # drawCave(surface, scale, cave)

            # Move the sand particle 1 step
            sandGrain.moveParticle(cave)

            # Draw the sand particle
            sandGrain.drawParticle(scale, surface)
    
            # Flip the display
            # pygame.display.flip()

            # If the sand has reached the bottom of the cave, stop it falling
            if sandGrain.y == cave_bottom:
                sandGrain.falling = False

            # If the sand has reached the top of the cave, stop it falling
            if sandGrain.y == 0 and sandGrain.x == 500:
                sandGrain.falling = False
            
        # Sand is at rest. Add it to the cave
        cave[sandGrain.y, sandGrain.x] = SAND

        # Increment the sand count
        sand_count += 1

        # # Draw the cave
        # drawCave(surface, scale, cave)
        # pygame.display.flip()

        # Check if the sand has reached the top of the cave
        if sandGrain.y == 0:
            reached_top = True

    # Count the number of sand tiles
    sand_tiles = np.count_nonzero(cave == SAND)

    print(f"Sand tiles: {sand_tiles}")
    print(f"Sand count: {sand_count}")

    drawCave(surface, scale, cave)
    pygame.display.flip()

    while True:
        event=pygame.event.wait()
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_f:
                print("foo!")

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
