'''
Breadth first search algorithm
implemented according to 
https://en.wikipedia.org/wiki/Breadth-first_search#Pseudocode
'''
from action import Action
from collections import deque

def breath_first_search(start, goal):
  open_set = deque()
  closed_set = set()

  meta = {}
  meta[start] = (None, None)
  open_set.append(start)

  while len(open_set) > 0:
    subtree_root = open_set.popleft()

    if subtree_root == goal:
      return construct_path(subtree_root, meta)

    for (child, action) in get_sucessors(subtree_root):
      if child in closed_set:
        continue

      if child not in open_set:
        meta[child] = (subtree_root, action)
        open_set.append(child)
    
    closed_set.add(subtree_root)

def get_sucessors(current_state):
  clear_blocks = filter(lambda b: b.clear(), current_state.state.values())

  actions = []
  if current_state.arm == None:
    # unstack, pickup
    for b in clear_blocks:
      if b.ontable():
        actions.append(Action("pickup", (b.value,)))
      else:
        actions.append(Action("unstack", (b.value, b.below.value)))
  else:
    # stack, putdown
    actions.append(Action("putdown", (current_state.arm,)))
    for b in clear_blocks:
      actions.append(Action("stack", (current_state.arm, b.value)))


  result = []
  for action in actions:
    s = current_state.clone()
    s.arm = action.perform(s.state)
    s.printState()
    print "action performed", action
    print "arm: ", s.arm
    print "====next===="

    result.append((s, action))

  return result

# Produce a backtrace of the actions taken to find the goal node, using the 
# recorded meta dictionary
def construct_path(state, meta):
  action_list = list()
  
  # Continue until you reach root meta data (i.e. (None, None))
  while meta[state][0] is not None:
    state, action = meta[state]
    action_list.append(action)
  
  action_list.reverse()
  return action_list