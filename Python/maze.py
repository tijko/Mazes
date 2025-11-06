#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import pygame

from pathlib import PosixPath
from solutions.A_star import AstarPathFinder as astar


class Maze(object):

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((720, 720))
        '''
        We know that the path relative to the "images" directory
        must go through "Mazes/Python/images/".  Where this resides
        is not of consequence.  Just add this as the "absolute".
        Hence the `os.getcwd()' is misguided.....
        '''
        home = PosixPath.home()
        images = home.joinpath('Mazes/Python/images')
        self.wall = pygame.image.load(images.joinpath('sm_wall.png'))
        self.wall.convert_alpha()
        self.solution_path = pygame.image.load(images.joinpath('solution.png'))
        self.solution_path.convert_alpha()
        self.indicator = pygame.image.load(images.joinpath('sm_position.png'))
        self.mv_chk = lambda x, y: x + y
        self.lt_chk = lambda x, y: x - y
        self.indicator.convert_alpha()
        self.location = [20, 700]
        self.screen.blit(self.wall, (20, 700))
        self.screen.blit(self.wall, (700, 20))
        self.solve = False

    def run_maze_loop(self, maze):
        path_finder = astar(maze)
        solution = path_finder.pathfinder()
        while True:
            for event in pygame.event.get():
                if (event.type == pygame.KEYDOWN and 
                    event.key == pygame.K_ESCAPE):
                    sys.exit()
                elif (event.type == pygame.KEYDOWN and
                    event.key == pygame.K_UP):
                    if (self.location[0], self.location[1] - 20) in maze:
                        self.location[1] -= 20
                elif (event.type == pygame.KEYDOWN and
                    event.key == pygame.K_DOWN):
                    if (self.location[0], self.location[1] + 20) in maze:
                        self.location[1] += 20
                elif (event.type == pygame.KEYDOWN and
                    event.key == pygame.K_RIGHT):
                    if (self.location[0] + 20, self.location[1]) in maze:
                        self.location[0] += 20
                elif (event.type == pygame.KEYDOWN and
                    event.key == pygame.K_LEFT):
                    if (self.location[0] - 20, self.location[1]) in maze:
                        self.location[0] -= 20
                elif (event.type == pygame.KEYDOWN and
                    event.key == pygame.K_s):
                    self.solve = True
            for path in maze:
                self.screen.blit(self.wall, path)
            if self.solve:
                for path in solution:
                    self.screen.blit(self.solution_path, path)
            self.screen.blit(self.indicator, self.location)
            pygame.display.flip()
