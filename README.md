PyMaze
======

Randomized maze generator with pygames

There are three mazes you can run, first `cd /path/of/pymaze` then:

    python shape_maze.py

to run the shape maze or:

    python DFS_maze.py

for the depth first search algorithm generated maze or:

    python prims_maze.py

to run the prims algorithm generated maze.

#### Description:

The depth first search or **DFS** maze will randomly chose a path direction 
while their are still "unexplored" grid coordinates left.  If the path 
direction is blocked by intersections or the grid edge, the path direction 
will back track to the last unblocked and unexplored coordinate.  This will 
repeat until all coordinates are "explored".

The **prims** algorithm generated maze starts by randomly selecting a coordinate 
from a randomly weighted grid coordinates to expand from.  Once that position
is established, all that walls edges are added to the frontier array.  Since
every coordinate has been assigned a random weight, the next position is 
determined by the minimum weight in the frontier array.  These steps are 
repeated until there are no more frontier edges. 

#### Usage:

You start at the bottom left corner and use the arrow keys to move, 
finishing at the top right.

