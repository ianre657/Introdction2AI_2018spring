import copy
from collections import OrderedDict
from collections import deque

from math import floor

from heapq import heappush
from heapq import heappop

from computeTree import Point, ComputeNode, ComputeTree
from util import print_solution

# profiling
import atexit
from time import time
astar_prof_start_time = 0
astar_prof_end_time = 0
astar_prof_execute_time = 0
astar_prof_node_explored = 0
astar_prof_depth_reached = 0
astar_prof_max_queue_size = 0

def astar_show_profile():
    print('astar profiling outcome'.center(40,'-'))
    print(' execute time:   {:.4} sec'.format(astar_prof_execute_time))
    print(' node explored:  {}'.format(astar_prof_node_explored))
    print(' max tree depth: {}'.format(astar_prof_depth_reached))
    print(' max queue size: {}'.format(astar_prof_max_queue_size))
    atexit.unregister(exit_handler)


def exit_handler():
    global astar_prof_end_time, astar_prof_execute_time,astar_prof_start_time
    print("program stopped")
    # profiling
    astar_prof_end_time = time()
    astar_prof_execute_time = astar_prof_end_time - astar_prof_start_time
    # profiling end
    astar_show_profile()

def heuristic(point):
    return 1
    #return floor( abs(point.x)/9)+ floor( abs(point.y)/9)

def astar_find_solution(game_tree):
    global astar_prof_max_queue_size
    global astar_prof_start_time, astar_prof_end_time,astar_prof_execute_time
    global astar_prof_node_explored, astar_prof_depth_reached

    atexit.register(exit_handler)
    astar_prof_start_time = time()

    best_cost = 9999 # represent infinite
    best_node = None

    # use heapq to make this list in heap
    # each item is in type of a 2-tuple, which is (value, node)
    priority_q = []
    pair = ( heuristic(game_tree.root.point) + 0, game_tree.root )
    heappush( priority_q, pair)

    while len(priority_q) != 0:
        # profiling
        if len(priority_q) > astar_prof_max_queue_size:
            astar_prof_max_queue_size = len(priority_q)
        # profilingend

        _, node = heappop(priority_q)
        # profiling
        astar_prof_node_explored += 1
        if node.path_cost > astar_prof_depth_reached:
            astar_prof_depth_reached = node.path_cost
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
            pair = ( heuristic(obj.point)+node.path_cost, obj)
            heappush( priority_q, pair)
    #end while

    # profiling
    astar_prof_end_time = time()
    astar_prof_execute_time = astar_prof_end_time - astar_prof_start_time
    # profiling end
    
    if best_node != None:
        print("find best solution!!")
        print_solution(best_node)
    else:
        print("no solution finded")
    astar_show_profile()