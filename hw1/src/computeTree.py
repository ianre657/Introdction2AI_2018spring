from collections import namedtuple

Point = namedtuple('Point',['x','y'])

class ComputeNode:
    """ The node for computeTree
    
    Attributes:
        parent (ComputeNode): the parent for is node.
        ppath_type (str): specified which type of calculation the parent have append
            in order to reach this node, must be one of ['addx', 'subx', 'addy', 'suby', 'pass'].
        cur_num (int): the number to be computed to reach this point from parent node.
        remain_num (tuple): numbers to be computed after this node.
        path_cost (int): path cost for reaching this point.
        point (Point): coordinates of the current point, in 2-D space. 
        children (dict): children of this point.a NULL in dict's value means no child for such type of compute.  
    """

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

    def __lt__(self, other):
        return self.point < other.point 
        
    def appendchild(self,child_type,exist_node=None,point=None,path_cost=None):
        ''' append a child to node.
        '''
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
    ''' Search Tree for computation
        Attributes:
            root (ComputeNode): root of the search tree.
            end_point (Point): destinaiton point the search tree want to find.
    '''
    def __init__(self, numbers, end_point):
        self.root = ComputeNode(
            parent=None,
            point=Point(0,0),
            path_cost=0,
            cur_num=0,
            remain_num=numbers
            )
        self.end_point = end_point 