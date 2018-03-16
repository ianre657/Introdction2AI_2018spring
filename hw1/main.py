from collections import namedtuple
from collections import deque
import sys
import re

Point = namedtuple('Point',['x','y'])
class ComputeNode:
    def __init__(self, parent, point,path_cost, remain_numbers):
        self.parent = parent
        self.remain_numbers = remain_numbers # number to compute (tuple) 
        self.path_cost = path_cost
        self.point = point
        self.children = {# ComputeNodes
            'addx':None,
            'subx':None,
            'addy':None,
            'suby':None,
            'pass':None,
        }
    def appendchild(self,point,path_cost,child_type):
        self.children[child_type] = ComputeNode(
            parent=self,
            point=point, 
            path_cost=path_cost,
            remain_numbers=self.remain_numbers[1:]
            )

class ComputeTree:
    def __init__(self, remain_numbers):
        self.root = ComputeNode(parent=None,point=Point(0,0), path_cost=0, remain_numbers=remain_numbers)


def bfs_find_solution():
    # BFS
    dq = deque()
    dq.append(gameTree.root)
    while dq.count != 0:
        node = dq.popleft() # the leftmost one

if __name__ == '__main__':
    with open('IntroAI_PR1_test.txt') as inputfile:
        for line in inputfile:
            line = str(line).strip()
            words = re.split('[ \n]+', line )
            
            method = words[0]
            x,y = words[1:3]
            endPoint = Point(x,y )
            numbers = tuple(words[3:]) #in

            print( 'method :"{}", endPoint:{}'.format(method,endPoint))
            print( '    numbers : {}'.format(str(numbers)))
    
    gameTree = ComputeTree(numbers)
    


        

