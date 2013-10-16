#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import random
import sys
import os
import time

os.environ['SDL_VIDEO_WINDOW_POS'] = '600, 30'


mv_chk = lambda x, y: x + y
lt_chk = lambda x, y: x - y

def h_mov(coordinates):
    horizontal = {1:[-20, 0], 2:[20, 0]}
    moves = [v for v in [map(mv_chk, coordinates, horizontal[i]) 
             for i in horizontal] if all(j>0 and j<700 for j in v)]
    return moves

def v_mov(coordinates):
    vertical = {1:[0, -20], 2:[0, 20]}
    moves = [v for v in [map(mv_chk, coordinates, vertical[i])
             for i in vertical] if all(j>0 and j<700 for j in v)]
    return moves

def vec_chk(cur, pre):
    diff = tuple(map(lt_chk, cur, pre))
    nodes = {(0, 20,):[[-20, 0], [20, 0], [20, 20], [-20, 20], [0, 20]],
             (0, -20,):[[-20, 0], [20, 0], [-20, -20], [20, -20], [0, -20]],
             (20, 0,):[[20, 0], [20, -20], [20, 20], [0, -20], [0, 20]],
             (-20, 0,):[[-20, 0], [-20, -20], [-20, 20], [0, -20], [0, 20]]
            }
    moves = [v for v in [map(mv_chk, cur, i) for i in nodes[diff]]]
    return moves


def main():
    pygame.init()
    screen = pygame.display.set_mode((720, 720))
    home = os.getcwd()
    wall = pygame.image.load(home + '/images/sm_wall.png')
    wall.convert_alpha()
    indicator = pygame.image.load(home + '/images/sm_position.png')
    indicator.convert_alpha()
    location = [20, 720]
    screen.blit(wall, (20, 700))
    filled = [[20,700]] 
    prev_type = 'vert' 
    curr_type = 'vert'
    prev = [20, 700]
    pos = [20, 680]
    curr = pos
    unexplored = [None]
    horz = [i for i in h_mov(pos) if i not in filled]
    vert = [i for i in v_mov(pos) if i not in filled]
    edges = horz + vert
    while unexplored:
        if unexplored[0] == None:
            unexplored.pop(0)
        if (all(i > 0 and i < 700 for i in pos) and pos not in filled):
            screen.blit(wall, pos)
            pygame.display.flip()
            filled.append(pos) 
            horz = [i for i in h_mov(pos) if i not in filled]
            vert = [i for i in v_mov(pos) if i not in filled]
            edges = horz + vert
            prev = pos
            if prev_type != curr_type and curr_type == 'horz':
                while True:
                    if horz:
                        pos = random.choice(horz)
                        horz.remove(pos)
                        if not [i for i in vec_chk(pos, prev) if i in filled]:
                            curr = pos
                            prev_type = curr_type 
                            if prev[0] == curr[0]:
                                curr_type = 'vert'
                            else:
                                curr_type = 'horz'    
                            for i in edges:
                                unexplored.append({tuple(prev):i})
                            break                    
                    else:
                        pos = prev
                        break
            elif prev_type != curr_type and curr_type == 'vert':
                while True:
                    if vert:
                        pos = random.choice(vert)
                        vert.remove(pos)
                        if not [i for i in vec_chk(pos, prev) if i in filled]:
                            curr = pos                    
                            prev_type = curr_type 
                            if prev[0] == curr[0]:
                                curr_type = 'vert'
                            else:
                                curr_type = 'horz'
                            for i in edges:
                                unexplored.append({tuple(prev):i})
                            break
                    else:
                        pos = prev
                        break
            else:
                while True:
                    if edges:
                        pos = random.choice(edges)
                        edges.remove(pos)
                        if not [i for i in vec_chk(pos, prev) if i in filled]:
                            curr = pos
                            prev_type = curr_type 
                            if prev[0] == curr[0]:
                                curr_type = 'vert'
                            else:
                                curr_type = 'horz'
                            for i in edges:
                                unexplored.append({tuple(prev):i})
                            break
                    else:
                        pos = prev
                        break

        else:
            while True:
                if unexplored:
                    move_pos = unexplored.pop(0)
                    prev, pos = move_pos.items()[0]
                    if not [i for i in vec_chk(pos, prev) if i in filled]:
                        curr = pos
                        prev_type = curr_type
                        if prev[0] == curr[0]:
                            curr_type = 'vert'
                        else:
                            curr_type = 'horz'
                        break
                else:
                    break
    screen.blit(wall, [700, 20])
    filled.extend([[700, 20], [720, 20]])
    screen.blit(indicator, location) 
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN and 
                event.key == pygame.K_ESCAPE):
                sys.exit()
            if (event.type == pygame.KEYDOWN and
                event.key == pygame.K_UP):
                if [location[0], location[1] - 20] in filled:
                    location[1] -= 20
            if (event.type == pygame.KEYDOWN and
                event.key == pygame.K_DOWN):
                if [location[0], location[1] + 20] in filled:
                    location[1] += 20
            if (event.type == pygame.KEYDOWN and
                event.key == pygame.K_RIGHT):
                if [location[0] + 20, location[1]] in filled:
                    location[0] += 20
            if (event.type == pygame.KEYDOWN and
                event.key == pygame.K_LEFT):
                if [location[0] - 20, location[1]] in filled:
                    location[0] -= 20
        for path in filled:
            screen.blit(wall, path)
        screen.blit(indicator, location)
        pygame.display.flip()

if __name__ == '__main__':
    main()
