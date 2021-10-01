# Astar
Implementation of the A* algorithm


## Setup
1. Install pipenv 
```
  pip install pipenv
```
2. Navigate to Astar folder
2. Run
``` 
  pipenv install
```
to install the packages from the pipfile

4. done!

## How to run
Below the main function all the way down there you can choose the task number. It defaults to `task=1`

When the program is running, right click to make nodes white. 

Left click to color nodes black.
If there is no start or goal node yet, this will first color nodes as start (turquoise) and goal (green) nodes.

`Keys 1-4` to change between tasks

Press `spacekey` to run the A* algorithm

Press `r` to reset back to the map corresponding to the chosen tasknumber

## Tips
You might have to edit the paths inside the `fill_critical_positions` function.

Depending on operating system you might have to add/remove `"astar_code/"` at the start of the paths
## Todos
- [ ] add greyscale to color_nodes function
- [ ] add greyscale weights into f score
- [ ] add keypress 1-5? to quickly change map and task
