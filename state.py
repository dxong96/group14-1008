import input
from block import Block

class State(object):
  limit = -1
  """Contains the state for the blocks"""
  def __init__(self, state):
    super(State, self).__init__()
    self.state = state
    self.arm = None

  def onTableBlocks(self):
    return filter(Block.ontable, self.state.values())
    
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

  def dump(self, blank=' '):
    # find the width
    table_blocks = []
    for b in self.state.values():
      if b.ontable():
        table_blocks.append(b)

    width = len(table_blocks)
    
    # initialize list with size with to 1
    heights = [1 for i in range(width)]

    # find the height
    for i in range(len(table_blocks)):
      b = table_blocks[i]
      while b.up != None:
        heights[i] += 1
        b = b.up

    max_height = max(heights)
    field = [[blank for x in range(width)] for y in range(max_height)]
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
    new_state = input.read_state(self.dump(None))
    new_state.arm = self.arm
    new_state.limit = self.limit
    if self.arm != None:
      b = Block(self.arm, None, None)
      b.held = True
      new_state.state[self.arm] = b

    return new_state

  def __eq__(self, other):
    """Overrides the default implementation"""
    if isinstance(other, State):
        return self.arm == other.arm and self.dump() == other.dump()
    return False

  def __ne__(self, other):
    """Overrides the default implementation (unnecessary in Python 3)"""
    return not self.__eq__(other)