#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
import random
from collections import deque, namedtuple
import os


# refer to Maze MASK constants for valid mask characters
sample_mask =\
    """

       #########################
       ##......................##
        ##......................##
         ##......................##
          ##........    ..........#
         ##......... ## .........##
        ##.......... ## ........##
       ##...........    .......##
       #......................##
       #......................#
       #......................#
       #......................#
       #......................#
       #......................#
       #......................#
       #......................#
       ########################

    """

bird =\
    """
                 ######
              ###......###
            ##............##
          ##...  ....  .....##
         #.....  ....  .......#
        #......................#
        #......................#
        #.......... ...........#
        #.........   ..........#
        #........     .........#
        #.......       ........#
        #........     .........#
        #.........   ..........#
        #.......... ...........#
        ##....................##
        ####................####
        ###..................###
        ###..................###
        ####................####
        ###..................###
        ##....................##         #
        ##....................##        ##
        #......................#       #.#
        #......................#     ##..#
        #......................#   ##...#
        #......................####....#
        #.............................#
        #............................#
        #..........................##
        #......................####
         #....................#
          ##................##
           #.#............#.#
           #.####......####.#
           #.#   ######   #.#
           #.#            #.#         ####
          ##.##          ##.##       #...#
         #.....#        #.....#     #....#
         #.#.#.#        #.#.#.#     #....#
         #.#.#.#        #.#.#.#     #....###
##########.#.#.##########.#.#.#######.......###
...............................................#
................................................#
###########################################......#
                                           ###....#
                                              ###..#
                                                 ###
    """

def main():
    os.environ['SDL_VIDEO_WINDOW_POS'] = '600, 30'
    pygame.init()
    # images and sizes
    image_dir = os.path.join(os.getcwd(), 'images')
    _path = pygame.image.load(os.path.join(image_dir, 'path.png'))
    wall = pygame.image.load(os.path.join(image_dir, 'wall.png'))
    indicator = pygame.image.load(os.path.join(image_dir, 'position.png'))
    entrance = pygame.image.load(os.path.join(image_dir, 'entrance.png'))
    _exit = pygame.image.load(os.path.join(image_dir, 'exit.png'))
    block_width, block_height = _path.get_size()
    # maze and position lists
    maze = Maze(bird)
    maze_text = str(maze)
    maze_rows = maze_text.splitlines(False)
    entrance_coordinates = list()
    exit_coordinates = list()
    path_coordinates = list()
    wall_coordinates = list()
    undefined_coordinates = list()
    lookup = {Maze.BLOCK_ENTRANCE: entrance_coordinates,
              Maze.BLOCK_EXIT: exit_coordinates,
              Maze.BLOCK_PATH: path_coordinates,
              Maze.BLOCK_WALL: wall_coordinates,
              Maze.BLOCK_UNDEFINED: undefined_coordinates}
    for row, row_string in enumerate(maze_rows):
        for col, char in enumerate(row_string):
            coordinates = (block_width * col, block_height * row)
            lookup[char].append(coordinates)
    path_coordinates.extend(entrance_coordinates)
    path_coordinates.extend(exit_coordinates)
    # display
    display_height = block_height * (len(maze_rows) + 1)
    display_width = block_width * (max(len(r) for r in maze_rows) + 1)
    display = pygame.display.set_mode((display_width, display_height))
    _path.convert_alpha()
    indicator.convert_alpha()
    entrance.convert_alpha()
    _exit.convert_alpha()
    # location
    loc = [entrance_coordinates[0][0], entrance_coordinates[0][1]]
    # main loop
    continue_main_loop = True
    while continue_main_loop:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                continue_main_loop = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if (loc[0], loc[1] - block_height) in path_coordinates:
                    loc[1] -= block_height
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                if (loc[0], loc[1] + block_height) in path_coordinates:
                    loc[1] += block_height
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                if (loc[0] + block_width, loc[1]) in path_coordinates:
                    loc[0] += block_width
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                if (loc[0] - block_width, loc[1]) in path_coordinates:
                    loc[0] -= block_width
        for coordinates in path_coordinates:
            display.blit(_path, coordinates)
        for coordinates in wall_coordinates:
            display.blit(wall, coordinates)
        display.blit(entrance, entrance_coordinates[0])
        display.blit(_exit, exit_coordinates[0])
        display.blit(indicator, loc)
        pygame.display.flip()


class Maze(object):
    Coordinates = namedtuple('Coordinates', ('row', 'col'))
    # text mask constants
    MASK_UNDEFINED = ' '
    MASK_USABLE = '.'
    MASK_UNUSABLE = '#'
    # status of block spaces
    BLOCK_UNDEFINED = ' '
    BLOCK_ENTRANCE = '@'
    BLOCK_EXIT = '!'
    BLOCK_PATH = '='
    BLOCK_WALL = '#'
    # neighbors definition
    BLOCK_NEIGHBORS = (Coordinates(-1, 0),  # up
                       Coordinates(1, 0),  # down
                       Coordinates(0, -1),  # left
                       Coordinates(0, 1))  # right

    def __init__(self, mask):
        """Create a random maze based on the text mask.

        mask: refer to MASK_* constants for characters to use in the mask
        """
        spaces = self._mask_to_spaces(mask)
        self._spaces = spaces
        self._spaces = self._generate_maze(spaces)

    def __str__(self):
        """Return a rectangular string representation of this maze."""
        # find the bounding rectangle
        rows, cols = zip(*self._spaces)
        row_min, row_max = min(rows), max(rows)
        col_min, col_max = min(cols), max(cols)
        # build the string
        rows_list = list()
        for row in range(row_min, row_max + 1):
            row_list = list()
            for col in range(col_min, col_max + 1):
                coordinates = self.Coordinates(row, col)
                try:
                    status = self._spaces[coordinates]
                except KeyError:
                    status = self.MASK_UNDEFINED
                #char = status_to_char[status]
                row_list.append(status)
            rows_list.append(row_list)
        return '\n'.join(''.join(char for char in row_list)
                         for row_list in rows_list)

    def _mask_to_spaces(self, mask):
        """Convert the provided mask string to a dict of usable/unusable spaces.

        mask: refer to MASK_* constants for characters to use in the mask
            unknown characters will be treated as unusable
        returns spaces: a dict with (row, col) keys and status values
        """
        valid_chars = (self.MASK_USABLE, self.MASK_UNUSABLE,
                       self.MASK_UNDEFINED)
        spaces = dict()
        for row, row_string in enumerate(mask.splitlines(False)):
            for col, char in enumerate(row_string):
                if char in valid_chars:
                    # ignore invalid chars
                    coordinates = self.Coordinates(row, col)
                    spaces[coordinates] = char
        return spaces

    def _generate_maze(self, spaces):
        """Modify dict of spaces into a maze and return it."""
        # find a position on an edge and start making the maze path
        edges = tuple(self._edges(spaces))  # efficient tester for spaces
        start = random.choice(edges)
        spaces[start] = self.BLOCK_ENTRANCE
        current_path = deque()
        current_path.append(start)
        potential_exit_and_length = (start, 1)  # longest path to an edge
        # iteratively loop until the algorithm can find no more usable spaces
        # current_path will get longer as it stretches through the maze
        # eventually it will get shorter and come back to zero as the maze
        # fills up
        space = start
        while current_path:
            neighbors = list(self._neighbors(space, spaces))
            random.shuffle(neighbors)
            for new_space, status in neighbors:
                if self._is_pathable(new_space, space, spaces):
                    # pathable neighbor ==> keep extending the path
                    spaces[new_space] = self.BLOCK_PATH  # set it as a path
                    current_path.append(new_space)  # extend the path stack
                    # track the best potential exit
                    new_length = len(current_path)
                    old_length = potential_exit_and_length[1]
                    if (new_length > old_length) and (new_space in edges):
                        potential_exit_and_length = (new_space, new_length)
                    # setup for the next iteration
                    space = new_space
                    break  # don't need to check more neighbors
            else:
                # no usable neighbors ==> back up one step
                try:
                    # normal case - back up one step
                    space = current_path.pop()
                except IndexError:
                    # special case - maze complete. no more usable spaces
                    pass
        # when done making the maze, mark all remaining usable spaces as walls
        for space, status in spaces.items():
            if status == self.MASK_USABLE:
                spaces[space] = self.BLOCK_WALL
        # finally mark longest path to edge as exit
        _exit = potential_exit_and_length[0]
        spaces[_exit] = self.BLOCK_EXIT
        return spaces

    def _edges(self, spaces):
        """Generate all edge coordinates in spaces.

        An edge is defined as a space that:
            1) is a user space
            AND
                a) has at least one unusable neighbor
                OR
                b) is a maximum or minimum usable row or column
        """
        # setup tracking and test variables
        edge_set = set()
        user_statuses = (self.BLOCK_EXIT, self.BLOCK_ENTRANCE, self.BLOCK_PATH,
                         self.MASK_USABLE)
        rows, cols = zip(*spaces)
        row_minmax = min(rows), max(rows)
        col_minmax = min(cols), max(cols)
        for space, status in spaces.items():
            # usable or path spaces
            if status in user_statuses:
                for n, n_status in self._neighbors(space, spaces):
                    if n_status == self.MASK_UNUSABLE:
                        # at least one unusable neighbor
                        edge_set.add(space)
                        break  # no need to keep testing this space
                    else:
                        # OR min/max row/col
                        row, col = space
                        if row in row_minmax or col in col_minmax:
                            edge_set.add(space)
                            break  # no need to keep testing this space
        for edge in edge_set:
            yield edge

    def _neighbors(self, space, spaces):
        """Generate all neighbor coordinates and statuses of space."""
        row, col = space
        for row_delta, col_delta in self.BLOCK_NEIGHBORS:
            coordinates = self.Coordinates(row + row_delta, col + col_delta)
            try:
                status = spaces[coordinates]
                yield coordinates, status  # the coordinates exist
            except KeyError:
                pass  # the coordinates don't exist

    def _is_pathable(self, space, previous_space, spaces):
        """Return True if the space can be used as a path. False otherwise."""
        # for blocks, the rule is (usable) and (no path statuses)
        if spaces[space] != self.MASK_USABLE:
            return False
        path_statuses = (self.BLOCK_ENTRANCE, self.BLOCK_EXIT, self.BLOCK_PATH)
        for neighbor, status in self._neighbors(space, spaces):
            if neighbor == previous_space:
                continue  # skip the previous space
            if status in path_statuses:
                return False
        # if it couldn't be disqualified, allow it
        return True


if __name__ == '__main__':
    main()
