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
    # find the width
    width = 0
    table_blocks = []
    for b in self.state.values():
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

  def predicates(self):
    predicates = []
    for b in self.state.values():
      predicates.extend(b.predicates())

    predicates.insert(0, predicates[:])
    return predicates