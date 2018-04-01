#import sys
import re

from computeTree import Point, ComputeNode, ComputeTree
from util import print_solution_path

from bfs import bfs_find_solution
from ids import ids_find_solution
from astar import astar_find_solution

input_file_name = './inputdata/IntroAI_PR1_test.txt' 


from math import floor
from astar import default_heuristic
from table import table
from table import pt_solution_table
from table import load_table

table_size = 18
table_steps = 4
t = load_table(max_size=table_size, max_steps=table_steps)

def improved_heuristic(point, endpoint, numbers):
    global table

    px,py = point
    ex,ey = endpoint
    vec = (ex-px, ey-py)
    dist = t.find_distance( vec, numbers) 
    if dist != None:
        return dist
    # table have indicate that there are at least `table_steps+1` steps in the solution
    elif abs(vec[0]) < table_size and abs(vec[1]) < table_size:
        return table_steps+1
    else:
        return floor( abs(vec[0])/9)+ floor(abs(vec[1])/9)


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
                print('imporved method'.center(40,'='))
                cur_point = Point(0,0)
                print('numbers:{}'.format(numbers))
                est_step = improved_heuristic(point=cur_point, endpoint=end_point,numbers=numbers)
                print("estimated step:{}".format(est_step))
                sol = astar_find_solution(game_tree=gameTree, show_profiling=True,heuristic=improved_heuristic)
                print_solution_path( sol)
            else:
                raise('unknown method')
            print('\n\n')

if __name__ == '__main__':
    main()