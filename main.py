# Eight Puzzle Problem (Comparison of Hamming and Manhattan Distance)
import heapq
import sys
import random
import time
import statistics


class State:

    def __init__(self, grid, moves):
        self.grid = grid
        self.moves = moves
        self.pos = int(self.grid.index(0))

    def __lt__(self, other):
        if self.moves < other.moves:
            return True
        return False

    def __eq__(self, other):
        if self.grid == other.grid:
            return True
        return False

    # Prints current state
    def print_grid(self):
        for i in range(9):
            if i % 3 == 0 and i > 0:
                print("")
            print(str(self.grid[i]) + " ", end="")
        print("")

    # Check whether goal state has been reached
    def is_goal_state(self):
        for i in range(9):
            if self.grid[i] != i:
                return False
        return True

    # Returns array of possible moves from given state
    def get_next_states(self):
        next_states = []

        pos = self.pos

        if pos == 0:
            arr = [1, 3]
        elif pos == 1:
            arr = [0, 2, 4]
        elif pos == 2:
            arr = [1, 5]
        elif pos == 3:
            arr = [0, 4, 6]
        elif pos == 4:
            arr = [1, 3, 5, 7]
        elif pos == 5:
            arr = [2, 4, 8]
        elif pos == 6:
            arr = [3, 7]
        elif pos == 7:
            arr = [4, 6, 8]
        elif pos == 8:
            arr = [5, 6]

        for i in range(len(arr)):
            grid_copy = self.grid.copy()  # state duplication

            # swapping the value of 0 with the value of the position of 0
            grid_copy[pos] = self.grid[arr[i]]
            grid_copy[arr[i]] = 0
            next_states.append(State(grid_copy, self.moves + 1))

        return next_states  # return the possible new states


class PriorityQueue:
    def __init__(self, heuristic_function):
        self.heuristic_function = heuristic_function
        self.heap = []

    def push(self, item):
        # print(self.heuristic_function(item))
        heapq.heappush(self.heap, (self.heuristic_function(item), item))

    def pop(self):
        (_, item) = heapq.heappop(self.heap)
        return item

    def empty(self):
        return len(self.heap) == 0


# Counts the number of misplaced tiles
def hamming_distance(state):
    return len([i for i in range(len(state.grid)) if state.grid[i] != 0 and state.grid[i] != i + 1])


# Sums up the deviations of all tiles from goal state
def manhattan_distance(state):
    def distance(i):
        return 0 if state.grid[i] == 0 else abs(((state.grid[i] - 1) / 3) - (i / 3)) + abs(
            ((state.grid[i] - 1) % 3) - (i % 3))

    return sum(distance(i) for i in range(len(state.grid)))


def search(state, cost_function):
    history = []
    queue = PriorityQueue(cost_function)
    queue.push(state)
    history = set([str(state.grid)])

    while not queue.empty():
        state = queue.pop()
        if state.is_goal_state():
            return (state, len(history))

        for st in state.get_next_states():
            grid = str(st.grid)
            if grid not in history:
                # print(st.grid)
                history.add(grid)
                queue.push(st)
            else:
                del st
    return None


# A utility function to count
# inversions in given array 'arr[]'
def getInvCount(arr):
    inv_count = 0
    empty_value = 0
    for i in range(0, 9):
        for j in range(i + 1, 9):
            if arr[j] != empty_value and arr[i] != empty_value and arr[i] > arr[j]:
                inv_count += 1
    return inv_count


# This function returns true
# if given 8 puzzle is solvable.
# https://www.geeksforgeeks.org/check-instance-8-puzzle-solvable/
def isSolvable(node):
    puzzle = []
    puzzle.append(node[0:3])
    puzzle.append(node[3:6])
    puzzle.append(node[6:9])

    # Count inversions in given 8 puzzle
    inv_count = getInvCount([j for sub in puzzle for j in sub])

    # return true if inversion count is even.
    return inv_count % 2 == 0


def get_random_start_node():
    options = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    random_node = []

    while len(options) > 0:
        c = random.choice(options)
        random_node.insert(0, c)
        options.remove(c)

    return random_node


def get_random_start_nodes(n):
    start_nodes = []

    while len(start_nodes) < n:
        node = get_random_start_node()
        if (isSolvable(node) and node not in start_nodes):
            start_nodes.append(node)
    return start_nodes


if __name__ == '__main__':
    number_of_puzzles = 2
    start_nodes = get_random_start_nodes(number_of_puzzles)
    expanded_nodes = []
    time_per_node = []

    cost_hamming = lambda state: state.moves + hamming_distance(state)
    cost_manhattan = lambda state: state.moves + manhattan_distance(state)

    for node in start_nodes:
        start = time.time()
        solution, history_length = search(State(node, 0), cost_hamming)
        expanded_nodes.append(history_length)
        end = time.time()
        time_per_node.append(end - start)

    print("Hamming heuristic:")
    print("Mean Time per Puzzle: " + str(statistics.mean(time_per_node)) + "s")
    print("Standard Deviation of Time per Puzzle: " + str(statistics.stdev(time_per_node)) + "s")
    print("Mean Value (Expanded Nodes): " + str(statistics.mean(expanded_nodes)) + " nodes")
    print("Standard Deviation (Expanded Nodes): " + str(statistics.stdev(expanded_nodes)) + " nodes")
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")


    expanded_nodes.clear()
    time_per_node.clear()
    for node in start_nodes:
        start = time.time()
        solution, history_length = search(State(node, 0), cost_manhattan)
        expanded_nodes.append(history_length)
        end = time.time()
        time_per_node.append(end - start)

    print("Manhattan heuristic:")
    print("Mean Time per Puzzle: " + str(statistics.mean(time_per_node)) + "s")
    print("Standard Deviation of Time per Puzzle: " + str(statistics.stdev(time_per_node)) + "s")
    print("Mean Value (Expanded Nodes): " + str(statistics.mean(expanded_nodes)) + " nodes")
    print("Standard Deviation (Expanded Nodes): " + str(statistics.stdev(expanded_nodes)) + " nodes")

