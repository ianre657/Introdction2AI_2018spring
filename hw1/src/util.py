from collections import deque
from computeTree import Point, ComputeNode, ComputeTree
from computeTree import solution_path, solNode
present_dict = {
    'addx':'(x+)',
    'addy':'(y+)',
    'subx':'(x-)',
    'suby':'(y-)',
    'pass':'(S)',
}

def print_solution_path( sol_path):
    node = sol_path[0]
    print('initial\t({:>2},{:>2})'.format(node.point.x, node.point.y))
    for n in sol_path[1:]:
        point_str = '({:>2},{:>2})'.format(n.point.x, n.point.y)
        print( '{} {}\t{}'.format(present_dict[n.ppath_type], n.number, point_str),end='')
        if n == sol_path[-1]:
            print(' final')
        else:
            print()


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