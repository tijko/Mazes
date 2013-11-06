#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import random
import sys
import os
import time

from collections import defaultdict

os.environ['SDL_VIDEO_WINDOW_POS'] = '600, 30'


class Maze(object):

    def __init__(self, scr, wall):
        self.scr = scr
        self.wall = wall
        self.mv_chk = lambda x, y: x + y
        self.lt_chk = lambda x, y: x - y
        maze_grid = range(1296)
        random.shuffle(maze_grid)
        self.maze = list()
        self.explored = set()
        self.matrix = dict()
        self.frontier = defaultdict(list)
        for row in xrange(0, 720, 20):
            for col in xrange(0, 720, 20):
                self.matrix[maze_grid.pop(0)] = [row, col]


    @property
    def get_first_wall(self):
        #XXX: works because the keys match up with the length but 
        #     wouldn't if keys = 'str' (better random.choice just keys)
        self.pos = random.choice(self.matrix)  
        for weight in self.matrix:
            if self.matrix[weight] in self.all_mvs:
                self.frontier[weight].extend([self.matrix[weight], self.pos])        
        self.explored.update(tuple(self.pos))
        self.scr.blit(self.wall, self.pos)
        self.prev = self.pos
        pygame.display.flip()

    @property
    def all_mvs(self):
        directions = {1:[0, -20], 2:[0, 20], 3:[-20, 0], 4:[20, 0]}
        moves = [v for v in [map(self.mv_chk, self.pos, directions[i])
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
        moves = [v for v in [map(self.mv_chk, self.pos, i) for i in nodes[diff]]]
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
                    self.scr.blit(self.wall, self.pos)
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

def main():
    pygame.init()
    screen = pygame.display.set_mode((720, 720))
    home = os.getcwd()
    wall = pygame.image.load(home + '/images/sm_wall.png')
    wall.convert_alpha()
    indicator = pygame.image.load(home + '/images/sm_position.png')
    indicator.convert_alpha()
    location = [20, 700]
    screen.blit(wall, (20, 700))
    screen.blit(wall, (700, 20))
    maze = Maze(screen, wall)
    maze_structure = maze.gen_maze()
    maze_structure.extend([[700, 20], [720, 20], [20, 700]])
    if not([700, 40] in maze_structure) and not([680, 20] in maze_structure):
        if ([660, 20] in maze_structure):
            maze_structure.append([700, 40])
        else:
            maze_structure.append([680, 20])
    while True:
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN and 
                event.key == pygame.K_ESCAPE):
                sys.exit()
            if (event.type == pygame.KEYDOWN and
                event.key == pygame.K_UP):
                if [location[0], location[1] - 20] in maze_structure:
                    location[1] -= 20
            if (event.type == pygame.KEYDOWN and
                event.key == pygame.K_DOWN):
                if [location[0], location[1] + 20] in maze_structure:
                    location[1] += 20
            if (event.type == pygame.KEYDOWN and
                event.key == pygame.K_RIGHT):
                if [location[0] + 20, location[1]] in maze_structure:
                    location[0] += 20
            if (event.type == pygame.KEYDOWN and
                event.key == pygame.K_LEFT):
                if [location[0] - 20, location[1]] in maze_structure:
                    location[0] -= 20
        for path in maze_structure:
            screen.blit(wall, path)
        screen.blit(indicator, location)
        pygame.display.flip()


if __name__ == '__main__':
    main()
