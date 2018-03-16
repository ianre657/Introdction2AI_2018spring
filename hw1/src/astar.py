import copy
from collections import OrderedDict
from collections import deque

from computeTree import Point, ComputeNode, ComputeTree
from util import print_solution

def heuristic():
    pass

def astar_find_solution(game_tree):
    # BFS
    best_cost = 9999 # represent infinite
    best_node = None
    dq = deque()
    dq.append(game_tree.root)
    while dq.count != 0:
        node = dq.popleft() # the leftmost one

        if node.point == game_tree.end_point:
            if node.path_cost < best_cost:
                best_cost = node.path_cost
                best_node = node
            break
        elif len(node.remain_num) == 0 :
            continue

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
        for obj in ref_dict:
            dq.append(obj)
    #end while
    
    if best_node != None:
        print("find best solution!!")
        print_solution(best_node)
    else:
        print("no solution finded")