from block import Block
from predicate import Predicate
from action import Action
from input import read_input

"""
Print the a given state
"""
def represent(state_dict):
  # find the width
  width = 0
  table_blocks = []
  for b in state_dict.values():
    if b.ontable():
      width += 1
      table_blocks.append(b)

  # initialize list with size with to 0
  heights = [1 for i in range(width)]

  # find the height
  for i in range(len(table_blocks)):
    b = table_blocks[i]
    while b.up != None:
      heights[i] += 1
      b = b.up

  max_height = max(heights)
  side = max(width, max_height)
  field = [[' ' for x in range(side)] for y in range(side)]
  for x in range(len(table_blocks)):
    b = table_blocks[x]
    y = 0
    while b != None:
      field[x][y] = str(b.value)
      b = b.up
      y += 1

  for y in range(side - 1, -1, -1):
    values = []
    for x in range(side):
      values.append(field[x][y])
    print ' '.join(values)
  print


current, goal = read_input()


arm = None
predicate_stack = []
steps = []
# convert goals to predicates
for b in goal.values():
  predicate_stack.extend(b.predicates())

predicate_stack.insert(0, predicate_stack[:])

represent(current)

while len(predicate_stack) > 0:
  # print predicate_stack, "arm: ", arm
  top = predicate_stack[-1]
  # print type(top)
  if type(top) is Predicate:
    # predicate
    statisfy = top.check(current, arm)
    if statisfy:
      predicate_stack.pop()
    else:
      correction = top.correction(current, arm)
      preconds = correction.preconditions(current)
      predicate_stack.append(correction)
      predicate_stack.extend(preconds)
  elif type(top) is Action:
    # action
    arm = top.perform(current)
    predicate_stack.pop()
    steps.append(str(top))
    represent(current)
  elif type(top) is list:
    # conjuction predicate
    # why we need this?
    # because some conditions are cleared but due to the order of clearing it does not mean all the 
    # conditions are met before the action / end of stack
    statisfy = True
    for predicate in top:
      if not predicate.check(current, arm):
        predicate_stack.append(predicate)
        statisfy = False

    if statisfy:
      predicate_stack.pop()
  # raw_input()

print steps