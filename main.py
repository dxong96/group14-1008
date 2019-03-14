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
      ontable_blocks = current.onTableBlocks()
      if current.limit == -1 or len(ontable_blocks) < current.limit:
        # unlimited spaces or limit not reached
        current.arm = top.perform(current.state)
        predicate_stack.pop()
        steps.append(top)
        print "Action performed: %s" % str(top)
      else:
        # limited space
        if top.name == 'putdown':
          # action is putdown
          # check the last stack step
          # it cannot be a pickup step as picking up will leave a empty space
          previous_action = steps[-1]
          from_block = previous_action.args[1]
          # get top blocks that is not the from block
          top_blocks = filter(Block.clear, current.state.values())
          for i in range(len(top_blocks)):
            if top_blocks[i].value == from_block:
              del top_blocks[i]
              break

          # try to stack on top blocks and check if action will be undone
          for b in top_blocks:
            stack_action = Action('stack', (top.args[0], b.value))
            next_action = calculate_next_action(current, predicate_stack, stack_action)
            unstack_action = Action('unstack', stack_action.args)
            if next_action != unstack_action:
              current.arm = stack_action.perform(current.state)
              predicate_stack.pop()
              steps.append(stack_action)
              print "Action performed: %s" % str(stack_action)
              break
        else:
          current.arm = top.perform(current.state)
          predicate_stack.pop()
          steps.append(top)
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
  # print steps
  print cleanup_steps(steps)
  print "Total number steps:", len(steps)

def calculate_next_action(state, predicate_stack, action):
  state = state.clone()
  predicate_stack = predicate_stack[:-1]
  print 'calculating next action, start predicate: ', predicate_stack
  state.arm = action.perform(state.state)
  while len(predicate_stack) > 0:
    top = predicate_stack[-1]
    if type(top) is Predicate:
      statisfy = top.check(state.state, state.arm)
      if statisfy:
        predicate_stack.pop()
      else:
        correction = top.correction(state.state, state.arm)
        preconds = correction.preconditions(state.state)
        predicate_stack.append(correction)
        predicate_stack.extend(preconds)
    elif type(top) is Action:
      print 'next action: ', top
      return top
    elif type(top) is list:
      statisfy = True
      for predicate in top:
        if not predicate.check(state.state, state.arm):
          predicate_stack.append(predicate)
          statisfy = False

      if statisfy:
        predicate_stack.pop()
    # raw_input()
  return None

def cleanup_steps(steps):
  i = 0
  size = len(steps)
  while i < size - 1:
    current_step = steps[i]
    opposite_step = current_step.undoing_action()
    next_step = steps[i + 1]
    if opposite_step == next_step:
      del steps[i:i+2]
      size -= 2
      i -= 1
      continue
    i += 1
  return steps


# goal_stack_planning()



result = breath_first_search(start, goal)
if result == None:
  print 'no result'
else:
  print result
