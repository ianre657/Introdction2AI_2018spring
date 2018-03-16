#import sys
import re

from computeTree import Point, ComputeNode, ComputeTree

from bfs import bfs_find_solution
from ids import ids_find_solution
from astar import astar_find_solution

def main():
    with open('IntroAI_PR1_test.txt') as inputfile:
        for line in inputfile:
            line = str(line).strip()
            words = re.split('[ \n]+', line )
            
            method = words[0]
            x,y = tuple( int (i) for i in words[1:3])
            end_point = Point(x,y)
            numbers = tuple( int(i) for i in words[3:] ) #in

            print( 'method :"{}", end_point:{}'.format(method,end_point))
            print( '    numbers : {}'.format(str(numbers)))
    
            gameTree = ComputeTree(numbers=numbers,end_point=end_point)
            if method == 'BFS':
                bfs_find_solution(game_tree= gameTree)
            elif method == 'IDS':
                ids_find_solution(game_tree= gameTree)
            elif method == 'A*':
                astar_find_solution(game_tree= gameTree)
            else:
                raise('unknown method')

if __name__ == '__main__':
    main()