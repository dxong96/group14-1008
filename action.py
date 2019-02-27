from stack_node import StackNode
import predicate

class Action(StackNode):
	def __init__(self, name, args):
		StackNode.__init__(self, "action", name, args)

	def perform(self, current):
		# maximum 2 args
		a = None
		b = None
		arg_len = len(self.args)

		if arg_len > 0:
			a = current[self.args[0]]

		if arg_len > 1:
			b = current[self.args[1]]

		if self.name == "unstack":
			# pick up clear block A from block B.
			a.below = None
			b.up = None
			a.held = True

			return a.value
		elif self.name == "stack":
			# place block A using the arm onto clear block B.
			a.below = b
			b.up = a
			a.held = False
		elif self.name == "pickup":
			# lift clear block with the empty arm
			a.held = True

			return a.value
		elif self.name == "putdown":
			# place the held block A onto a free space on the table.
			a.held = False

		return None

	def preconditions(self, current):
		# maximum 2 args
		a = None
		b = None
		arg_len = len(self.args)

		if arg_len > 0:
			a = current[self.args[0]].value

		if arg_len > 1:
			b = current[self.args[1]].value

		ret = []
		if self.name == "unstack":
			ret.append(predicate.Predicate('armempty', ()))
			ret.append(predicate.Predicate('on', (a, b)))
			ret.append(predicate.Predicate('clear', (a,)))
		elif self.name == "stack":
			ret.append(predicate.Predicate('clear', (b,)))
			ret.append(predicate.Predicate('holding', (a,)))
		elif self.name == "pickup":
			ret.append(predicate.Predicate('armempty', ()))
			ret.append(predicate.Predicate('ontable', (a,)))
			ret.append(predicate.Predicate('clear', (a,)))
		elif self.name == "putdown":
			ret.append(predicate.Predicate('holding', (a,)))

		ret.insert(0, ret[:])
		return ret

	def __repr__(self):
		params = ', '.join(map(str, self.args))
		return '%s(%s)' % (self.name, params)