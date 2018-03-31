import copy
from collections import OrderedDict
from collections import deque

from math import floor

from heapq import heappush
from heapq import heappop


from computeTree import Point, ComputeNode, ComputeTree
from computeTree import solNode, solution_path

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

def default_heuristic(point, endpoint):
    (px,py) = point
    (ex,ey) = endpoint
    #return 1
    return floor( abs(px-ex)/9)+ floor( abs(py-ey)/9)

def astar_find_solution(game_tree, heuristic=default_heuristic, show_profiling=False ):
    global astar_prof_max_queue_size
    global astar_prof_start_time, astar_prof_end_time,astar_prof_execute_time
    global astar_prof_node_explored, astar_prof_depth_reached

    if show_profiling == True:
        atexit.register(exit_handler)
    astar_prof_start_time = time()

    best_cost = 9999 # represent infinite
    best_node = None

    # use heapq to make this list in heap
    # each item is in type of a 2-tuple, which is (value, node)
    priority_q = []
    srt_pt, end_pt = game_tree.root.point, game_tree.end_point
    if heuristic== default_heuristic:
        pair = ( heuristic(srt_pt, end_pt) + 0, game_tree.root )
    else:
        # imporved version of heuristic funciton need to known the next
        pair = ( heuristic(srt_pt, end_pt, game_tree.root.remain_num), game_tree.root)

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

        node.appendchildren()
        for ch_name in node.children.keys():
            obj = node.children[ch_name]
            srt_pt, end_pt = obj.point, game_tree.end_point
            if heuristic== default_heuristic:
                pair = ( heuristic(srt_pt, end_pt) +node.path_cost, node.children[ch_name] )
            else:
                # imporved version of heuristic funciton need to known the next
                pair = ( heuristic(srt_pt, end_pt, obj.remain_num)+node.path_cost, node.children[ch_name])
                #pair = ( heuristic(obj.point,game_tree.end_point)+node.path_cost, node.children[ch_name])
            heappush( priority_q, pair)
    #end while

    # profiling
    astar_prof_end_time = time()
    astar_prof_execute_time = astar_prof_end_time - astar_prof_start_time
    # profiling end
    
    if show_profiling == True:
        astar_show_profile()

    if best_node != None:
        return solution_path(best_node)
        #print_solution(best_node)
    else:
        return None