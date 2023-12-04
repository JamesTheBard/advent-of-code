# Let's get all of the lines of the input file read into memory as a list of
# strings and dump it into data.
#
with open('input.txt', 'r') as f:
    data = [i for i in f.readlines()]

# Let's get those moves into something a bit more comfortable.  Grab
# every-other element (starting with element 1), convert it to an
# integer, then toss that array into a larger array.
#
# "move 2 from 5 to 9" -.    [[ 2, 5, 9 ],
# "move 3 from 1 to 7"  |-->  [ 3, 1, 7 ],
# "move 2 from 3 to 9" -'     [ 2, 3, 9 ]]
#
moves = [[int(j) for j in i.strip().split()[1::2]] for i in data[10:]]

# Now, let's take the first 9 lines of the unprocessed data and make a
# matrix.  The ultimate goal is to make 9 actual programming stacks where
# the top box is on the bottom of the stack.  This will allow us to pop
# items off the list which is a perfect emulation of a crane pulling a box
# off a stack of boxes.
#
# 1. So, we make a matrix of the boxes where each row is the row in the
#    current state.  Not very useful, but it's a start.
#
# 2. Let's transpose the matrix.  This means that instead of each row being
#    a row of boxes, each row is now a stack of boxes.  Unfortunately, we're
#    still not done yet as pop()-ing one of the stacks will give us the bottom
#    box of that physical stack.
#
# 3. Now reverse every stack (row).  This means that when we pop a box off a
#    stack, it will be the top box of the stack!  I also remove all the empty
#    elements in this step as they would be the first things pop()-ed off the
#    stack when we start moving stuff.
#
#      DATA             MAKE MATRIX         TRANSPOSE MATRIX      INVERT STACKS/CLEANUP
#---------------------------------------------------------------------------------------
#     [D]     -.    [[ " ", "D", " " ],    [[ " ", "N", "Z" ],    [[ "Z", "N" ],
# [N] [C]      |-->  [ "N", "C", " " ], ->  [ "D", "C", "M" ], ->  [ "M", "C", "D" ],
# [Z] [M] [P] -'     [ "Z", "M", "P" ]]     [ " ", " ", "P" ]]     [ "P" ]]
#  1   2   3  
def create_state(data: list[str]) -> list[list[str]]:
    state = [list(i[1::4]) for i in data[:8]] # (1)
    state = [[state[j][i] for j in range(len(state))] for i in range(len(state[0]))] # (2)
    return [[j for j in i if j != " "][::-1] for i in state] # (3)

# For the output, get the box on the top of every column, jam them together
# as a string, and return it.
def get_final_state(state: list[list[str]]) -> str:
    return ''.join([[j for j in i][-1] for i in state])

# Part One
#
# So, create the state, then loop through all the moves.  For each source and
# destination, we pop a box off of the source stack and put it on the
# destination stack a number of times equal to 'num'.  Pretty simple and
# straightforward.
#
state = create_state(data)
for m in moves:
    src, dst, num = m[1] - 1, m[2] - 1, m[0]
    [state[dst].append(state[src].pop()) for _ in range(0, num)]
    
print(get_final_state(state))

# Part Two
#
# Welp, we can't really use the pop() method for this, so let's have fun with
# slices!  So, remove 'num' number of boxes from a stack (which preserves order)
# and then tack them onto the destination stack while making sure we actually
# remove them from the source stack.
#
state = create_state(data)
for m in moves:
    src, dst, num = m[1] - 1, m[2] - 1, m[0]
    removed_boxes = state[src][-num:]
    del state[src][-num:]
    state[dst].extend(removed_boxes)

print(get_final_state(state))
