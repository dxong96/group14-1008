class StackNode(object):
	name = ""
	args = None

	"""docstring for StackNode"""
	def __init__(self, type, name, args):
		super(StackNode, self).__init__()
		self.type = type
		self.name = name
		self.args = args
		