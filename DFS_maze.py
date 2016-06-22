#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import random
import sys
import os
import time

from solutions.A_star import AstarPathFinder as astar

os.environ['SDL_VIDEO_WINDOW_POS'] = '600, 30'


class Maze(object):

    def __init__(self, scr, wall):

        self.scr = scr
        self.wall = wall

        self.mv_chk = lambda x, y: x + y
        self.lt_chk = lambda x, y: x - y
        
        self.prev = [20, 700]
        self.pos = [20, 680]

        self.explored = [self.prev]
        self.unexplored = [None]

        self.prev_type = 'vert' 
        self.curr_type = 'vert'

        self.horz = [i for i in self.h_mov if i not in self.explored]
        self.vert = [i for i in self.v_mov if i not in self.explored]
        self.edges = self.horz + self.vert

    @property
    def h_mov(self):
        horizontal = {1:[-20, 0], 2:[20, 0]}
        moves = [v for v in [list(map(self.mv_chk, self.pos, horizontal[i])) 
                 for i in horizontal] if all(j>0 and j<700 for j in v)]
        return moves

    @property
    def v_mov(self):
        vertical = {1:[0, -20], 2:[0, 20]}
        moves = [v for v in [list(map(self.mv_chk, self.pos, vertical[i]))
                 for i in vertical] if all(j>0 and j<700 for j in v)]
        return moves

    @property
    def vec_chk(self):
        diff = tuple(map(self.lt_chk, self.pos, self.prev))
        nodes = {(0, 20,):[[-20, 0], [20, 0], [20, 20], [-20, 20], [0, 20]],
                 (0, -20,):[[-20, 0], [20, 0], [-20, -20], [20, -20], [0, -20]],
                 (20, 0,):[[20, 0], [20, -20], [20, 20], [0, -20], [0, 20]],
                 (-20, 0,):[[-20, 0], [-20, -20], [-20, 20], [0, -20], [0, 20]]
                }
        moves = [v for v in [list(map(self.mv_chk, self.pos, i)) 
                   for i in nodes[diff]]]
        return moves

    def next_wall(self, walls):
        move_pos = None
        while True:
            if walls:
                if isinstance(walls[0], dict):
                    move_pos = walls.pop(-1)    
                    self.prev, self.pos = list(move_pos.items())[0]
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

                self.scr.blit(self.wall, self.pos)
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

def main():
    pygame.init()
    screen = pygame.display.set_mode((720, 720))
    home = os.getcwd()
    wall = pygame.image.load(home + '/images/sm_wall.png')
    wall.convert_alpha()
    solution_path = pygame.image.load(home + '/images/solution.png')
    solution_path.convert_alpha()
    indicator = pygame.image.load(home + '/images/sm_position.png')
    indicator.convert_alpha()
    location = [20, 700]

    screen.blit(wall, (20, 700))
    screen.blit(wall, [700, 20])
    screen.blit(indicator, location)

    maze = Maze(screen, wall)
    maze_structure = maze.gen_maze()
    maze_structure.extend([[700, 20], [720, 20]])

    if not([700, 40] in maze_structure) and not([680, 20] in maze_structure):
        if ([660, 20] in maze_structure):
            maze_structure.append([700, 40])
        else:
            maze_structure.append([680, 20])
    path_finder = astar(maze_structure)
    solution = path_finder.pathfinder()
    solve = False
    while True:
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN and 
                event.key == pygame.K_ESCAPE):
                sys.exit()
            elif (event.type == pygame.KEYDOWN and
                event.key == pygame.K_UP):
                if [location[0], location[1] - 20] in maze_structure:
                    location[1] -= 20
            elif (event.type == pygame.KEYDOWN and
                event.key == pygame.K_DOWN):
                if [location[0], location[1] + 20] in maze_structure:
                    location[1] += 20
            elif (event.type == pygame.KEYDOWN and
                event.key == pygame.K_RIGHT):
                if [location[0] + 20, location[1]] in maze_structure:
                    location[0] += 20
            elif (event.type == pygame.KEYDOWN and
                event.key == pygame.K_LEFT):
                if [location[0] - 20, location[1]] in maze_structure:
                    location[0] -= 20
            elif (event.type == pygame.KEYDOWN and
                event.key == pygame.K_s):
                solve = True
        for path in maze_structure:
            screen.blit(wall, path)
        if solve:
            for path in solution:
                screen.blit(solution_path, path)
        if location == [720, 20]:
            # display
            break
        screen.blit(indicator, location)
        pygame.display.flip()


if __name__ == '__main__':
    main()
