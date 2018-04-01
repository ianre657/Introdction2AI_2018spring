from random import randint
from pprint import pprint
import sys
import itertools

sys.path.append('..')
from table import find_path

max_sz = 3

def main():
  global max_sz
  if len(sys.argv) < 2:
    length = int(input())
  else:
    length = int(sys.argv[1])
  print('depth :{}'.format(length))

  rng = range( max_sz+1)
    # only generate grid points in the first quadrant
  grid_points = [(x,y) for x,y in itertools.product( rng, rng ) ]

  print('solution with {} steps'.format(length))
  for point in grid_points:
    num_iter = 10**length
    for i in range(num_iter):
      nm_arr = [ int(i) for i in str(i) ]
      nm_arr = [0]*(length - len(nm_arr))+nm_arr
      
      ans = []
      sol = find_path( point,nm_arr)
      if sol and sol.steps==length:
        ans.append(point[0])
        ans.append(point[1])
        for node in sol[1:]:
          ans.append(node.number)
        ans = [ str(i) for i in ans]
        print( ' '.join(ans) )

if __name__ == '__main__':
    main()