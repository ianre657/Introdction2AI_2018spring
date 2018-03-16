from collections import namedtuple
from collections import OrderedDict
from collections import deque
import copy
import sys
import re

Point = namedtuple('Point',['x','y'])
class ComputeNode:
    def __init__(self, parent, point,path_cost, cur_num,remain_num):
        self.parent = parent
        self.ppath_type = None # The type of the path from parent to child
        self.cur_num = cur_num # A signle number
        self.remain_num = remain_num # number remained in computation tree (tuple) 
        self.path_cost = path_cost
        self.point = point
        self.children = {# ComputeNodes
            'addx':None,
            'subx':None,
            'addy':None,
            'suby':None,
            'pass':None,
        }
    def appendchild(self,child_type,exist_node=None,point=None,path_cost=None):
        if exist_node != None:
            self.children[child_type] = exist_node
            exist_node.parent = self
        else:
            self.children[child_type] = ComputeNode(
                parent=self,
                point=point, 
                path_cost=path_cost,
                cur_num = self.remain_num[0],
                remain_num=self.remain_num[1:]
                )

class ComputeTree:
    def __init__(self, numbers, end_point):
        self.root = ComputeNode(
            parent=None,
            point=Point(0,0),
            path_cost=0,
            cur_num=0,
            remain_num=numbers
            )
        self.end_point = end_point 


def bfs_find_solution(game_tree):
    # BFS
    best_cost = 999 # represent infinite
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
        solution = deque()
        cur_node = best_node
        while cur_node != None :
            solution.append(cur_node)
            cur_node = cur_node.parent

        cur_node = solution.pop()
        while cur_node != None:
            print( '{} : {}'.format( cur_node.point, cur_node.ppath_type) )
            if len(solution) == 0:
                break
            cur_node = solution.pop()
    else:
        print("no solution finded")

if __name__ == '__main__':
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
                exit(0)
            



        

