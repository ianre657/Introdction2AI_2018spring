from time import time

from build_table import table_lookup

point_table = table_lookup()

def evaluation_func(dict):
  pass


def get_point_score( lookup_table,point_index, board, evaluation_func):
  table = lookup_table
  node = point_index
  count = {2:0, 3:0,4:0,5:0}
  for rng in [2,3,4,5]:
    tl_dr = table.get_node_subrange(node)[rng]['TL_DR']
    l_r = table.get_node_subrange(node)[rng]['L_R']
    tr_dl = table.get_node_subrange(node)[rng]['TR_DL']
    for directions in [tl_dr,l_r,tr_dl]:
      for li in directions:
        good = True
        for i in li:
          if board[i] !=1:
            good = False 
            break;
        if good is True:
          count[len(li)] +=1
  return count


board_value = [85,102,103,118,119,120,134]
board = [0 for i in range(217)]
for i in board_value:
  board[i] = 1

if __name__ == "__main__":

  iterate = 200000

  start = time()
  for _ in range(iterate):
    count = count = get_point_score(point_table,119,board,None)
    #print(count)
  end = time()
  print("second:{:2f} sec".format(end-start))
  print("-----")

  exit(0)

  while True:
    node = int(input("Node id:"))
    direction = input("direction:").upper()
    nlist = point_table.n_node_down(node,direction,5)
    print(nlist)