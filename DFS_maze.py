#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import random

from maze import *

os.environ['SDL_VIDEO_WINDOW_POS'] = '600, 30'


class DFS(Maze):

    def __init__(self):
        super(DFS, self).__init__()
        
        self.prev, self.pos = (20, 700,), [20, 680]

        self.explored = [self.prev]
        self.unexplored = [None]

        self.prev_type = 'vert' 
        self.curr_type = 'vert'

        self.horz = [i for i in self.h_mov if i not in self.explored]
        self.vert = [i for i in self.v_mov if i not in self.explored]
        self.edges = self.horz + self.vert

        self.maze_structure = self.gen_maze()
        if (not((700, 40,) in self.maze_structure) and 
            not((680, 20,) in self.maze_structure)):
            if ((660, 20,) in self.maze_structure):
                self.maze_structure.append((700, 40,))
            else:
                self.maze_structure.append((680, 20,))
        self.maze_structure.extend([(700, 20,), (720, 20,), (20, 680,)])

        path_finder = astar(self.maze_structure)
        self.solution = path_finder.pathfinder()

    @property
    def h_mov(self):
        horizontal = {1:(-20, 0,), 2:(20, 0,)}
        moves = [v for v in [tuple(map(self.mv_chk, self.pos, horizontal[i])) 
                 for i in horizontal] if all(j>0 and j<700 for j in v)]
        return moves

    @property
    def v_mov(self):
        vertical = {1:(0, -20), 2:(0, 20)}
        moves = [v for v in [tuple(map(self.mv_chk, self.pos, vertical[i]))
                 for i in vertical] if all(j>0 and j<700 for j in v)]
        return moves

    @property
    def vec_chk(self):
        diff = tuple(map(self.lt_chk, self.pos, self.prev))
        nodes = {(0, 20,):[(-20, 0,), (20, 0,), (20, 20,), (-20, 20,), (0, 20,)],
                 (0, -20,):[(-20, 0,), (20, 0,), (-20, -20,), (20, -20,), (0, -20,)],
                 (20, 0,):[(20, 0,), (20, -20,), (20, 20,), (0, -20,), (0, 20,)],
                 (-20, 0,):[(-20, 0,), (-20, -20,), (-20, 20,), (0, -20,), (0, 20,)]
                }
        moves = [v for v in [tuple(map(self.mv_chk, self.pos, i)) 
                   for i in nodes[diff]]]
        return moves

    def next_wall(self, walls):
        move_pos = None
        while True:
            if walls:
                if isinstance(walls[0], dict):
                    move_pos = walls.pop(-1)    
                    self.prev, self.pos = tuple(move_pos.items())[0]
                else:
                    self.pos = random.choice(walls)
                    walls.remove(self.pos)
                if not [i for i in self.vec_chk if i in self.explored]:
                    self.prev_type = self.curr_type 
                    if self.prev[0] == self.pos[0]:
                        self.curr_type = 'vert'
                    else:
                        self.curr_type = 'horz'   
                    if not move_pos: 
                        for i in self.edges:
                            self.unexplored.append({tuple(self.prev):i})
                    return        
            else:
                self.pos = self.prev
                return

    def gen_maze(self):
        while self.unexplored:
            if not self.unexplored[0]:
                self.unexplored.pop(0)
            if (all(i > 0 and i < 700 for i in self.pos) and 
                self.pos not in self.explored):
                self.explored.append(self.pos)

                self.screen.blit(self.wall, self.pos)
                pygame.display.flip() 
                time.sleep(0.05)

                self.horz = [i for i in self.h_mov if i not in self.explored]
                self.vert = [i for i in self.v_mov if i not in self.explored]
                self.edges = self.horz + self.vert
                self.prev = self.pos
                if self.prev_type != self.curr_type and self.curr_type == 'horz':
                    self.next_wall(self.horz)
                elif self.prev_type != self.curr_type and self.curr_type == 'vert':
                    self.next_wall(self.vert)
                else:
                    self.next_wall(self.edges)
            else:
                self.next_wall(self.unexplored)
        return self.explored


if __name__ == '__main__':
    dfs_maze = DFS()
    dfs_maze.run_maze_loop(dfs_maze.maze_structure)
