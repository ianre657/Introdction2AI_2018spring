import copy
from collections import OrderedDict
from collections import deque

from computeTree import Point, ComputeNode, ComputeTree
from util import print_solution

def recursive_find(node, end_point, max_depth):
    '''
        return None if no answer finded
    '''

    if node.path_cost > max_depth:
        return None
    elif node.point == end_point:
        return node
    elif len(node.remain_num)==0:
        return None
    
    # add five children
    child_pcost = node.path_cost+1
    child_num = node.remain_num[0]
    child_re_num = node.remain_num[1:]
    example_node = ComputeNode( 
        parent=node,
        point=Point(0,0),
        path_cost= child_pcost,
        cur_num=child_num,
        remain_num=child_re_num
        )
    # Allocate five childeren
    (cur_x, cur_y) = node.point
    add_x, add_y, sub_x, sub_y, ps = ( copy.copy(example_node) for _ in range(5))
    add_x.point= Point(cur_x+child_num, cur_y)
    add_y.point= Point(cur_x, cur_y+child_num)
    sub_x.point= Point(cur_x-child_num, cur_y)
    sub_y.point= Point(cur_x, cur_y-child_num)
    ps.point= Point(cur_x, cur_y)
    ref_dict = OrderedDict( [(add_x,'addx'),(add_y,'addy'),(sub_x,'subx'),(sub_y,'suby'),(ps,'pass')])
    for ob in ref_dict.keys():
        ob_name = ref_dict[ob]
        ob.ppath_type = ob_name
        node.appendchild(child_type=ob_name,exist_node=ob)
    
    for child in node.children.keys():
        result_node = recursive_find(
                node= node.children[child],
                end_point= end_point,
                max_depth= max_depth
            )
        if result_node != None:
            return result_node

    return None

def ids_find_solution(game_tree):
    ''' Iteractive Deeping Search
    use DFS with limited depth , which would be incremented iteractiveily.
    '''
    
    best_cost = 0
    best_node = None
    
    max_depth = 2
    
    while max_depth <= len(game_tree.root.remain_num):
        result_node = recursive_find(
                        node= game_tree.root,
                        end_point= game_tree.end_point,
                        max_depth= max_depth
                    )
        if result_node != None:
            if best_node == None or result_node.path_cost < best_cost:
                best_node = result_node
                best_cost = result_node.path_cost
            print_solution(best_node)
            return
                
        max_depth += 1 

    