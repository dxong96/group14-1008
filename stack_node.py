class StackNode(object):
  name = ""
  args = None

  """docstring for StackNode"""
  def __init__(self, type, name, args):
    super(StackNode, self).__init__()
    self.type = type
    self.name = name
    self.args = args
  
  def __eq__(self, other):
      """Overrides the default implementation"""
      if isinstance(other, StackNode):
          return self.type == other.type and self.name == other.name and self.args == other.args
      return False

  def __ne__(self, other):
    """Overrides the default implementation (unnecessary in Python 3)"""
    return not self.__eq__(other)