from random import randint
from pprint import pprint
import sys
choose = {
  1:'x+',
  2:'x-',
  3:'y+',
  4:'y-',
  5:'pass'
}

def main():
  if len(sys.argv) < 2:
    depth = int(input())
  else:
    depth = int(sys.argv[1])
  print('depth :{}'.format(depth))

  x,y = (0,0)
  num_list = []
  for _ in range(depth):
    r_int = randint(1,9)
    r_choose_num = randint(1,5)
    r_choose = choose[r_choose_num]
    print('move:{}, int:{}'.format(r_choose, r_int))
    if r_choose == 'x+':
      x+=r_int
    elif r_choose=='x-':
      x-=r_int
    elif r_choose=='y+':
      y+=r_int
    elif r_choose=='y-':
      y-=r_int
    num_list.append( r_int)
  
  print('x,y = {}, {}'.format((x,y), num_list ))
  num_list.insert(0,y)
  num_list.insert(0,x)
  #print( ' '.join(num_list) ) 
  pprint( ' '.join( map( str, num_list)) )
if __name__ == '__main__':
    main()