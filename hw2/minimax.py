
import random
import time
import math

from evaluate import board_view
from build_table import table_lookup

# init lookup table 
table = table_lookup()

max_depth=5

positive_inf = math.inf
negative_inf = -1*math.inf

def eva_function(match_dic):
  value = {
    2:1,
    3:100,
    4:10000,
    5:1000000
  }
  result = 0
  for k,v in match_dic.items():
    result +=  value[k]* v 
  return result

#def get_board_value(board):
#  value=random.randint(-board_value_limit,board_value_limit)
#    return value

def minimax(board,lookup_table, max_depth):
  '''max 為我方的最優化方向,且每次進入max時皆代表為我方執子
     mini 為對手的最優化方向
  '''
  max_depth = max_depth
  bview = board_view(
    board=board,
    point_scores=None,
    lookup_table=lookup_table,
    evaluation_function= eva_function,
    recompute_all=True
  )

  def get_eva_pts(cur_bview):
    return [ i for i in range(217) if cur_bview.board[i]==0 ]

  def _max(cur_bview, depth, alpha, beta):
    '''進入時永遠為我方執子
    '''
    if depth >= max_depth:
      #回傳我方的分數
      return cur_bview.get_board_score[1]

    # max_value  為目前偵測到的最大值
    max_node = None
    max_value = negative_inf
    
    points = get_eva_pts(cur_bview)
    for i in points:
      board_next = cur_bview.create_new_board(i,1)
      val,step = _mini(board_next,depth+1,alpha,beta)
      if val > max_value:
        max_node = step
        max_value = val

      if max_value >= beta:
        return max_value,max_node
      alpha = max(alpha,max_value)

  def _mini(cur_bview,depth, alpha, beta):
    '''進入時永遠為對方執子
    '''
    if depth >= max_depth:
      return cur_bview.get_board_score()

    # min_value 為目前探測到的最小值
    min_node = None
    min_value = positive_inf

    points = get_eva_pts(cur_bview)
    for i in points:
      board_next = cur_bview.create_new_board(i,2)# 對方執子
      val, step = _max(board_next,depth+1,alpha,beta)
      if val < min_value:
        min_value = val
        min_node = step

      if min_value <= alpha:
        return min_value, min_node
      beta = min(beta,min_value)

  #執行程式
  val,step = _max(bview,depth=0,alpha=negative_inf,beta=positive_inf)
  print(f'next step:{step}, val:{val}')
 
def main():
  board = [0 for i in range(217)]
  board[103] = 2 #對方先手
  minimax(board=board,lookup_table=table, max_depth=3)

if __name__ == '__main__':
  main()

