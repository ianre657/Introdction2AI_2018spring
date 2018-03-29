import copy
from collections import deque
from collections import namedtuple
from collections import OrderedDict

Point = namedtuple('Point',['x','y'])
solNode = namedtuple('solNode', ['number','point','ppath_type'])

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
        self.ppath_type = None
        self.cur_num = cur_num
        self.remain_num = remain_num
        self.path_cost = path_cost
        self.point = point
        self.children = OrderedDict([
            # ComputeNodes
            ('addx',None),
            ('subx',None),
            ('addy',None),
            ('suby',None),
            ('pass',None),
        ])

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
    def appendchildren(self):
        '''Add five children to a single node
        '''
        node = self
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

class solution_path:
    '''Contain the information of the solution
    '''

    def __init__(self, ans_leaf):
        ''' generate the solution from leave node
        self.list: contain all of the nodes(include the starting point)
        self.steps: count the steps of the solution ( len(self.list)-1 ) 
        '''
        self.list = []

        solution = deque()
        cur_node = ans_leaf
        while cur_node != None :
            solution.append(cur_node)
            cur_node = cur_node.parent

        # get solution
        while len(solution) != 0:
            cur_node = solution.pop()
            self.list.append(
                solNode(
                    cur_node.cur_num,
                    cur_node.point,
                    cur_node.ppath_type
                )
            )
        self.steps = len(self.list)-1
            

    def __len__(self):
        return len(self.list)

    def __getitem__(self, key):
        return self.list[key]
    def __str__(self):
        rep = []
        for i in self.list:
            rep.append('num={},porint={},ppath={}'.format(i.number,i.point,i.ppath_type))
        return '\n'.join(rep)