import input

class State(object):
  """Contains the state for the blocks"""
  def __init__(self, state):
    super(State, self).__init__()
    self.state = state
    self.arm = None
    
  """
  Print the state
  """
  def printState(self):
    field = self.dump()

    for row in field:
      print ' '.join(row)
    print

  def predicates(self):
    predicates = []
    for b in self.state.values():
      predicates.extend(b.predicates())

    predicates.insert(0, predicates[:])
    return predicates

  def dump(self):
    # find the width
    width = 0
    table_blocks = []
    for b in self.state.values():
      if b.ontable():
        width += 1
        table_blocks.append(b)

    # initialize list with size with to 1
    heights = [1 for i in range(width)]

    # find the height
    for i in range(len(table_blocks)):
      b = table_blocks[i]
      while b.up != None:
        heights[i] += 1
        b = b.up

    max_height = max(heights)
    field = [[' ' for x in range(width)] for y in range(max_height)]
    for x in range(len(table_blocks)):
      b = table_blocks[x]
      y = 0
      while b != None:
        field[y][x] = str(b.value)
        b = b.up
        y += 1

    field.reverse()
    return tuple(map(tuple, field))


  def clone(self):
    new_state = input.read_state(self.dump())
    new_state.arm = self.arm
    return new_state