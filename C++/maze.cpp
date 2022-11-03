#include <map>
#include <vector>
#include <iterator>
#include <iostream>
#include <unistd.h>
#include <signal.h>
#include <ncurses.h>


#define VERTICAL "|"
#define HORIZONTAL "--"


class Maze
{
    public:
        Maze(int max_x, int max_y);
        void build(void);
        
    private:
        int max_x;
        int max_y;
        struct vector_cmp {
            bool operator() (std::vector<int> a, std::vector<int> b)
            {
                return a[0] >  a[0] ? 0 : 
                       a[0] == b[0] ? 
                       a[1] <  b[1] : a[0] < b[0];
            }
        };

        std::map<std::vector<int>, std::string, vector_cmp> grid;
        std::map<std::vector<int>, std::string> maze;
        std::vector<std::vector<int>> find_neighbors(int x, int y);
        void draw(void);
};

Maze::Maze(int max_x, int max_y)
{
    this->max_x = max_x;
    this->max_y = max_y;

    for (int x=0; x < max_x; x++) {
        for (int y=1; y < max_y; y++) {
            std::vector<int> coord = {x, y};
            if (y % 2 == 0 && x % 3 == 0) 
                grid[coord] = VERTICAL; 
            else if (y % 2 != 0 && (x - 1) % 3 == 0) 
                grid[coord] = HORIZONTAL;
        }
    }
    
    build();
    draw();
}

std::vector<std::vector<int>> Maze::find_neighbors(int x, int y)
{
    std::vector<std::vector<int>> neighbor_list;

    int neighbors[2][6][2] = {{{3, 0}, {-3, 0}, {2, 1},
                               {2, -1}, {-1, 1}, {-1, -1}},
                              {{0, 2}, {0, -2}, {1, 1},
                               {1, -1}, {-2, 1}, {-2, -1}}};
    
    int direction = x % 3 ? 0 : 1;

    for (int i=0; i < 6; i++) {
        std::vector<int> neighbor = {x + neighbors[direction][i][0],
                                     y + neighbors[direction][i][1]};

        neighbor_list.push_back(neighbor);
    }

    return neighbor_list;
}

void Maze::build(void)
{
    srand(time(NULL));

    while (!grid.empty()) {

        int size = grid.size();
        int random_pos = rand() % size;
        std::map<std::vector<int>, std::string>::iterator it = grid.begin();
        std::advance(it, random_pos);

        std::vector<int> current = it->first;
        std::vector<std::vector<int>> neighbors = find_neighbors(current[0], 
                                                                 current[1]);
        int neighbor_count = 0;
        for (std::vector<int> neighbor : neighbors) {
            if (maze.find(neighbor) != maze.end())
                neighbor_count++;
        }

        if (neighbor_count < 3)
            maze[current] = it->second;
        grid.erase(it);
    }
}

void Maze::draw(void)
{
    std::map<std::vector<int>, std::string>::iterator it = maze.begin();
    for (; it != maze.end(); it++) { 
        mvwprintw(stdscr, it->first[1], it->first[0], "%s", it->second.c_str());
        if (it->first[1] < max_y - 3 && !(it->first[0] % 3)) {
            std::vector<int> horizontal = {it->first[0] - 1, it->first[1] + 1};
            if (maze.find(horizontal) == maze.end())
                mvwprintw(stdscr, it->first[1] + 1, it->first[0], "%s", "|");
        } else if (!((it->first[0] - 1) % 3)) {
            std::vector<int> vertical = {it->first[0], it->first[1] + 1};
            if (maze.find(vertical) == maze.end())
                mvwprintw(stdscr, it->first[1], it->first[0], "%s", " ");
        }
    }

    refresh();
}

void init_screen(void)
{
    initscr();
    noecho();
    cbreak();
    curs_set(0);

    box(stdscr, '|', '-');
}

void destroy_screen(void)
{
    nocbreak();
    endwin();
}

void interrupt(int signal_number)
{
    destroy_screen();

    std::cout << "Maze-running <" << signal_number << "> interrupted!" 
              << std::endl;
}

int main(int argc, char *argv[])
{
    struct sigaction sa;
    sa.sa_handler = interrupt;
    sigaction(SIGINT, &sa, NULL);

    init_screen();
    /* 
    mvwprintw(stdscr, 24, 9, "%s", "|");
    mvwprintw(stdscr, 24, 12, "%s", |");
    mvwprintw(stdscr, 25, 10, "%s", "--");
    mvwprintw(stdscr, 23, 10, "%s", "--");

    mvwprintw(stdscr, 22, 9, "%s", "|");
    mvwprintw(stdscr, 22, 12, "%s", "|");
    mvwprintw(stdscr, 21, 10, "%s", "--"); 

    mvwprintw(stdscr, 22, 11, "%s", "x");

    mvwprintw(stdscr, 21, 13, "%s", "--");
    mvwprintw(stdscr, 23, 13, "%s", "--");
    mvwprintw(stdscr, 22, 15, "%s", "|");
    */

    /*
     * Vertical-Neighbor:
     *     y + 2, x (y's)
     *     y - 2, x
     *
     *     y + 1, x + 1 (x's)
     *     y - 1, x + 1
     *     y + 1, x - 2 
     *     y - 1, x - 2 
     *
     */
    /* Horizontal-Neighbor:
     *     y, x + 3 (x's)
     *     y, x - 3
     *
     *     y + 1, x + 2 (y's)
     *     y - 1, x + 2
     *     y + 1, x - 1
     *     y - 1, x - 1
     */
    int max_x, max_y;
    getmaxyx(stdscr, max_y, max_x);

    Maze m(max_x, max_y);
    
    refresh();
    sleep(100);
    destroy_screen();

    return 0;
}

