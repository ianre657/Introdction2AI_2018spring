from collections import deque
from computeTree import Point, ComputeNode, ComputeTree

def print_solution( ans_leaf ):
    '''print the answer from the leave node
       example format:
        initial ( 0, 0)
        (x+) 2  ( 2, 0)
        (y+) 7  ( 2, 7)
        (y-) 6  ( 2, 1)
        (x-) 3  (-1, 1)
        (y-) 5  (-1,-4) final
    '''
    if ans_leaf == None:
        return None

    present_dict = {
        'addx':'(x+)',
        'addy':'(y+)',
        'subx':'(x-)',
        'suby':'(y-)',
        'pass':'(S)',
    }
    solution = deque()
    cur_node = ans_leaf
    while cur_node != None :
        solution.append(cur_node)
        cur_node = cur_node.parent

    cur_node = solution.pop()
    while cur_node != None:
        x,y = cur_node.point
        point_str = '({:>2},{:>2})'.format(x,y)
        # root node
        if cur_node.ppath_type == None:
            print( 'initial\t{}'.format(point_str),end='')
        else:
            print( '{} {}\t{}'.format(present_dict[ cur_node.ppath_type], cur_node.cur_num, point_str),end='')    
            #print( '{}, num:{} : {}'.format( cur_node.point, cur_node.cur_num ,cur_node.ppath_type) )
        if len(solution) == 0:
            print(' final')
            break
        print()
        cur_node = solution.pop()