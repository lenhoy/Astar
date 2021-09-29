from pandas.core.construction import array
from pandas.core.dtypes.missing import array_equivalent
import pygame
import math
import pandas as pd
from queue import PriorityQueue

# Code based on https://www.youtube.com/watch?v=JtiK0DOeI4A&t=4122s

# Initializing pygame and setting constants
WIDTH = 39
HEIGHT = 47
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Samfundet Intro AI Øving 2")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


# Create python enviroment based on handout Map 
class Map_Obj():
    def __init__(self, task=1):
        self.start_pos, self.goal_pos, self.end_goal_pos, self.path_to_map = self.fill_critical_positions(task)
        self.map = self.read_map(self.path_to_map)
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
        return self.map


#object for nodes
class Node:
    def __init__(self, row, col, width, total_rows):
        self.row


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


