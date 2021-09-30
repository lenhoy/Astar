#!/usr/bin/env python
# -*- coding: utf-8 -*-


import numpy as np
import pygame
import math
import pandas as pd
from queue import PriorityQueue

# Code based on https://www.youtube.com/watch?v=JtiK0DOeI4A&t=4122s


# Colors for classification of nodes
RED = (255, 0, 0)  # Interior/Closed nodes
GREEN = (0, 255, 0)  # Goal node
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)  # Unvisited node
BLACK = (0, 0, 0)  # Barrier
PURPLE = (128, 0, 128)  # Path
ORANGE = (255, 165, 0)  # Frontier
TURQUOISE = (64, 224, 208)  # Start node
GREY1 = (50, 50, 50)
GREY2 = (100, 100, 100)
GREY3 = (128, 128, 128)
GREY4 = (200, 200, 200)

# Create python enviroment based on handout Map


class Map:
    def __init__(self, task=1):
        """Initializing map values. Node Start has value 10 and Goal value 20

        Args:
            task (int, optional): Select task 1-5. Defaults to 1.
        """
        self.start_pos, self.goal_pos, self.end_goal_pos, self.path_to_map = self.fill_critical_positions(
            task)
        self.mapArray = self.read_map(self.path_to_map)
        self.tmp_cell_value = self.get_cell_value(self.goal_pos)
        self.set_cell_value(self.start_pos, 10)
        self.set_cell_value(self.goal_pos, 20)
        # print(self.mapArray)
        #self.tick_counter = 0

    def read_map(self, path):

        # Read in from mapfile
        df = pd.read_csv(path, index_col=None, header=None)

        # Convert to dataframe to numpy array
        mapdata = df.values

        return mapdata

    def fill_critical_positions(self, task=1):
        """Takes in task number and sets the right path to map and critical positions

        Args:
            task (int, optional): Task 1-5. Defaults to 1.

        Returns:
            touple: (start_pos->Array, goal_pos->Array, end_goal_pos->Array, path_to_map->Str)
        """
        if task == 1:
            start_pos = [27, 18]
            goal_pos = [40, 32]
            end_goal_pos = goal_pos
            path_to_map = 'Samfundet_map_1.csv'
        elif task == 2:
            start_pos = [40, 32]
            goal_pos = [8, 5]
            end_goal_pos = goal_pos
            path_to_map = 'Samfundet_map_1.csv'
        elif task == 3:
            start_pos = [28, 32]
            goal_pos = [6, 32]
            end_goal_pos = goal_pos
            path_to_map = 'Samfundet_map_2.csv'
        elif task == 4:
            start_pos = [28, 32]
            goal_pos = [6, 32]
            end_goal_pos = goal_pos
            path_to_map = 'Samfundet_map_Edgar_full.csv'
        elif task == 5:
            start_pos = [14, 18]
            goal_pos = [6, 36]
            end_goal_pos = [6, 7]
            path_to_map = 'Samfundet_map_2.csv'

        return start_pos, goal_pos, end_goal_pos, path_to_map

    def set_cell_value(self, pos, value):
        self.mapArray[pos[0], pos[1]] = value

    def get_cell_value(self, pos):
        return self.mapArray[pos[0], pos[1]]

    def get_map(self):
        """Returns a 2d array of values for the map nodes.
        Transposes the returnes array

        Returns:
            Array[[int]]: [description]
        """
        return self.mapArray

    def get_rows(self):
        return len(self.mapArray)

    def get_cols(self):
        return len(self.mapArray[0])

    def get_start_pos(self):
        return self.start_pos

    def get_goal_pos(self):
        return self.goal_pos


# object for nodes
class Node:
    def __init__(self, row, col, width, height, total_rows, total_cols):
        self.row = row
        self.col = col
        # Width/height here references to the drawn cubes
        # x, y are the coordinates taking the width of a cube into account
        # NOTE: make width=height for normal, rectangular cubes in the grid
        self.x = col * width
        self.y = row * height
        self.color = WHITE
        self.neighbours = []
        self.width = width
        self.height = height
        self.total_rows = total_rows
        self.total_cols = total_cols

    def get_pos(self):
        return self.row, self.col

    # Methods for checking status of node
    def is_interior(self):  # closed
        return self.color == RED

    def is_frontier(self):  # opened
        return self.color == ORANGE

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == BLUE

    def is_goal(self):
        return self.color == GREEN

    def is_flatGround(self):
        return self.color == WHITE

    # Methods for changing status of node
    def make_interior(self):
        self.color = RED

    def make_frontier(self):
        self.color = ORANGE

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = BLUE

    def make_goal(self):
        self.color = GREEN

    def make_flatGround(self):
        self.color = WHITE

    def make_path(self):
        self.color = PURPLE

    # Method to draw node/cube

    def draw(self, win):
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.height))

    def update_neighbours(self, grid):
        self.neighbours = []
        # DOWN
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbours.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbours.append(grid[self.row - 1][self.col])

        # RIGHT
        if self.col < self.total_cols - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbours.append(grid[self.row][self.col + 1])

        if self.row > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbours.append(grid[self.row][self.col - 1])

    # Less than, for comparing two nodes
    def __lt__(self, other):
        return False


def Astar(draw, grid, start, goal):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), goal.get_pos())

    open_set_hash = {start}  # check if the item is in the Priority Queue

    while not open_set.empty():
        for event in pygame.event.get():
            # method to quit
            if event.type == pygame.QUIT:
                pygame.quit()

        # get just the node from the open set (minimal object)
        current = open_set.get()[2]
        # make sure we don't have any duplicates
        open_set_hash.remove(current)

        if current == goal:
            return True

        for neighbour in current.neighbours:
            temp_g_score = g_score[current] + \
                1         # +1 because of neighbour

            if temp_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + \
                    h(neighbour.get_pos(), goal.get_pos())
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_frontier()

        draw()

        if current != start:
            current.make_interior()

    return False                # did not find a path


# Function for making grid of nodes
def make_grid(rows, cols, WIDTH):
    """Make a grid of nodes

    Args:
        rows (int): amount of rows
        cols (int): amount of cols
        WIDTH (int): the calculated width with regard to cube size
        height (int): the calculated height with regard to cube size
    Returns:
        2d Array: Array of node objects
    """
    grid = []
    gap = WIDTH // cols
    for i in range(rows):
        grid.append([])
        for j in range(cols):
            node = Node(i, j, gap, gap, rows, cols)
            grid[i].append(node)

    return grid

# Function for defining node colors based on CSV file / map


def color_nodes(grid, map):
    """Loop through grid and apply values from map file

    Args:
        grid (Array[[Node]]): [description]
        map (obj): [description]

    Returns:
        2d array: the grid with updated nodes
    """

    mapArray = map.get_map()  # gives 2d[int] array

    for gridRow, CSVRow in zip(grid, mapArray):  # Going through the rows
        for node_x, CSVvalue in zip(gridRow, CSVRow):  # Going through the columns
            color_node(node_x, CSVvalue)

    return grid


def color_node(node, value):
    """Applies the correct color value to a node

    Args:
        node (obj): node object
        value (int): value corresponding to a color

    Returns:
        [type]: [description]
    """

    if value == -1:  # Barrier
        node.make_barrier()
    elif value == 1:  # Flat
        node.make_flatGround()
    elif value == 2:  # Stairs
        pass
    elif value == 3:  # Packed Stairs
        pass
    elif value == 4:  # Packed room
        pass
    elif value == 10:  # Start
        node.make_start()
    elif value == 20:  # Goal
        node.make_goal()

# Function for drawing the gridlines


def draw_grid(win, rows, cols, WIDTH, HEIGHT):
    gap = WIDTH // cols

    # Draw the Horizontal and Vertical lines of the Grid
    for i in range(rows):
        # Horizontal
        pygame.draw.line(win, GREY3, (0, i * gap), (WIDTH, i * gap))
        for j in range(cols):
            # Vertical
            pygame.draw.line(win, GREY3, (j * gap, 0), (j * gap, HEIGHT))

# Main draw function for drawing map


def draw(win, grid, rows, cols, WIDTH, HEIGHT):
    # win.fill(WHITE)

    for row in grid:
        for node in row:
            # Draw each individual node
            node.draw(win)

    draw_grid(win, rows, cols, WIDTH, HEIGHT)
    pygame.display.update()

# For interactivity - find mouseclick position


def get_clicked_pos(pos, cols, WIDTH):
    """Find the clicked position in terms of rows and columns.
        # TODO: Fix this function, registrers wrong node

    Args:
        pos ([type]): pygame mouse clicked position
        cols ([type]): amount of cols in map
        WIDTH ([type]): WIDTH of map

    Returns:
        (int, int): touple of indexer
    """

    gap = WIDTH // cols
    x, y = pos

    row = y // gap
    col = x // gap

    return row, col

# heuristic function


def h(p1, p2):
    """Heuristic function calculating the Manhattan distance between two points

    Args:
        p1 (touple[int, int]): [description]
        p2 (touple[int, int]): [description]

    Returns:
        int: The Manhattan ("L") distance between the two points
    """
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

# The actual algorithm


def Astar(Map):

    # import Heapq - priority queue

    # Naboer

    # Get start point
    # Liste for frontier
    # Markere ting som visited
    # beregne f score og gscore
    # Huske "parent", hvor vi kom fra - trengs for å lage path tilslutt
    # Finne ut hvordan man kan finne naboen til pos i mappet

    return


def main(win, WIDTH, HEIGHT, map):

    ROWS = map.get_rows()
    COLS = map.get_cols()
    #print(f"Rows: {ROWS}, Cols: {COLS}")

    # Positions
    start = map.get_start_pos()
    goal = map.get_goal_pos()
    # start = None
    # goal = None

    # note WIDTH is used to calculate the gap
    grid = make_grid(ROWS, COLS, WIDTH)

    # Color the nodes according to the CSV file
    grid = color_nodes(grid, map)

    # are we running the main loop currently
    run = True

    # Have we started the algorithm
    started = False

    while run:
        draw(win, grid, ROWS, COLS, WIDTH, HEIGHT)
        for event in pygame.event.get():

            # Stop the game
            if event.type == pygame.QUIT:
                run = False

            # While algorithm is running user can't interact with map, except quit
            if started:
                continue

            if pygame.mouse.get_pressed()[0]:  # On left mouse click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, COLS, WIDTH)
                node = grid[row][col]  # The clicked node

                # If start node is not defined, first click defines start node
                if not start and not node.is_goal():
                    start = node.get_pos()
                    node.make_start()

                elif not goal and not node.is_start():  # same for goal
                    goal = node.get_pos()
                    node.make_goal()

                # If start and goal are defined, left click makes node a barrier
                elif not node.is_goal() and not node.is_start():
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # On right mouse click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, COLS, WIDTH)
                node = grid[row][col]  # The clicked node

                if node.is_start():
                    start = None
                elif node.is_goal():
                    goal = None

                node.make_flatGround()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    # start algorithm on space key
                    for row in grid:
                        for node in row:
                            node.update_neighbours()
                    Astar(lambda: draw(win, grid, ROWS, width), grid, start, goal)

    pygame.quit()


# Initializing pygame and selecting map

# Select map 1
map = Map(task=1)
# print(map.get_map())
# Set a scale factor for the pygame window
SCALE = 15

WIDTH = map.get_cols() * SCALE
HEIGHT = map.get_rows() * SCALE
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Samfundet - Intro AI - Øving 2")


main(WIN, WIDTH, HEIGHT, map)
