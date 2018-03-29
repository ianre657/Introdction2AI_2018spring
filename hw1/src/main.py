#import sys
import re

from computeTree import Point, ComputeNode, ComputeTree
from util import print_solution_path

from bfs import bfs_find_solution
from ids import ids_find_solution
from astar import astar_find_solution

input_file_name = './inputdata/IntroAI_PR1_test.txt' 

def main():
    with open(input_file_name) as inputfile:
        for line in inputfile:
            line = str(line).strip()

            # skip blank line and #(commented) line
            if line.startswith('#') or len(line)==0:
                continue

            words = re.split('[ \n]+', line )
            
            method = words[0]
            x,y = tuple( int (i) for i in words[1:3])
            end_point = Point(x,y)
            numbers = tuple( int(i) for i in words[3:] ) #in

            #print( 'method :"{}", end_point:{}'.format(method,end_point))
            #print( '    numbers : {}'.format(str(numbers)))
    
            gameTree = ComputeTree(numbers=numbers,end_point=end_point)
            if method == 'BFS':
                sol = bfs_find_solution(game_tree= gameTree, show_profiling=True)
                print_solution_path( sol)
                
            elif method == 'IDS':
                sol = ids_find_solution(game_tree= gameTree, show_profiling=True)
                print_solution_path( sol)
                #exit(0)
            elif method == 'A*':
                sol = astar_find_solution(game_tree= gameTree, show_profiling=True)
                print_solution_path( sol)
 
            elif method == 'improved':
                continue
                print('imporved method'.center(40,'='))
                from astar import heuristic
                cur_point = Point(0,0)
                est_step = heuristic(point=cur_point, endpoint=end_point)
                print("estimated step:{}".format(est_step))
                if est_step <= 5:
                    ids_find_solution(game_tree= gameTree)
                else:
                    astar_find_solution(game_tree= gameTree)
                print('imporved method'.center(40,'^'))
            else:
                raise('unknown method')
            print('\n\n')

if __name__ == '__main__':
    main()