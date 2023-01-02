# Eight Puzzle Problem (Comparison of Hamming and Manhattan Distance)
import heapq
import sys
import random
import time
import statistics


# Class representing a puzzle state
class State:

    def __init__(self, grid, moves):
        # Array with current grid
        self.grid = grid
        # number og moves to get from initial state to current state
        self.moves = moves

        self.pos = int(self.grid.index(0))

    # Definition of "<" operator
    # Needed to add new state to heap when another state in the heap has the same cost function
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

    # Returns array of possible moves considering the current state
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
            # state duplication
            grid_copy = self.grid.copy()

            # swapping the value of 0 with the value of the position of 0
            grid_copy[pos] = self.grid[arr[i]]
            grid_copy[arr[i]] = 0
            next_states.append(State(grid_copy, self.moves + 1))

        # return the possible new states
        return next_states


# Heap containing all expanded nodes, node with minimum total costs is at the top and is removed by pop function
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
    sum = 0
    for count, tile in enumerate(state.grid):
        if count == tile:
            sum += 1
    return len(state.grid) - sum


# Sums up the deviations of all tiles from its goal state
def manhattan_distance(state):
    sum = 0
    for count, tile in enumerate(state.grid):
        sum += abs(tile % 3 - count % 3) + abs(tile // 3 - count // 3)
    return sum


# Here the actual search is performed
def search(state, cost_function):
    # History is containing all expanded nodes
    history = []
    queue = PriorityQueue(cost_function)
    # Intitial state is pushe to heap
    queue.push(state)
    history = set([str(state.grid)])

    while not queue.empty():
        state = queue.pop()
        if state.is_goal_state():
            # Goal state has been found
            return (state, len(history))

        for st in state.get_next_states():
            grid = str(st.grid)
            # Check whether node is already known
            if grid not in history:
                # New node is added to history
                history.add(grid)
                # New node is pushed to heap
                queue.push(st)
            else:
                # Node is already known and can be deleted
                del st
    return None


# A utility function to count Inversions in given array 'arr[]'
def getInvCount(arr):
    inv_count = 0
    empty_value = 0
    for i in range(0, 9):
        for j in range(i + 1, 9):
            if arr[j] != empty_value and arr[i] != empty_value and arr[i] > arr[j]:
                inv_count += 1
    return inv_count


# This function returns true if given 8 puzzle is solvable.
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


# Random node is generated
def get_random_start_node():
    options = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    random_node = []

    while len(options) > 0:
        c = random.choice(options)
        random_node.insert(0, c)
        options.remove(c)

    return random_node


# Array of random nodes is generated (only containing solveable puzzles)
def get_random_start_nodes(n):
    start_nodes = []

    while len(start_nodes) < n:
        node = get_random_start_node()
        if (isSolvable(node) and node not in start_nodes):
            start_nodes.append(node)
    return start_nodes


if __name__ == '__main__':
    # Number of puzzles to be solved
    number_of_puzzles = 10
    # Creation of random puzzles array
    start_nodes = get_random_start_nodes(number_of_puzzles)
    # Array to store number of extended nodes per puzzle
    expanded_nodes = []
    # Array to store execution time per puzzle
    time_per_node = []

    # Cost functions: total costs = number of actions to get to current state + heuristic value to reach final state
    cost_hamming = lambda state: state.moves + hamming_distance(state)
    cost_manhattan = lambda state: state.moves + manhattan_distance(state)

    # Solving all puzzles
    for node in start_nodes:
        start = time.time()
        solution, history_length = search(State(node, 0), cost_hamming)
        expanded_nodes.append(history_length)
        end = time.time()
        time_per_node.append(end - start)

    # Presentation of the performance of the hamming heuristic
    print("Hamming heuristic:")
    print("Mean Time per Puzzle: " + str(statistics.mean(time_per_node)) + "s")
    print("Standard Deviation of Time per Puzzle: " + str(statistics.stdev(time_per_node)) + "s")
    print("Mean Value (Expanded Nodes): " + str(statistics.mean(expanded_nodes)) + " nodes")
    print("Standard Deviation (Expanded Nodes): " + str(statistics.stdev(expanded_nodes)) + " nodes")
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

    # Clearing arrays for new heuristic
    expanded_nodes.clear()
    time_per_node.clear()
    # Solving all puzzles
    for node in start_nodes:
        start = time.time()
        solution, history_length = search(State(node, 0), cost_manhattan)
        expanded_nodes.append(history_length)
        end = time.time()
        time_per_node.append(end - start)

    # Presentation of the performance of the manhattan heuristic
    print("Manhattan heuristic:")
    print("Mean Time per Puzzle: " + str(statistics.mean(time_per_node)) + "s")
    print("Standard Deviation of Time per Puzzle: " + str(statistics.stdev(time_per_node)) + "s")
    print("Mean Value (Expanded Nodes): " + str(statistics.mean(expanded_nodes)) + " nodes")
    print("Standard Deviation (Expanded Nodes): " + str(statistics.stdev(expanded_nodes)) + " nodes")
