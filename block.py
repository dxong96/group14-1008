from predicate import Predicate

class Block:
	up = None
	below = None
	value = None
	held = False

	def __init__(self, value, up, below):
		self.value = value
		self.up = up
		self.below = below

	def ontable(self):
		return self.below == None and not self.held

	def on(self, block):
		if self.below == None:
			return False

		return self.below.value == block.value

	def clear(self):
		return self.up == None and not self.held


	def predicates(self):
		ret = []
		if self.ontable():
			ret.append(Predicate('ontable', (self.value, )))

		if self.below != None:
			ret.append(Predicate('on', (self.value, self.below.value)))

		if self.clear():
			ret.append(Predicate('clear', (self.value, )))

		return ret