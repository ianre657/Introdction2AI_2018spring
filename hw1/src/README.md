# Program structure

## Main script

`main.py` stand for the "main sricpt", which import the other 3 modules to perform different type of algorithm based on various inputs.

## Searching subroutine

All of the subroutines have build-in profiling functionality.

+ `bfs.py` - Breadth First Search
+ `ids.py` - Iteractive Deeping Search
+ `astar.py` - A* search, (with heuristic function)

## Basic DataStructre & functions

The basic module is the `computeTree.py`, which defined the common data structure for tree search. The tree I construct is specified for this problem.

In `util.py`, I define some common function based on the data structure in `compteTree.py`, such as showing the solution using backtracking from the leaf node.