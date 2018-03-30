from computeTree import Point, ComputeNode, ComputeTree
from bfs import bfs_find_solution

def find_path( end_point, numbers):
  gameTree = ComputeTree( numbers= numbers, end_point=end_point)
  sol = bfs_find_solution(game_tree=gameTree)
  if sol:
    return sol
  return None

class pt_solution_table:
  from collections import OrderedDict
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
    
    for ln, st in enumerate(self.sets, start=1):
      print(" point:{}".format(self.point) )
      print(" number of solutions :{}".format(len(st)) )
      print(  "solution for {}".format(ln).center(30,'-') )
      print(st)
      print("")

class table:
  def __init__(self, max_sz=2, max_len=3):
    import itertools
    self.points = dict()
    rng = range( max_sz*-1 ,max_sz,1)
    for x,y in itertools.product( rng, rng ):
      pt = (x,y)
      self.points[ pt ] = pt_solution_table(end_point=pt )
    #for k in self.points.keys():
    # print(k)
  def find_distance( self, point, numbers):
    pass

def main():
  t = table()
  return 
  x,y = -2,3
  end_pt = Point(x,y)
  pt_solution_table(end_pt,max_len=4)
  return

  set3 = set()
  max_len =3 
  for i in range(1000):
    num_array = [ int(i) for i in str(i) ]
    num_array = [0]*(max_len - len(num_array)) +num_array
    #print(num_array)
     
    sol = find_path(end_pt, num_array)
    if sol:
      set3.update( (tuple(num_array),) )
      #print( str(num_array) + ' steps:{}'.format(sol.steps) )
      #print(set3)
      #print(sol)
  
  from pprint import pprint
  print(set3)
  if (2,6,3) in set3:
    print("Good!")
  pass

if __name__ == '__main__':
  main()
