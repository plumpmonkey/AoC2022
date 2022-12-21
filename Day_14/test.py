
# Importing the library
import pygame
from pygame.locals import *


class Sand:
    def __init__(self, startX, startY):
        self.x = startX
        self.y = startY

    def CheckNextMove(self, m):
        if m[self.x][self.y+1] == 0:
            self.y += 1
            return True
        elif m[self.x-1][self.y+1] == 0:
            self.x -= 1
            self.y += 1
            return True
        elif m[self.x+1][self.y+1] == 0:
            self.x += 1
            self.y += 1
            return True
        else:
            return False

    def draw(self, scale):
        c = (255, 255, 0)
        # draw the sand
        pygame.draw.rect(surface, c, pygame.Rect(
            self.x*scale, self.y*scale, scale, scale))


def drawMap(scale, xmax, ymax, m):

    rockColor = (125, 125, 125)
    sandColor = (255, 255, 0)

    for x in range(xmax):
        for y in range(ymax):
            if (m[x][y] == 1):
                # draw the rock
                pygame.draw.rect(surface, rockColor, pygame.Rect(
                    x*scale, y*scale, scale, scale))
                pygame.draw.rect(surface, (255, 255, 255), pygame.Rect(
                    x*scale, y*scale, scale, scale), width=1)
            elif (m[x][y] == 2):
                pygame.draw.rect(surface, sandColor, pygame.Rect(
                    x*scale, y*scale, scale, scale))


def drawSource():
    c = (255, 0, 0)
    pygame.draw.rect(surface, c, pygame.Rect(500*scale, 0*scale, scale, scale))


def buildRock(r, m):
    # break rock out into start and end co-ord pairs
    x = 0
    y = 1
    s = r[0]
    e = r[1]

    print("Building Rock: {} -> {}".format(r[0], r[1]))
    # is the rock x or y aligned?
    if s[x] == e[x]:
        print("X aligned")
        # X is same in both, so this segment is x aligned
        if (e[y] > s[y]):
            for i in range(s[y], e[y]+1):
                m[s[x]][i] = 1
        else:
            for i in range(e[y], s[y]+1):
                m[s[x]][i] = 1
    else:
        print("Y aligned")
        # y aligned
        if (e[x] > s[x]):
            for i in range(s[x], e[x]+1):
                m[i][s[y]] = 1
        else:
            for i in range(e[x], s[x]+1):
                m[i][s[y]] = 1


# Initializing Pygame and the font handler
pygame.init()
pygame.font.init()
myFont = pygame.font.SysFont('Arial', 10)


#### START OF DATA LOADING ####
file1 = open('Day_14/input.txt', 'r')

# read file input.txt into an array of strings
Lines = file1.readlines()

rocks = []
# loop through each line
for line in Lines:
    line = line.strip()

    pairs = line.split(' -> ')
    for c in range(len(pairs)-1):

        x, y = map(int, pairs[c].split(','))
        p = (x, y)

        x2, y2 = map(int, pairs[c+1].split(','))
        p2 = (x2, y2)

        # print("{0} -> {1}".format(p, p2))

        rocks.append((p, p2))

# print(rocks)


# Lets initialise a map to sort our rocks and sand
# we know the highest co-ords we need to deal with
# are max x: 544, max y: 164. So lets round them up
# to the nearest 100, and then create a blank
# array of that size, so that we can just arbitarily
# populate it as we process data
x = 700
y = 200
map = []
for i in range(x):
    map.append([0 for j in range(y)])

# print(map)

# for part 2 we need to add a floor going across the entire
# width, 2 cells below the lowest y co-ord, so as we're building
# the predefined rocks, lets work out what the Y floor needs to be
# then add an extra rock to form the floor
largestY = 0
for r in rocks:
    buildRock(r, map)
    if (r[0][1] > largestY):
        largestY = r[0][1]

    if (r[1][1] > largestY):
        largestY = r[1][1]

print("Largest Y: {}".format(largestY))
buildRock(((0, largestY+2), (x-1, largestY+2)), map)

# setup the display, now we know how big we need it
scale = 3
surface = pygame.display.set_mode((scale*x, scale*y))


# comes to rest at the source
count = 0
done = False
# keep pumping in sand
while done == False:
    testSand = Sand(500, 0)
    active = True

    while active == True:
        # pygame.time.wait(100)

        active = testSand.CheckNextMove(map)
        if active:
            testSand.draw(scale)

            # for part 2 - we leave the part 1 exit condition
            # in as a safety belt, but really this is an error
            # if this fires
            if (testSand.y > 190):
                active = False
                done = True
        else:

            surface.fill((0, 0, 0))

            # drawMap(scale, x, y, map)
            # drawSource()

            map[testSand.x][testSand.y] = 2
            count += 1
            print("Count:{}".format(count))

            # for part 2 our exit condition is when we hit the
            # source block with sand - i.e. when the pyramid fills
            # up from the floor all the way up to where the sand
            # falls from
            if (testSand.x == 500) and (testSand.y == 0):
                active = False
                done = True

            # flip the display for double buffering
            # pygame.display.flip()

print("Done")

drawMap(scale, x, y, map)
drawSource()

# flip the display for double buffering
pygame.display.flip()

pygame.event.clear()
while True:
    event = pygame.event.wait()
    if event.type == QUIT:
        pygame.quit()
        exit()
    elif event.type == KEYDOWN:
        if event.key == K_f:
            print("foo!")