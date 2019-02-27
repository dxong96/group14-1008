
# simple-block-world-1008
Requirements 
python >= 2.7

## How to run?

    python main.py

## How to change start and goal state?
Edit input.json

## Blocks World Planning Examples

What is the Blocks World? -- The world consists of:
- A flat surface such as a tabletop 
- An adequate set of identical blocks which are identified by letters. - The blocks can be stacked one on one to form towers of apparently unlimited height. 
- The stacking is achieved using a robot arm which has fundamental operations and states which can be assessed using logic and combined using logical operations. 
- The robot can hold one block at a time and only one block can be moved at a time.

We shall use the four actions:  
**UNSTACK(A,B)** -- pick up clear block A from block B;  
**STACK(A,B)** -- place block A using the arm onto clear block B;  
**PICKUP(A)** -- lift clear block A with the empty arm;  
**PUTDOWN(A)** -- place the held block A onto a free space on the table.  

and the five predicates:  
**ON(A,B)** -- block A is on block B. ONTABLE(A) -- block A is on the table.  
**CLEAR(A)** -- block A has nothing on it.  
**HOLDING(A)** -- the arm holds block A. ARMEMPTY -- the arm holds nothing.  
  
Using logic but not logical notation we can say that If the arm is holding a block it is not empty If block A is on the table it is not on any other block If block A is on block B,block B is not clear.

*Why Use the Blocks world as an example?*
The blocks world is chosen because:
it is sufficiently simple and well behaved. easily understood yet still provides a good sample environment to study planning: problems can be broken into nearly distinct subproblems we can show how partial solutions need to be combined to form a realistic complete solution.
