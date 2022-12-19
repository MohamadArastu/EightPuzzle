# Misplaced Tiles - Heuristic Function

def print_in_matrix(matrix):  # correct 3x3 Matrix
    for i in range(9):
        if i % 3 == 0 and i > 0:
            print("")
        print(str(matrix[i]) + " ", end="")


def count(n):  # Counts the amount of misplaced tiles
    c = 0
    goal = [1, 2, 3,
            4, 5, 6,
            7, 0, 8]
    # goal is our solved puzzle to be compared to

    for i in range(9):
        if n[i] != 0 and n[i] != goal[i]:
            # s[i] != 0 ensures that Zero won't count as heuristic value because 0 is just the empty space
            c += 1
    # counts the total number of tiles that are not in the correct place
    return c


def move(ar, p, st):
    rh = 9999  # max value of heuristic
    store_st = st.copy()  # state copy to store the state

    for i in range(len(ar)):

        dupl_st = st.copy()  # state duplication

        # swapping the value of 0 with the value of the position of 0
        temp = dupl_st[p]
        dupl_st[p] = dupl_st[arr[i]]
        dupl_st[arr[i]] = temp

        temp_rh = count(dupl_st)  # calculation of the heuristic state

        if temp_rh < rh:
            rh = temp_rh  # replace the heuristic
            store_st = dupl_st.copy()  # replace the state

    return store_st, rh  # return the heuristic and the state


start = [1, 2, 3,
         5, 0, 6,
         4, 7, 8]
# starting point of the 8-puzzle

h = count(start)  # h = heuristic value
Level = 1

print("\nLevel " + str(Level))
print_in_matrix(start)
print("\nHeuristic Value(Misplaced) : " + str(h))

while h > 0:
    pos = int(start.index(0))

    Level += 1

    # in a 3x3 Matrix at Position X the empty space can move either right, left, down or up depending on the position
    if pos == 0:
        arr = [1, 3]
        start, h = move(arr, pos, start)
    elif pos == 1:
        arr = [0, 2, 4]
        start, h = move(arr, pos, start)
    elif pos == 2:
        arr = [1, 5]
        start, h = move(arr, pos, start)
    elif pos == 3:
        arr = [0, 4, 6]
        start, h = move(arr, pos, start)
    elif pos == 4:
        arr = [1, 3, 5, 7]
        start, h = move(arr, pos, start)
    elif pos == 5:
        arr = [2, 4, 8]
        start, h = move(arr, pos, start)
    elif pos == 6:
        arr = [3, 7]
        start, h = move(arr, pos, start)
    elif pos == 7:
        arr = [4, 6, 8]
        start, h = move(arr, pos, start)
    elif pos == 8:
        arr = [5, 6]
        start, h = move(arr, pos, start)

    print("\nLevel " + str(Level))
    print_in_matrix(start)
    print("\nHeuristic Value(Misplaced) : " + str(h))
