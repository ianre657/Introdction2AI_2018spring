import copy
from collections import OrderedDict
from collections import deque

from computeTree import Point, ComputeNode, ComputeTree
from util import print_solution

# profiling
from time import time
bfs_prof_start_time = 0
bfs_prof_end_time = 0
bfs_prof_execute_time = 0
bfs_prof_node_explored = 0
bfs_prof_depth_reached = 0
bfs_prof_max_queue_size = 0

def bfs_show_profile():
    print('BFS profiling outcome'.center(40,'-'))
    print(' execute time:   {:.4} sec'.format(bfs_prof_execute_time))
    print(' node explored:  {}'.format(bfs_prof_node_explored))
    print(' max tree depth: {}'.format(bfs_prof_depth_reached))
    print(' max queue size: {}'.format(bfs_prof_max_queue_size))


def bfs_find_solution(game_tree):
    global bfs_prof_max_queue_size
    global bfs_prof_start_time, bfs_prof_end_time,bfs_prof_execute_time
    global bfs_prof_node_explored, bfs_prof_depth_reached
    # BFS
    bfs_prof_start_time = time()
    best_cost = 999 # represent infinite
    best_node = None
    dq = deque()
    dq.append(game_tree.root)
    while len(dq) != 0:
        # profiling
        if len(dq) > bfs_prof_max_queue_size:
            bfs_prof_max_queue_size = len(dq)
        # profilingend

        node = dq.popleft() # the leftmost one
        # profiling
        bfs_prof_node_explored += 1
        if node.path_cost > bfs_prof_depth_reached:
            bfs_prof_depth_reached = node.path_cost
        # profiling end

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
    
    bfs_prof_end_time = time()
    bfs_prof_execute_time = bfs_prof_end_time - bfs_prof_start_time
    if best_node != None:
        print("find best solution!!")
        print_solution(best_node)
    else:
        print("no solution finded")
    bfs_show_profile()