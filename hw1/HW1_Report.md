# HW1

    Introdunction to AI @ NCTU, Spring 2018
    0411276 陳奕安
    Environment : OSX 10.13.3, using cpython 3.6.4

## Program structure

### Main script

`main.py` stand for the "main sricpt", which import the other 3 modules to perform different type of algorithm based on various inputs.

### Searching subroutine

All of the subroutines have build-in profiling functionality.

+ `bfs.py` - Breadth First Search
+ `ids.py` - Iteractive Deeping Search
+ `astar.py` - A* search, (with heuristic function)

### Basic DataStructre & functions

Common data structures for tree searching, which is specilly designed for this problem, are defined in `computeTree.py`.

In `util.py`,common functions were defined based on the data structure in `compteTree.py`, such as showing the solution using backtracking from the leaf node.

## Expected outcome

All of the search tree have branching factor B = 5. So the complexity of searching tree might be O(5^n). We expect a O(5^n) time complexity on searching.
However, different from BFS & IDS ,the actual performance of A* search depends on the heuristic funciton h(n) it used, since the goal of A* search is to improve the efficiency of BFS, we might expect a better runtime but almost same space/time complexity of it compare to BFS.

## Outcomes

Given the inputs that vary on the steps of the optimal solution,
it's shown that BFS/IDS have the similar performance. IDS have explored slighlty more nodes than BFS in order to find a solution, but in exchange, the low demand on memory usage, which can't be shown by this chart, is the reason that make IDS a more pratical algorithm while the size of the searching tree grows. On my testing environment, when the optimal solution of the input data is equal to 9 steps, BFS require 834~885 MB of memory during computation. On the other side, only 2MB of memory is used by IDS.

![pic1-1: Node explored under different searching method](./pic/cmp_eng.png)

Changing the vertical axis to a logarithmic scale. It's shows that the 
order of growth between A* and BFS/IDS is different, in a input size that is still capable of measureing (on my computer). We can't get further information without testing a larger input set or use a mathemetic approach.

![pic1-2: pic1-1 in a logarithmic scale](./pic/cmp_log_eng.png)

When it comes to pratical usage. For the sake of efficiency, it's better to apply IDS when the solution doesn't contains no more than 6 steps and use A* instead when it does. The question is that how can we know the steps that a solution would take before actually build a search tree on it? I suggest that __using the heuristic function in A* search to estimate the steps of a optimal solution__.
