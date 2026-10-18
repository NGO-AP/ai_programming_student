"""
Oefening 2: Breadth-First Search
=================================
Implementeer BFS met backward printing van het pad.
"""
from collections import deque


class State:
    def __init__(self, name):
        self.name = name


class Node:
    def __init__(self, state):
        self.state = state
        self.actions = []

    def add_action(self, action):
        self.actions.append(action)


def breadth_first_search(initial_node, goal_state):
    # TODO: implementeer BFS met een queue
    # HINT: gebruik parent-tracking om het pad te reconstrueren
    frontier = deque([initial_node])
    visited = set([initial_node])
    parent = {initial_node.state.name: None}

    while frontier:
        node = frontier.popleft()

        if node.state.name == goal_state.name:
            return print_path(parent, node)

        visited.add(node)

        for neighbour in node.actions:
            if neighbour not in visited:
                frontier.append(neighbour)
                if neighbour.state.name not in parent:
                    parent[neighbour.state.name] = node

    return None


def print_path(parent, goal_node):
    # TODO: print het pad van start naar goal (backward printing)
    path = []
    node = goal_node
    while True:
        path.append(node.state.name)
        next_node = parent[node.state.name]
        if next_node is not None:
            node = next_node
        else:
            break
    path.reverse()
    return " -> ".join(path)
        


if __name__ == "__main__":
    # Graaf opbouwen
    state_a = State("A")
    state_b = State("B")
    state_c = State("C")
    state_d = State("D")
    state_e = State("E")
    state_f = State("F")
    state_h = State("H")

    node_a = Node(state_a)
    node_b = Node(state_b)
    node_c = Node(state_c)
    node_d = Node(state_d)
    node_e = Node(state_e)
    node_f = Node(state_f)
    node_h = Node(state_h)

    node_a.add_action(node_b)
    node_a.add_action(node_c)
    node_b.add_action(node_d)
    node_b.add_action(node_e)
    node_c.add_action(node_f)
    node_f.add_action(node_h)

    solution = breadth_first_search(node_a, state_h)
    if solution:
        print("Oplossing gevonden! Doel:", solution)
    else:
        print("Geen oplossing.")


"""
Oefening 2: Sliding Puzzle (8-puzzle)
======================================
Implementeer de sliding puzzle en los hem op met BFS/DFS.
"""
import numpy as np


class SlidingPuzzle:
    GRIDSIZE = 3
    EMPTY = 0

    GOAL = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]

    def __init__(self, game):
        self.Game = np.array(game)

    def possible_new_configurations(self):
        # TODO: geef alle nieuwe configuraties door het lege vakje te verschuiven
        configurations = []
        possible_moves = [
            (-1,0),
            (1,0),
            (0,1),
            (0,-1)]

        r, c = self.locate_empty()

        for dr, dc in possible_moves:
            new_r, new_c = r+dr, c+dc
            if 0 <= new_r < self.GRIDSIZE and 0 <= new_c < self.GRIDSIZE:
                new_configuration = self.duplicate().Game
                new_configuration[r][c], new_configuration[new_r][new_c] = new_configuration[new_r][new_c], new_configuration[r][c]
                configurations.append(SlidingPuzzle(new_configuration))
        
        return configurations

    def locate_empty(self):
        for row in range(self.GRIDSIZE):
            for col in range(self.GRIDSIZE):
                if self.Game[row][col] == self.EMPTY:
                    return (row, col)
        raise Exception("Geen leeg vakje!")

    def manhattan_distance(self):
        # TODO: bereken de Manhattan-afstand tot de goal-configuratie
        cost = 0

        for r in range(self.GRIDSIZE):
            for c in range(self.GRIDSIZE):
                value = self.Game[r][c]
                if value != 0:
                    goal_r, goal_c = np.argwhere(np.array(self.GOAL) == value)[0]
                    cost += abs(goal_r - r) + abs(goal_c - c)
        
        return cost

    def is_goal(self):
        return np.array_equal(self.Game, self.GOAL)

    def duplicate(self):
        return SlidingPuzzle([[self.Game[r][c] for c in range(self.GRIDSIZE)] for r in range(self.GRIDSIZE)])

    def log(self):
        print("---")
        for row in self.Game:
            print(", ".join(str(int(x)) for x in row))
        print("---")

def to_hashable(state):
    return tuple(tuple(row) for row in state)


def solve_puzzle(start_puzzle):
    # TODO: los de puzzel op met BFS
    frontier = deque([start_puzzle])
    visited = set([to_hashable(start_puzzle.Game)])

    while frontier:
        node = frontier.popleft()

        if node.is_goal():
            return node

        visited.add(to_hashable(node.Game))

        for neighbour in node.possible_new_configurations():
            if to_hashable(neighbour.Game) not in visited:
                frontier.append(neighbour)

    return None


if __name__ == "__main__":
    game = [
        [1, 2, 3],
        [4, 5, 0],
        [7, 8, 6]
    ]
    puzzle = SlidingPuzzle(game)
    print("Startconfiguratie:")
    puzzle.log()

    oplossing = solve_puzzle(puzzle)
    print("Oplossing:")
    oplossing.log()

"""
Oefening 3: Maze met DFS
=========================
Implementeer DFS om een weg door het maze te vinden.
"""
import numpy as np


class Maze:
    def __init__(self, size, start, end, walls):
        self.size = size
        self.start = start
        self.end = end
        self.maze = np.zeros(size, dtype=str)
        self.maze[:, :] = '.'
        self.maze[start] = 'S'
        self.maze[end] = 'E'
        self.rows, self.cols = size
        for wall in walls:
            self.maze[wall] = '#'

    def valid_moves(self, current):
        # TODO: geef lijst van (rij,kolom)-coördinaten die geldig zijn
        new_positions = []
        possible_moves = [
            (-1,0),
            (1,0),
            (0,-1),
            (0, 1)]

        r, c = current

        for dr, dc in possible_moves:
            new_r, new_c = r + dr, c + dc
            if 0 <= new_r < self.rows and 0 <= new_c < self.cols and self.maze[new_r, new_c] != '#':
                new_positions.append((new_r, new_c))

        return new_positions

    def extract_path(self, stack):
        # TODO: haal het pad uit de stack van start tot end
        if not stack:
            return
        for r, c in stack:
            if self.maze[r, c] not in ['S', 'E']:
                self.maze[r, c] = 'o'

    def print_maze(self):
        for row in self.maze:
            print(' '.join(row))


def find_path(maze):
    # TODO: implementeer DFS met een stack
    frontier = deque([[maze.start]])
    visited = set([maze.start])
    stappen = 0

    while frontier:

        path = frontier.pop()
        node = path[-1]
        stappen += 1
        if node == maze.end:
            return path, stappen

        for neighbour in maze.valid_moves(node):
            if neighbour not in visited:
                frontier.append(path + [neighbour])
                visited.add(neighbour)

    return None, stappen


if __name__ == "__main__":
    maze_size = (10, 10)
    start_point = (0, 0)
    end_point = (9, 9)
    walls = [(2, 1), (2, 2), (2, 3), (4, 6), (6, 6), (7, 6), (8, 6),
             (4, 7), (4, 8), (2, 2), (5, 2), (6, 2), (4, 2), (3, 2),
             (8, 0), (9, 6), (1, 8), (2, 8), (6, 9), (7, 9),
             (3, 6), (3, 7), (4, 1), (5, 1)]

    my_maze = Maze(maze_size, start_point, end_point, walls)
    pad, stappen = find_path(my_maze)

    if pad:
        my_maze.extract_path(pad)

    my_maze.print_maze()
    print("Pad:", pad)
    print("Stappen:", stappen)