import json
from collections import namedtuple
from block import Block

def read_input():
  input_file = open("input.json", "r")
  # convert to object
  input_json = input_file.read()
  # make a temp class X with fields that the dict have
  # then create a new instance of X with values
  parsed = json.loads(input_json, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
  input_file.close()

  # check length of each row is the same
  start_state = read_state(parsed.start)
  end_state = read_state(parsed.end)

  start_keys = set(start_state.keys())
  end_keys = set(end_state.keys())

  if len(start_keys | end_keys) != len(start_keys):
    raise ValueError("the blocks used at start is different from the ones at end")

  return (start_state, end_state)


def read_state(state_obj):
  # the state is a dict
  state = {}
  # get the number of rows it has
  height = len(state_obj)
  # get the size of the first row
  row_length = len(state_obj[0])
  # use set to ensure no repeat
  values = set()

  # check floating block
  if None in state_obj[-1]:
    raise ValueError('No floating blocks allowed')

  # loop each row
  for y in range(height):
    row = state_obj[y]
    # check length of row
    if len(row) != row_length:
      raise ValueError('row have unequal length')

    # loop each column in row
    for x in range(len(row)):
      col = state_obj[y][x]
      # skip if the col is None
      if col == None:
        continue

      # ensure the block is not repeated
      len_before = len(values)
      values.add(col)
      if len(values) == len_before:
        raise ValueError('duplicate block is not allowed')

      # create block
      up = None
      if y > 0:
        # get the block above current block
        up = state_obj[y - 1][x]
        if up != None:
          # use back block if exist
          if up in state:
            up = state[up]
          else:
            state[up] = Block(up, None, None)
            up = state[up]

      below = None
      if y < height - 1:
        # get the blcok below current block
        below = state_obj[y + 1][x]
        if below != None:
          if below in state:
            below = state[below]
          else:
            state[below] = Block(below, None, None)
            below = state[below]

      # instatiate current block
      block = Block(col, up, below)
      state[col] = block

  return state