from block import Block
from predicate import Predicate
from action import Action
from input import read_input
from bfs import breath_first_search


start, goal = read_input()

"""
Solve the steps for start to end using goal stack planning
"""
def goal_stack_planning():
  # we clone because it might be used later on
  current = start.clone()
  predicate_stack = []
  steps = []
  # convert goals to predicates
  predicate_stack.extend(goal.predicates())

  print "Starting state:"
  current.printState()
  print "====================="

  while len(predicate_stack) > 0:
    # current.printState()
    # print "stack: ", predicate_stack
    # print "arm: ", current.arm
    # print "steps:", steps
    top = predicate_stack[-1]
    # print type(top)
    if type(top) is Predicate:
      # predicate
      statisfy = top.check(current.state, current.arm)
      if statisfy:
        predicate_stack.pop()
      else:
        correction = top.correction(current.state, current.arm)
        preconds = correction.preconditions(current.state)
        predicate_stack.append(correction)
        predicate_stack.extend(preconds)
    elif type(top) is Action:
      # action
      current.arm = top.perform(current.state)
      predicate_stack.pop()
      steps.append(str(top))
      print "Action performed: %s" % str(top)
      print "State:"
      current.printState()
      print "Arm: %s" % current.arm
      print "====================="
    elif type(top) is list:
      # conjuction predicate
      # why we need this?
      # because some conditions are cleared but due to the order of clearing it does not mean all the 
      # conditions are met before the action / end of stack
      statisfy = True
      for predicate in top:
        if not predicate.check(current.state, current.arm):
          predicate_stack.append(predicate)
          statisfy = False

      if statisfy:
        predicate_stack.pop()
    # raw_input()

  print steps

def bfs():
  current = start.clone()
  steps = breath_first_search(start, goal)
  if steps == None:
    return

  for step in steps:
    arm = step.perform(current.state)
    print "Action performed: %s" % str(step)
    print "State:"
    current.printState()
    print "Arm: %s" % arm
    print "====================="

  print steps


if __name__ == '__main__':
  try: input = raw_input
  except NameError: pass

  print 'Please choose which algorithm to use:'
  print '1. Goal Stack Algorithm, Limited space not implemented'
  print '2. Breadth first search, Limited space implemented\n'
  
  while True:
    ui = input('Enter your choice: ')
    if ui == '1':
      goal_stack_planning()
      break
    elif ui == '2':
      bfs()
      break

    print 'Please enter 1 or 2'

