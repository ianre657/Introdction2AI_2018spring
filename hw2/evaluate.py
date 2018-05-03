import collections
import functools
import random

from time import time


from build_table import table_lookup


point_table = table_lookup()


class point_score:
  ''' 儲存單一點的分數，該點上是哪一子
  並額外儲存三個方向上的分數
  '''
  def sum_score(self):
    self.score = sum(self.direction_score.values())
  def __init__(self, dic=None,point_type=None):
    
    self.pt_type = point_type
    self.score = 0
    self.direction_score = {'TL_DR':0,'L_R':0, 'TR_DL':0}
    if dic != None:
      for k,v in dic.items():
        self.direction_score[k] = v
    self.sum_score()
  def __repr__(self):
    return f'<point_score point_type={self.pt_type} total:{self.score};{self.direction_score[self.pt_type]}>'


def evaluation_func(match_dic):
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
  result = 0
  for k,v in match_dic.items():
    #print(f'k:{k}, v:{v}')
    result +=  value[k]* v 
  return result

def get_board_score(lookup_table, board, evaluation_func):
  import random 
  points_to_evaluate = [ random.randint(0,216) for _ in range(4)]
  return random.randint(1,200)

def get_point_score_in_direction( lookup_table,point_index, board, evaluation_func,direction, point_type ):
  '''dir = TL_DR, L_R, TR_DL
  point_type is 1 or 2(我方 or 對方)
  如果在某個方向發現遊戲終止，回傳tuple的第二個值會是True而不是False
  '''
  # 點的值如果不相同不可能基於該值而產生連線
  # ex.在黑子上問目前該點白子的連線數 ->一定為0
  if board[point_index] != point_type:
    return 0

  # live 活(兩邊開放)
  # dead 死(兩邊封閉)
  # half 半活(一邊開放)
  count = {
    'dead2':0,
    'half2':0,
    'live2':0,
    'dead3':0,
    'half3':0,
    'live3':0,
    'dead4':0,
    'half4':0,
    'live4':0,
    '5':0
    }
  #count = { 2:0, 3:0,4:0,5:0}

  def get_count(li, node_type):
    # 利用 n_node_down 回傳None的結果來得知已經到棋盤邊界 
    count = 0
    live = 0 # Live是以數字作為回傳，方便做整合用

    # 數到li[3](第四個)就可以檢查遊戲是否結束
    # 在四個沒有數完的情況下仍要確定延伸出去一格的是哪一種棋子
    for i in range(5):
      #最多數到第五個
      node_id = li[i]
      if node_id == None:#數到棋盤邊界
        return count,live
      if board[node_id] == node_type:
        count +=1
        if count >= 4:
          return 4,1 #一定是五子連線，活跟死不重要
      else: 
        if board[node_id]==0:
          live=1
        return count,live
    
    print(f"不可能發生的情況:li:{li},count:{count},live:{live}")
    exit(0)
  
  if direction == "TL_DR":
    dir1, dir2 = "TL","DR"
  elif direction == "L_R":
    dir1, dir2 = "L","R"
  elif direction == "TR_DL":
    dir1, dir2 = "TR", "DL"
  else:
    print("error, unknown direction")
    exit(1)
  dir1_line = lookup_table.n_node_down(point_index,dir1,4)
  dir2_line = lookup_table.n_node_down(point_index,dir2,4)
  dir1_count, cur_live1 = get_count(dir1_line,point_type)
  dir2_count, cur_live2 = get_count(dir2_line,point_type)
  total_count = dir1_count + dir2_count +1
  total_live = cur_live1+cur_live2
  if total_count >= 5:
    #發現遊戲中止，沒有必要再算下去
    count['5']+=1
    return evaluation_func(count),True
  
  elif total_count <5 and total_count>=2:
    if total_live == 0:
      state="dead"
    elif total_live ==1:
      state='half'
    elif total_live ==2:
      state='live'
    count[f'{state}{total_count}']+=1
  return evaluation_func(count),False

  #舊的計算方法
  #for rng in [5,4,3,2]:
  #  compute_range_list = lookup_table.get_node_subrange(point_index)[rng][direction]
  #  for li in compute_range_list:
  #    good = True
  #    for i in li:
  #      if board[i] !=point_type:
  #        good = False 
  #        break;
  #    if good is True:
  #      count[len(li)] +=1
  #
  #      #發現遊戲中止，沒有必要再算下去
  #      if(rng==5):
  #        return evaluation_func(count),True
  #      
  #return evaluation_func(count),False

def get_point_score( lookup_table,point_index, board, evaluation_func,point_type):
  '''回傳單點之得分數，如果該點造成遊戲終止(五子連線)則回傳tuple的第二個值會為True
  '''
  calc_dir_score = functools.partial( get_point_score_in_direction, lookup_table,point_index,board,evaluation_func)

  outcome_dic = {}
  end = False
  outcome_dic['TL_DR'],end1 = calc_dir_score("TL_DR",point_type)
  outcome_dic['L_R'],end2 = calc_dir_score("L_R",point_type)
  outcome_dic['TR_DL'],end3 = calc_dir_score("TR_DL", point_type)
  end = end or end1 or end2 or end3
  return point_score(outcome_dic, point_type),end


class board_view:
  '''某一瞬間的棋盤，額外儲存每個格子點的分數與盤面的分數
  '''
  def __init__(self,board,point_scores,lookup_table,evaluation_function,recompute_pt_dict=None, recompute_all=False):
    '''
      參數:
        recompute_pt_dict: 要重新計算的節點跟重新計算的方向 { node_idx:{'TL_DR'} }
    '''
    self.board = board[:]
    self.lookup_table = lookup_table
    self.evaluation_function = evaluation_function

    # 紀錄整個盤面上兩方的總成績
    self.board_score = { 1:0, 2:0}

    # init point scores
    if recompute_all == True:
      # 1 是我方
      # 2 是敵方
      # 紀錄整個盤面上分別每個點雙方的成績
      self.point_scores = [ 0 for _ in range(217)]
      for i in range(217):
        if self.board[i] != 0:
          # get point score中有自己做優化
          self.point_scores[i],_ = get_point_score(self.lookup_table,i,self.board,self.evaluation_function,self.board[i])
        else:
          self.point_scores[i] = point_score(point_type=0)
    else:
      self.point_scores = point_scores[:]

    if recompute_all != True and recompute_pt_dict != None:
      for node_id,direction in recompute_pt_dict.items():
        pt = self.point_scores[node_id]
        if self.board[node_id] == 0: # 不太可能的情況，因為不會把為0的格子點列入重算
          pt.direction_score[direction]=0
        else:
          #這裡就算發現會結束也不會回傳,因為造成結束的點不會是這個點，而是self.create_new_board中填入的點
          #另外，因為init沒辦法回傳值所以在這裡進行遊戲終止判斷也不太適合
          new_direction_score,_ = get_point_score_in_direction( self.lookup_table,node_id, self.board, self.evaluation_function, direction,self.board[node_id])
          pt.direction_score[direction] = new_direction_score
        pt.sum_score()
    
    node_1 = [ i for i in range(217) if self.board[i]==1 ]
    node_2 = [ i for i in range(217) if self.board[i]==2 ]
    s1,s2 =0,0
    for i in node_1:
      s1 += self.point_scores[i].score
    for i in node_2:
      s2 += self.point_scores[i].score
    self.board_score[1] = s1
    self.board_score[2] = s2

  def get_board_score(self, point_type):
    return self.board_score[point_type]
  
  def check_borad_end(self):
    '''檢查是否有任何一方獲勝,
    或是和局(雙方皆沒獲勝，而且棋盤沒有空格)
    '''
    check_list = self.lookup_table.get_end_checking_table()
    # 檢查單一條直線中是否有連續五個子
    def check_line(line):
      # Line中為棋盤上存在於一直線中的node id
      count = 0
      last_val=0
      for i in line:
        cur_val = self.board[i]
        if cur_val == last_val and cur_val != 0:
          count += 1
          if count == 5:
            return True
        else:
          count =1
        last_val = cur_val 
      return False

    for li in check_list:
      #if li[0] == 19 and li[1]==20:
        #print("THERE!") 
      if check_line(li) == True:
        return True
    
    #檢查是否有空格可以放棋子
    for i in range(217):
      if self.board[i]!=0:
        return False
    return True

  def create_new_board(self, new_node, new_node_value):
    '''根據目前盤面來建立出新盤面
    更新以目前點畫出直線在距離(4)內的所有點

    回傳值(tuple): -> (新產生的盤面,是否造成遊戲終止)
    '''
    def merged_node_list(node,dir1, dir2,n):
      '''回傳存在且不為空格的點
      '''
      dir1 = self.lookup_table.n_node_down( node, dir1,n)
      dir2 = self.lookup_table.n_node_down( node, dir2,n)
      return [i for i in list(dir1+dir2) if i != None and self.board[i]!= 0]

    n = 4
    tl_dr = merged_node_list(new_node,'TL','DR',n)
    l_r  = merged_node_list(new_node,'L','R',n)
    tr_dl = merged_node_list(new_node,'TR','DL',n)
    
    recompute_nodes = {}
    #{ node_id:要重新計算的方向 }
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
    #必須進行終止判斷
    new_point_scores[new_node],end = get_point_score( self.lookup_table,new_node,new_board, self.evaluation_function,new_node_value)
    
    return board_view(new_board,new_point_scores,self.lookup_table,self.evaluation_function,recompute_pt_dict=recompute_nodes),end



if __name__ == "__main__":
  board_value = [85,102,103,118,119,120,134]
  board = [0 for i in range(217)]
  for i in board_value:
    board[i] = 1
  #pt_score = get_point_score(point_table,119,board,evaluation_func)
  #print(pt_score)
  #exit(0)

  iterate = 10000

  def new_board(bview=None):
    if bview is None:
      bview = board
    return board_view(
    board=bview,
    point_scores=None,
    lookup_table=point_table,
    evaluation_function=evaluation_func,
    recompute_all=True
    )


  start = time()
  b = new_board()

  bi = b
  bn = None
  for _ in range(iterate):
    blank = [ i for i in bi.board  if i != None ]
    if len(blank)!=0:
      next_move = random.randint(0,len(blank)-1)
      bn = bi.create_new_board(next_move,1)
      
      #next_board = bi.board[:]
      #next_board[next_move] = 1
      #bn = new_board(next_board)
    else:
      blank = [ i for i in b.board  if i != None ]
      next_move = random.randint(0,len(blank)-1)
      bn = b.create_new_board(next_move,1)
    bi = bn
    #b2 = b.create_new_board(135,1)
    #b3 = b2.create_new_board(91,1)
      
    
    
  end = time()
  print("second:{:2f} sec".format(end-start))
  print("-----")

  exit(0)

  while True:
    node = int(input("Node id:"))
    direction = input("direction:").upper()
    nlist = point_table.n_node_down(node,direction,4)
    print(nlist)