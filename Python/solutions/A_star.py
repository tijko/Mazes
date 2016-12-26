#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict


class AstarPathFinder(object):

    def __init__(self, paths):
        self.paths = paths 
        self.path = list()
        self.start, self.end = (20, 700), (700, 20)
        self.current = self.start
        self.prev = {self.start:None} 
        self.g_score = defaultdict(int)
        self.f_score = defaultdict(int)
        self.g_score[self.start]
        self._opend = {self.start}
        self.closed = set()

    def h_score_cal(self, position):
        cur_x, cur_y = position
        end_x, end_y = self.end
        return (abs(cur_x - end_x) + abs(cur_y - end_y)) * 10

    @property
    def find_current(self):
        low = min([self.f_score[i] for i in self.f_score if i in self._opend])
        for position in self._opend:
            if self.f_score[position] != low:
                continue
            return position
    
    @property
    def neighbors(self):
        borders = [(20, 0), (-20, 0), (0, 20), (0, -20)]
        cost_cal = lambda x, y: x - y
        adjacent_walls = [tuple(map(cost_cal, self.current, i)) for i in borders]
        return [tuple(n) for n in adjacent_walls if n in self.paths]
        
    def pathfinder(self):
        self.f_score[self.start] = (self.g_score[self.start] + 
                                    self.h_score_cal(self.start))
        while self._opend:
            self.current = self.find_current
            if self.current == self.end:  
                return self.reconstruct_path(self.prev, self.current)
            self._opend.remove(self.current)
            self.closed.add(self.current)
            for neighbor in self.neighbors:
                tenative_g_score = self.g_score[self.current] + 1
                tenative_f_score = (tenative_g_score + 
                                    self.h_score_cal(neighbor))              
                if (neighbor in self.closed and 
                    tenative_f_score >= self.f_score[neighbor]):
                    continue
                if (neighbor not in self._opend or 
                    tenative_f_score < self.f_score[neighbor]):
                    self.prev[neighbor] = self.current
                    self.g_score[neighbor] = tenative_g_score
                    self.f_score[neighbor] = tenative_f_score
                    if neighbor not in self._opend:
                        self._opend.add(neighbor)

    def reconstruct_path(self, prev, curr):
        if curr in prev:
            self.path.append(curr)
            self.reconstruct_path(prev, prev[curr])
        return self.path
