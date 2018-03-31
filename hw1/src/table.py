from computeTree import Point, ComputeNode, ComputeTree
from bfs import bfs_find_solution
import itertools
import pickle
import sys
import time

from pprint import pprint 
global calc_start_time
import multiprocessing as mp

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
    
      print("Point : {}... finished".format( self.point))
      #for ln, st in enumerate(self.sets, start=1):
      #  print(" point:{}".format(self.point) )
      #  print(" steps:{}".format(ln))
      #  print(" number of solutions :{}".format(len(st)) )
      #  #print(  "solution for {}".format(ln).center(30,'-') )
      #  #print(st)
      #  print("")
    
    global calc_start_time
    cur_time= time.time()
    print("time elasped: {:.2f} sec".format(cur_time-calc_start_time))


class table:
  def __init__(self,max_sz=2, max_len=3, num_thread=4):
    '''
    max_len : maximum step to generate
    max_sz : the gride point to generate answer
    '''
    # keys are Points
    self.points = dict()
    self.max_len = max_len
    #self.update_lock = mp.Lock()
    self.generate_table(max_sz=max_sz, num_thread=num_thread)
    #print(self.points)
    #self.update_lock = None

  def generate_table(self, max_sz, num_thread):
    def split(a, n):
      k, m = divmod(len(a), n)
      return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))
    def log_result(result):
      print("Get result...")
      self.points.update(result)

    rng = range( max_sz+1)
    # only generate grid points in the first quadrant
    grid_points = [(x,y) for x,y in itertools.product( rng, rng ) ]
    point_groups = list(split( grid_points, num_thread))

    ps_list =[]
    pool = mp.Pool( processes= num_thread)
    for pg in point_groups:
      pool.apply_async( self.compute_points, args=(pg,), callback=log_result )
    pool.close()
    pool.join()
      #ps = mp.Process(target=self.compute_points,args=(pg,))
      #ps_list.append(ps)
      #ps.start()
    #for ps in ps_list:
      #ps.join()
    

  def compute_points(self, points):
    self_dict = dict()
    for point in points:
      cur_table = pt_solution_table(end_point=point,max_len=self.max_len)
      self_dict[ point ] = cur_table
    return self_dict

  def find_distance( self, point, numbers):
    x,y = point
    find_pt =  Point( abs(x), abs(y))
    pt_sol_table = self.points.get(find_pt,None)
    if pt_sol_table is None:
      return None 
    for length,sol_set in enumerate( pt_sol_table.sets, start=1 ):
      if tuple(numbers[0:length]) in sol_set:
        return length
    return None  

def load_table( max_size=18, max_steps= 3):
  table_name = './table/table_sz{}_stp{}.pickle'.format(max_size, max_steps)
  with open(table_name,'rb') as handle:
    t = pickle.load(handle)
    return t
  #dis = t.find_distance( (-2,-5),[4,2,1] )
  #print("distance={}".format(dis))
  return

def store_table( max_size =3, max_steps=3, num_thread=8):
  ''' Generate the compute table
  '''
  table_name = './table/table_sz{}_stp{}.pickle'.format(max_size, max_steps)
  t = table(max_sz=max_size,max_len=max_steps,num_thread=num_thread)
  #print(t.points)
  with open(table_name,'wb') as handle:
    pickle.dump(t,handle,protocol=pickle.HIGHEST_PROTOCOL)

def main():
  global calc_start_time
  calc_start_time=time.time()
  if len(sys.argv)>=2 and sys.argv[1] == 'store':
    print("start to compute")
    store_table(max_size=18, max_steps=4, num_thread=8)
    return
  
  store_table(max_size=2, max_steps=3, num_thread=4)
  t = load_table(max_size=2, max_steps=3)
  #print('{}'.format( t.points) )
  #dis = t.find_distance( (2,1),[6,2,1] )
  #print("distance={}".format(dis))

if __name__ == '__main__':
  main()


