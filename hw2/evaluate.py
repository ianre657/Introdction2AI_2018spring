from build_table import table_lookup

point_table = table_lookup()

def evaluation_func(dict):

  pass

# get node one the line
def n_node_down( point_index, direction, n):
  ''' return the next n node in the direction
  started from the nearest point
  need to use table_look_up to search nodes
  '''
  result = []
  cur_point = point_index
  #print(f'idx:{point_index}, dir:{direction}')
  for _ in range(n):
    next_node = point_table.get_id_by_relation( cur_point,direction)
    result.append(next_node)
    cur_point = next_node
  return result


def get_point_score( point_index, board, evaluation_func):
  idx = point_index
  
  pass



def node_subrange(node,dir1,dir2,range_num):
  ''' Create subranges to go through with given node_id and the length of the subrange
  '''
  def build_subrange( list1, list2, node,rng):
    ''' construct a list of list which each element have length "rng"
    the template to generate the sublist is 
        list1+[node]+list2 
    '''
    a = [i for i in list1 if i!= None]
    b = [i for i in list2 if i!= None]
    a_list=[]
    b_list=[]
    for i in range(rng):
      if i<=len(a) and i<=len(b):
        #print(f'i={i}')
        if i!=0:
          a_list.append( a[-i:] )
        else:
          a_list.append([])
        if rng-1-i!=0:
          b_list.append( b[:rng-1-i] )
        else:
          b_list.append( [])
    result = []
    for i,j in zip(a_list,b_list):
      result.append( i+[node]+j)
    #for i in result:
    #  print(i)
    return result
  return build_subrange(
    list1=n_node_down(node,dir1,range_num)[::-1],
    list2=n_node_down(node,dir2,range_num),
    node=node,
    rng=range_num
  )


board_value = [85,102,103,118,119,120,134]
board = [0 for i in range(217)]
for i in board_value:
  board[i] = 1

if __name__ == "__main__":
  #102 
  node = 119
  count = {2:0, 3:0,4:0,5:0}
  for rng in [2,3,4,5]:
    tl_dr = node_subrange(node, "TL","DR", rng)
    l_r = node_subrange(node, "L","R", rng)
    tr_dl = node_subrange(node, "DL", "TR", rng)
    for directions in [tl_dr,l_r,tr_dl]:
      for li in directions:
        good = True
        for i in li:
          if board[i] !=1:
            good = False
            break;
        if good is True:
          count[len(li)] +=1
  
  print( count )
  exit(0)

  while True:
    node = int(input("Node id:"))
    direction = input("direction:").upper()
    nlist = n_node_down(node,direction,5)
    print(nlist)