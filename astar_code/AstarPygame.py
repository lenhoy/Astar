from pandas.core.construction import array
from pandas.core.dtypes.missing import array_equivalent
import pygame
import math
import pandas as pd
from queue import PriorityQueue

# Code based on https://www.youtube.com/watch?v=JtiK0DOeI4A&t=4122s



# Colors for classification of nodes
RED = (255, 0, 0) # Interior/Closed nodes
GREEN = (0, 255, 0) # Goal node
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0) 
WHITE = (255, 255, 255) # Unvisited node
BLACK = (0, 0, 0) # Barrier
PURPLE = (128, 0, 128) # Path
ORANGE = (255, 165, 0) # Frontier
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208) # Start node


# Create python enviroment based on handout Map 
class Map:
    def __init__(self, task=1):
        self.start_pos, self.goal_pos, self.end_goal_pos, self.path_to_map = self.fill_critical_positions(task)
        self.mapArray = self.read_map(self.path_to_map)
        #self.tmp_cell_value = self.get_cell_value(self.goal_pos)
        #self.set_cell_value(self.start_pos, ' S ')
        #self.set_cell_value(self.goal_pos, ' G ')
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
            path_to_map = 'astar_code/Samfundet_map_1.csv'
        elif task == 2:
            start_pos = [40, 32]
            goal_pos = [8, 5]
            end_goal_pos = goal_pos
            path_to_map = 'astar_code/Samfundet_map_1.csv'
        elif task == 3:
            start_pos = [28, 32]
            goal_pos = [6, 32]
            end_goal_pos = goal_pos
            path_to_map = 'astar_code/Samfundet_map_2.csv'
        elif task == 4:
            start_pos = [28, 32]
            goal_pos = [6, 32]
            end_goal_pos = goal_pos
            path_to_map = 'astar_code/Samfundet_map_Edgar_full.csv'
        elif task == 5:
            start_pos = [14, 18]
            goal_pos = [6, 36]
            end_goal_pos = [6, 7]
            path_to_map = 'astar_code/Samfundet_map_2.csv'

        return start_pos, goal_pos, end_goal_pos, path_to_map
    
    def get_map(self):
        """Should return the map array, but gives out bound method something...

        Returns:
            [type]: [description]
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


#object for nodes
class Node:
    def __init__(self, row, col, width, height, total_rows):
        self.row = row
        self.col = col
        #Width/height here references to the drawn cubes
        #x, y are the coordinates taking the width of a cube into account
        # NOTE: make width=height for normal, rectangular cubes in the grid
        self.x = row * width
        self.y = col * height
        self.color = WHITE
        self.neighbours = []
        self.width = width
        self.height = height
        self.total_rows = total_rows
        
    def get_pos(self):
        return self.row, self.col
        
    # Methods for checking status of node
    def is_interior(self):
        return self.color == RED
    
    def is_frontier(self):
        return self.color == ORANGE
    
    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == TURQUOISE

    def is_end(self):
        return self.color == GREEN
    
    def is_reset(self):
        return self.color == WHITE
    
    # Methods for changing status of node
    def make_interior(self):
        self.color = RED
    
    def make_frontier(self):
        self.color = ORANGE
    
    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = TURQUOISE

    def make_end(self):
        self.color = GREEN
    
    def make_reset(self):
        self.color = WHITE
        
    def make_path(self):
        self.color = PURPLE
        
    
    # Method to draw node/cube
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        
    def update_neighbours(self, grid):
        pass #TODO: implement later
    
    # Less than, for comparing two nodes 
    def __lt__(self, other):
        return False

# Function for making grid of nodes
def make_grid(rows, cols, width):
    """Make a grid of nodes

    Args:
        rows (int): amount of rows
        cols (int): amount of cols
        width (int): the calculated width with regard to cube size
        height (int): the calculated height with regard to cube size
    Returns:
        2d Array: Array of node objects
    """
    grid = []
    gap = width // cols
    for i in range(rows):
        grid.append([])
        for j in range(cols):
            node = Node(i, j, gap, gap, rows)
            grid[i].append(node)

    return grid

# Function for defining node colors based on CSV file / map
def color_nodes(grid, map):
    pass
         
# Function for drawing the gridlines
def draw_grid(win, rows, cols, width, height):
    gap = width // cols
    
    # Draw the Horizontal and Vertical lines of the Grid
    for i in range(rows):
        # Horizontal
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(cols):
            # Vertical
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, height))

# Main draw function for drawing map
def draw(win, grid, rows, cols, width, height):
    win.fill(WHITE)
    
    for row in grid:
        for node in row:
            # Draw each individual node
            node.draw(win)
    
    draw_grid(win, rows, cols, width, height)
    pygame.display.update()
    
    
# For interactivity - find mouseclick position
def get_clicked_pos(pos, rows, width):
    """Find the clicked position in terms of rows and columns

    Args:
        pos ([type]): pygame mouse clicked position
        rows ([type]): amount of rows in map
        width ([type]): width of map

    Returns:
        (int, int): touple of indexer
    """
    gap = width // rows
    y, x = pos
    
    row = y // gap
    col = x // gap
    
    return row, col
    
    
    
#heuristic function
def h(p1, p2):
    """Heuristic function calculating the Manhattan distance between two points

    Args:
        p1 (touple[int]): [description]
        p2 (touple[int]): [description]

    Returns:
        int: The manhattan ("L") distance between the two points
    """
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)
     
     
#The actual algorithm 
def Astar(Map):
    
    
    # import Heapq - priority queue
    
    # Naboer
    
    # Get start point
    # Liste for frontier
    #Markere ting som visited
    #beregne f score og gscore
    #Huske "parent", hvor vi kom fra - trengs for å lage path tilslutt
    # Finne ut hvordan man kan finne naboen til pos i mappet
    
    
    
    
    return


def main(win, width, height, map):
    
    ROWS = map.get_rows()
    COLS = map.get_cols()
    #print(f"Rows: {ROWS}, Cols: {COLS}")
    
    #Positions
    start = map.get_start_pos
    goal = map.get_goal_pos
    
    grid = make_grid(ROWS, COLS, width) # note width is used to calculate the gap
    
    # are we running the main loop currently
    run = True
    
    # Have we started the algorithm
    started = False
    
    while run:
        draw(win, grid, ROWS, COLS, width, height)
        for event in pygame.event.get():
            
            # Stop the game
            if event.type == pygame.QUIT:
                run = False
                
            # While algorithm is running user can't interact with map, except quit
            if started:
                continue
            
            if pygame.mouse.get_pressed()[0]: # On left mouse click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col] # The clicked node
                
                # If start node is not defined, first click defines start node
                if not start:
                    start = node
                    start.make_start()
                elif not goal: # same for goal
                    goal = node
                    goal.make_goal()
                    
                # If start and goal are defined, left click makes node a barrier
                elif node != goal and node != start:
                    node.make_barrier()
                    
                    
                
            elif pygame.mouse.get_pressed()[2]: # On right mouse click 
                pass
            
                
    pygame.quit()
    
    
# Initializing pygame and selecting map

#Select map 1
map = Map(task=1)

#Set a scale factor for the pygame window
SCALE = 15

WIDTH = map.get_cols() * SCALE
HEIGHT = map.get_rows() * SCALE
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Samfundet Intro AI Øving 2")


main(WIN, WIDTH, HEIGHT, map)
    
    
