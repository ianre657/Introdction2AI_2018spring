import collections
import functools

from time import time

from build_table import table_lookup


point_table = table_lookup()


class point_score:
  ''' 儲存單一點的分數
  額外儲存三個方向上的分數
  '''
  def sum_score(self):
    self.score = sum(self.direction_score.values())
  def __init__(self, dic=None):
    #print(dic)
    self.direction_score = {'TL_DR':0,'L_R':0, 'TR_DL':0}
    if dic != None:
      for k,v in dic.items():
        self.direction_score[k] = v
    self.sum_score()
  def __repr__(self):
    return f'<point_score total:{self.score};{self.direction_score}>'


def evaluation_func(match_dic):
  value = {
    2:100,
    3:1000,
    4:10000,
    5:1000000
  }
  result = 0
  for k,v in match_dic.items():
    result +=  value[k]* v 
  return result

def get_board_score(lookup_table, board, evaluation_func):
  import random 
  points_to_evaluate = [ random.randint(0,216) for _ in range(4)]
  return random.randint(1,200)

def get_point_score_in_direction( lookup_table,point_index, board, evaluation_func,direction):
  '''dir = TL_DR, L_R, TR_DL
  '''
  count = {2:0, 3:0,4:0,5:0}
  for rng in [2,3,4,5]:
    compute_range_list = lookup_table.get_node_subrange(point_index)[rng][direction]
    for li in compute_range_list:
      good = True
      for i in li:
        if board[i] !=1:
          good = False 
          break;
      if good is True:
        count[len(li)] +=1
  return evaluation_func(count)

def get_point_score( lookup_table,point_index, board, evaluation_func):
  calc_dir_score = functools.partial( get_point_score_in_direction, lookup_table,point_index,board,evaluation_func)
  table = lookup_table
  node = point_index

  outcome_dic = {}
  outcome_dic['TL_DR'] = calc_dir_score("TL_DR")
  outcome_dic['L_R'] = calc_dir_score("L_R")
  outcome_dic['TR_DL'] = calc_dir_score("TR_DL")
  return point_score(outcome_dic)



class board_view:
  '''某一瞬間的棋盤，額外儲存每個格子點的分數與盤面的分數
  '''
  def __init__(self,board,point_scores,lookup_table,evaluation_function,recompute_pt_dict=None, recompute_all=False):
    '''
      參數:
        recompute_pt_dict:要重新計算的節點跟重新計算的方向 { node_idx:{'TL_DR'} }
    '''
    self.board = board[:] 
    self.lookup_table = lookup_table
    self.evaluation_function = evaluation_function
    self.board_score = 0

    # init point scores
    if recompute_all == True:
      self.point_scores = [point_score() for _ in range(217)]
      for i in range(217):
        self.point_scores[i] = get_point_score(self.lookup_table,i,self.board,self.evaluation_function)
    else:
      self.point_scores = point_scores[:]


    if recompute_all != True and recompute_pt_dict != None:
      for node_id,direction in recompute_pt_dict.items():
        new_direction_score = get_point_score_in_direction( self.lookup_table,node_id, self.board, self.evaluation_function, direction)
        pt = self.point_scores[node_id]
        pt.direction_score[direction] = new_direction_score
        pt.sum_score()
    
    self.board_score = sum( [s.score for s in  self.point_scores] )

  def get_board_score(self):
    return self.board_score
  
  def create_new_board(self, new_node, new_node_value):
    '''根據目前盤面來建立出新盤面
    更新以目前點畫出直線在距離(4)內的所有點
    '''
    def merged_node_list(node,dir1, dir2,n):
      dir1 = self.lookup_table.n_node_down( node, dir1,n)
      dir2 = self.lookup_table.n_node_down( node, dir2,n)
      return [i for i in list(dir1+dir2) if i != None]

    n = 4
    tl_dr = merged_node_list(new_node,'TL','DR',n)
    l_r  = merged_node_list(new_node,'L','R',n)
    tr_dl = merged_node_list(new_node,'TR','DL',n)
    
    recompute_nodes = {}
    for node in tl_dr:
      recompute_nodes[node] = "TL_DR"
    for node in l_r:
      recompute_nodes[node] = "L_R"
    for node in tr_dl:
      recompute_nodes[node] = "TR_DL"

    new_board = self.board[:]
    new_point_scores = self.point_scores[:]

    #重新計算落點新的分數
    new_board[new_node] = new_node_value
    new_point_scores[new_node] = get_point_score( self.lookup_table,new_node,new_board, self.evaluation_function)
    
    return board_view(new_board,new_point_scores,self.lookup_table,self.evaluation_function,recompute_pt_dict=recompute_nodes)

board_value = [85,102,103,118,119,120,134]
board = [0 for i in range(217)]
for i in board_value:
  board[i] = 1

if __name__ == "__main__":
  #pt_score = get_point_score(point_table,119,board,evaluation_func)
  #print(pt_score)
  #exit(0)

  iterate = 200000

  def new_board():
    return board_view(
    board=board,
    point_scores=None,
    lookup_table=point_table,
    evaluation_function=evaluation_func,
    recompute_all=True
    )

  #start = time()
  #for _ in range(iterate):
  #  b = new_board()
  #end = time()
  #print("first:{:2f} sec".format(end-start))
  #print("-----")

  start = time()
  b = new_board()
  for _ in range(iterate):
    b2 = b.create_new_board(135,1)
    b3 = b2.create_new_board(101,1)
    b4 = b3.create_new_board(86,1)
  end = time()
  print("second:{:2f} sec".format(end-start))
  print("-----")

  exit(0)

  while True:
    node = int(input("Node id:"))
    direction = input("direction:").upper()
    nlist = point_table.n_node_down(node,direction,5)
    print(nlist)