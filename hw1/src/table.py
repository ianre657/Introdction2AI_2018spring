from computeTree import Point, ComputeNode, ComputeTree
from bfs import bfs_find_solution
import itertools
import pickle
import sys

def find_path( end_point, numbers):
  gameTree = ComputeTree( numbers= numbers, end_point=end_point)
  sol = bfs_find_solution(game_tree=gameTree)
  if sol:
    return sol
  return None

class pt_solution_table:
  ''' Store all the possible solution for given point,
  Which "sets" contains the solution we need for given step
  Attribute:
    point (Point)
    sets  (List of sets)
  '''
  def __init__ (self,end_point,max_len=3):
    self.point = end_point
    self.sets = [ set() for i in range(max_len)]

    for length, st in enumerate(self.sets, start=1):
      num_iter = 10**length
      for i in range(num_iter):
        nm_arr = [ int(i) for i in str(i) ]
        nm_arr = [0]*(length - len(nm_arr))+nm_arr
        
        sol = find_path(self.point,nm_arr)
        if sol and sol.steps==length:
          st.update( (tuple(nm_arr),) )
    
    #for ln, st in enumerate(self.sets, start=1):
    #  print(" point:{}".format(self.point) )
    #  print(" number of solutions :{}".format(len(st)) )
    #  print(  "solution for {}".format(ln).center(30,'-') )
    #  print(st)
    #  print("")

class table:
  def __init__(self, max_sz=2, max_len=3):
    '''
    max_len : maximum step to generate
    max_sz : the gride point to generate answer
    '''
    # keys are Points
    self.points = dict()
    rng = range( max_sz*-1 ,max_sz,1)
    for x,y in itertools.product( rng, rng ):
      pt = (x,y)
      self.points[ pt ] = pt_solution_table(end_point=pt ,max_len=max_len)
    #for k in self.points.keys():
    # print(k)
  def find_distance( self, point, numbers):
    pt_sol_table = self.points.get(point,None)
    if pt_sol_table is None:
      return None 
    for length,sol_set in enumerate( pt_sol_table.sets, start=1 ):
      if tuple(numbers[0:length]) in sol_set:
        return length
    return None  

def load_f():
  store_file = './table/data.pickle'
  t = None
  with open(store_file,'rb') as handle:
    t = pickle.load(handle)
  dis = t.find_distance( (5,2),[4,2,1] )
  print("distance={}".format(dis))
  return

def store_f():
  t = table( max_sz=8,max_len=3)
  dis = t.find_distance( (4,2),[4,2,1] )
  #dis = t.find_distance( (1,1),[1,8,9] )
  print("distance={}".format(dis))
  with open('./table/data.pickle','wb') as handle:
    pickle.dump(t,handle,protocol=pickle.HIGHEST_PROTOCOL)
  return

def main():
  if sys.argv[1] == 'load':
    load_f()
  elif sys.argv[1] == 'store':
    print("start to compute")
    store_f()
  else:
    print("no method specified")



if __name__ == '__main__':
  main()
