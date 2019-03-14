from stack_node import StackNode
import action

class Predicate(StackNode):
  name = ""
  args = None

  def __init__(self, name, args):
    StackNode.__init__(self, "predicate", name, args)

  def check(self, current, arm):
    # maximum 2 args
    a = None
    b = None
    arg_len = len(self.args)

    if arg_len > 0:
      a = current[self.args[0]]

    if arg_len > 1:
      b = current[self.args[1]]

    if self.name == 'on':
      # block A is on block B
      return a.on(b)
    elif self.name == 'ontable':
      # block A is on the table
      return a.ontable()
    elif self.name == 'clear':
      # block A has nothing on it
      return a.clear()
    elif self.name == 'holding':
      # arm is holding block A
      return arm == a.value
    elif self.name == 'armempty':
      # arm is empty
      return arm == None

  def correction(self, current, arm):
    # when the predicate is not met 
    # create an action to fix it
    # maximum 2 args
    a = None
    b = None
    a_value = None
    b_value = None
    arg_len = len(self.args)

    if arg_len > 0:
      a = current[self.args[0]]
      a_value = a.value

    if arg_len > 1:
      b = current[self.args[1]]
      b_value = b.value

    if self.name == 'on':
      # block A is on block B
      return action.Action('stack', (a_value, b_value))
    elif self.name == 'ontable':
      # block A is on the table
      return action.Action('putdown', (a_value,))
    elif self.name == 'clear':
      # block A has nothing on it
      return action.Action('unstack', (a.up.value, a.value))
    elif self.name == 'holding':
      # arm is holding block A
      if a.ontable():
        return action.Action('pickup', (a_value,))
      else:
        return action.Action('unstack', (a_value, a.below.value))
    elif self.name == 'armempty':
      # arm is empty
      return action.Action('putdown', (arm,))

    return []

  def __repr__(self):
    params = ', '.join(map(str, self.args))
    return '%s(%s)' % (self.name, params)