#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import random

from maze import *
from itertools import product
from collections import defaultdict

os.environ['SDL_VIDEO_WINDOW_POS'] = '600, 30'


class Prims(Maze):

    def __init__(self):
        super(Prims, self).__init__()

        self.maze = list()
        self.explored = set()
        self.frontier = defaultdict(list)
        maze_coords = list(range(1296))
        random.shuffle(maze_coords)
        self.matrix = dict(zip(maze_coords, product(range(0, 720, 20),
                                                    range(0, 720, 20))))
        self.maze_structure = self.gen_maze()
        if (not ((700, 40) in self.maze_structure) and
            not ((680, 20) in self.maze_structure)):
            if ((660, 20) in self.maze_structure):
                self.maze_structure.append((700, 40,))
            else:
                self.maze_structure.append((680, 20,))
        self.maze_structure.extend([(700, 20,), (720, 20,), (20, 700,)])

    @property
    def get_first_wall(self):
        #XXX: works because the keys match up with the length but 
        #     wouldn't if keys = 'str' (better random.choice just keys)
        self.pos = random.choice(self.matrix)  
        for weight in self.matrix:
            if self.matrix[weight] in self.all_mvs:
                self.frontier[weight].extend([self.matrix[weight], self.pos])        
        self.explored.update(tuple(self.pos))
        self.screen.blit(self.wall, self.pos)
        self.prev = self.pos

    @property
    def all_mvs(self):
        directions = {1:[0, -20], 2:[0, 20], 3:[-20, 0], 4:[20, 0]}
        moves = [v for v in [tuple(map(self.mv_chk, self.pos, directions[i]))
                 for i in directions] if all(j>0 and j<700 for j in v)]
        return moves

    @property
    def vec_chk(self):
        diff = tuple(map(self.lt_chk, self.pos, self.prev))
        nodes = {(0, 20,):[[-20, 0], [20, 0], [20, 20], [-20, 20], [0, 20]],
                 (0, -20,):[[-20, 0], [20, 0], [-20, -20], [20, -20], [0, -20]],
                 (20, 0,):[[20, 0], [20, -20], [20, 20], [0, -20], [0, 20]],
                 (-20, 0,):[[-20, 0], [-20, -20], [-20, 20], [0, -20], [0, 20]]
                }
        moves = [v for v in [tuple(map(self.mv_chk, self.pos, i)) 
                             for i in nodes[diff]]]
        return moves

    def gen_maze(self):
        self.get_first_wall
        while self.frontier:
            self.explored.update([tuple(self.frontier[k][0]) 
                                  for k in self.frontier])
            lowest_weight = min(self.frontier)
            self.pos = self.frontier[lowest_weight][0]
            self.prev = self.frontier[lowest_weight][1]
            del self.frontier[lowest_weight]
            if (all(i > 0 and i < 700 for i in self.pos) and 
                self.pos not in self.maze):
                if not any(i for i in self.vec_chk if i in self.maze):
                    self.screen.blit(self.wall, self.pos)
                    pygame.display.flip() 
                    time.sleep(0.05)
                    nxt_mvs = self.all_mvs
                    for cell in self.matrix:
                        if (self.matrix[cell] in nxt_mvs and 
                            tuple(self.matrix[cell]) not in self.explored):
                            self.frontier[cell].extend([self.matrix[cell], 
                                                        self.pos])
                    self.maze.append(self.pos)
        return self.maze

if __name__ == '__main__':
    prims = Prims()
    prims.run_maze_loop(prims.maze_structure)
