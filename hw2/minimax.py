
import random
import time
import math
import multiprocessing as mp
import pprint

from evaluate import board_view
from build_table import table_lookup
from neighbor_table import gene_surroundings, gene_n_table


max_depth=5

# 決定要尋找離戰區最近的空格
max_neighbor_distance=2
max_branching_factor=30

n_table = gene_n_table(max_neighbor_distance)

# init lookup table 
table = table_lookup()



positive_inf = math.inf
negative_inf = -1*math.inf

def eva_function(match_dic):
  value = {
    'dead2':1,
    'half2':2,
    'live2':4,
    'dead3':100,
    'half3':200,
    'live3':800,
    'dead4':150,
    'half4':700,
    'live4':10000,
    '5':1000000
  }
  #value = {
  #  2:1,
  #  3:100,
  #  4:10000,
  #  5:1000000
  #}
  result = 0
  for k,v in match_dic.items():
    result +=  value[k]* v 
  return result

#def get_board_value(board):
#  value=random.randint(-board_value_limit,board_value_limit)
#    return value

def get_eva_pts(cur_bview):
  res = gene_surroundings(cur_bview.board,table=n_table)
  li = []
  for i in range(1,max_neighbor_distance+1):
    li+=list(res[i])
  #li = list(res[1])+list(res[2])+list(res[3])+list(res[4])
  #li = [i for i in range(217) if cur_bview.board[i] ==0]
  #print(len(li) )

  if len(li)>max_branching_factor:
    li = li[0:max_branching_factor]
  
  return li
  #return [ i for i in range(217) if cur_bview.board[i]==0 ]


def _max(cur_bview, depth,path, alpha, beta,points=None):
  '''進入時永遠為我方執子
  '''
  if depth >= max_depth:
    #回傳我方的分數
    return cur_bview.get_board_score(1),path

  # max_value  為目前偵測到的最大值
  max_node = None
  max_value = negative_inf
  max_path = None

  if points == None:
    points = get_eva_pts(cur_bview)
  #if depth ==0:
  #  print(f'pts:{points}')
  for i in points:
    #if depth ==0 and i==23:
    #  print("there")
    board_next,game_end = cur_bview.create_new_board(i,1)
    if game_end is True:
      val,p = board_next.get_board_score(1)-board_next.get_board_score(2), path+[i]
    else:
      val,p = _mini(board_next,depth+1,path+[i],alpha,beta)

    if val > max_value:
      max_node = i
      max_value = val
      max_path = p 
      

    if max_value >= beta:
      return max_value,None
    alpha = max(alpha,max_value)

  return max_value,max_path

def _mini(cur_bview,depth, path,alpha, beta):
  '''進入時永遠為對方執子
  '''
  if depth >= max_depth:
    return cur_bview.get_board_score(1),path

  # min_value 為目前探測到的最小值
  min_node = None
  min_value = positive_inf
  min_path = None

  points = get_eva_pts(cur_bview)
  for i in points:
    board_next,game_end = cur_bview.create_new_board(i,2)# 對方執子
    if game_end is True:
      val,p = board_next.get_board_score(1)-board_next.get_board_score(2), path+[i]
    else:
      val, p = _max(board_next,depth+1,path+[i],alpha,beta)

    if val < min_value:
      min_value = val
      min_node = i
      min_path = p

    if min_value <= alpha:
      return min_value,None 
    beta = min(beta,min_value)
  return min_value,min_path
#執行程式

def minimax(board,lookup_table, max_depth):
  '''max 為我方的最優化方向,且每次進入max時皆代表為我方執子
     mini 為對手的最優化方向
  '''
  max_depth = max_depth
  #print(f'minimax init board:')
  #for idx,v in enumerate(board):
  #  print(f'idx:{idx}, v:{v}')
  bview = board_view(
    board=board,
    point_scores=None,
    lookup_table=lookup_table,
    evaluation_function= eva_function,
    recompute_all=True
  )

  
  def _max_multicore(cur_bview,depth,path,alpha, beta):
    if depth >= max_depth:
      #回傳我方的分數
      return cur_bview.get_board_score(1),path
    
    _max_multicore.max_value = negative_inf
    _max_multicore.max_path = None
    def split(a, n):
      '''將list a分成n等分
      '''
      li = [[] for _ in range(n)]
      for idx,val in enumerate(a):
        li[ idx%n ].append(val)
      return li
      #k, m = divmod(len(a), n)
      #return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))

    def get_result(  val_tuple ):
      (max_value,max_path) = val_tuple
      print("get result!")
      if max_value > _max_multicore.max_value:
        _max_multicore.max_value = max_value
        _max_multicore.max_path = max_path

    def get_failed( f):
      print(f'failed:{f}')

    points = get_eva_pts(cur_bview)
    num_cpu =  mp.cpu_count()
    group_pts = list( split( points, num_cpu))

    print(points)
    print('splited points')
    pprint.pprint(group_pts)

    pool = mp.Pool( processes=num_cpu )
    for pg in group_pts:
      pool.apply_async(
        _max,
        args=(cur_bview,depth,path,alpha,beta,pg),
        callback=get_result,
        error_callback=get_failed
      )
    
    pool.close()
    pool.join()
    return _max_multicore.max_value,_max_multicore.max_path

  if len([ i for i in range(217) if bview.board[i] != 0 ]) ==0:
    val,path=1,[108,None] 
  else:
    val,path = _max(bview,depth=0,path=[],alpha=negative_inf,beta=positive_inf)
    #val,path = _max_multicore(bview,depth=0,path=[],alpha=negative_inf,beta=positive_inf)
  print(f'val:{val}, max path:{path}')
 
def main():
  board = [0 for i in range(217)]
  #board[103] = 2 #對方先手
  
  oppo = [24,35,48,23,62,47]
  me   = [36,37,26,12,77]
  #oppo = []
  #me = []
  for i in me:
    board[i] = 1
  for i in oppo:
    board[i] = 2 
  minimax(board=board,lookup_table=table, max_depth=4)

if __name__ == '__main__':
  main()

