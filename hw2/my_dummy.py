import collections
import functools
import math
import os
import time
from random import randint

# 基本設定
group_id = 3
max_depth=4
max_neighbor_distance=2
max_branching_factor=40

# build.py
class table_lookup:
  '''六角形棋盤的查找表

  Attributes:
    @self.table_hash: 儲存每個棋子編號所對應到的二維位置(row,col)
    @self.rowlist: 儲存每一個row中所具有的棋子
    @self.node_subrange_hash: 儲存每個點在評估分數時要取用的其他點

  functions:
    get_id_by_relation: 回傳任意編號棋子在特定方向上的棋子編號
    n_node_down: 回傳任意編號棋子在任何方向上連續數下去n個位置的棋子編號
    get_node_subrange: 回傳計算分數時三個方向上所要考慮的陣列
  '''
  def build_table_dict(self):
    start_idx = [
      0,9,19,30,42,55,69,84,100,117,133,148,162,175,187,198,
      (208,216)
    ]
    range_list = []
    for idx, val in enumerate(start_idx):
      if type(val) == int:
        next_val = start_idx[idx+1]
        next_val = next_val[0] if type(next_val) == tuple else next_val
        range_list.append([val,next_val-1])
        #print(f'{val}~{next_val-1}: {next_val-val}')
      else:
        range_list.append([val[0],val[1]])
        #print(f'{val[0]}~{val[1]}: {val[1]-val[0]+1}')
    #pprint(range_list)

    table_hash = {}
    for i in range(0,216+1):
      for idx, rang in enumerate(range_list):
        if i>=rang[0] and i<=rang[1]:
          table_hash[i] = {'row':idx, 'index':i-rang[0]}
    return table_hash

  def get_id_by_relation(self,node_id,direction):
    '''回傳任意編號棋子在特定方向上的棋子編號
    如果存取超過邊界時會回傳None

    參數解釋:
      @node_id(int):0~216
      @direction(str):one of  TL, TR, L, R, DL, DR
    回傳範例:
      get_id_by_relation(102,"DR")
        => 119
    '''
    if node_id is None:
      return None
    if direction == "TL":
      if node_id<=116:
        x,y = -1,-1
      else:
        x,y = 0,-1
    elif direction == "TR":
      if node_id <= 116:
        x,y = 0,-1
      else:
        x,y = 1,-1
    elif direction == "L":
      x,y = -1,0
    elif direction == "R":
      x,y = 1,0
    elif direction == "DL":
      if node_id >=100:
        x,y = -1,1
      else:
        x,y = 0,1
    elif direction == "DR":
      if node_id >=100:
        x,y = 0,1
      else:
        x,y = 1,1
    else:
      raise("unknown diection")

    if node_id <0 or node_id>216:
      return None
    cur_node = self.table_hash[node_id]

    dif_x, dif_y = x,y
    cur_x, cur_y = cur_node['index'], cur_node['row']
    #print(f'cx{cur_x}, cy:{cur_y}')
    # target 
    tx,ty = cur_x+dif_x, cur_y+dif_y
    #print(f'len:{len(self.row_list)}')
    #print(f'tx:{tx},ty:{ty}')
    #print(f'tx:{tx}, ty:{ty}')
    #print(f'row9:{self.row_list[8]}')
    if tx<0 or ty<0 or ty>=len(self.row_list):
      return None

    if tx < len(self.row_list[ty]):
      return self.row_list[ty][tx]
    else:
      return None


    # get node one the line
  def __build_n_node_down_cache(self):
    '''將 n_node_down n<=5 情況下的結果都儲存下來
    (在n<=5 的情況下執行速度可以加快約10倍)
    '''
    self.n_node_down_cache = [ {} for i in range(217) ]
    for point_index in range(217):
      for direction in ['TL','TR','L','R','DL','DR']:
        result = []
        cur_point = point_index
        for _ in range(5):
          next_node = self.get_id_by_relation( cur_point,direction)
          result.append(next_node)
          cur_point = next_node
        self.n_node_down_cache[point_index][direction] = result

  def n_node_down( self,point_index, direction, n):
    ''' 回傳任意編號棋子在任何方向上連續數下去n個位置的棋子編號 
      當值超過邊界的節點時回傳id會以None替代掉

    參數解釋:
      direction: 'TL','TR','L','R','DL','DR' 任意字串
      n:  要數連續幾子
    
    回傳範例:
      self.n_node_down(85,'DL',3)
        =>[101,117,None]

    '''
    if n <= 5:
      outcome = self.n_node_down_cache[point_index][direction]
      return outcome[:n]
    else:
      outcome = []
      cur_point = point_index
      #print(f'idx:{point_index}, dir:{direction}')
      for _ in range(n):
        next_node = self.get_id_by_relation( cur_point,direction)
        outcome.append(next_node)
        cur_point = next_node

      return outcome


  def get_end_checking_table(self):
    return self.end_checking_table

  def __build_end_checking_table(self):
    self.end_checking_table = []
    tl_dr = [0,1,2,3,4,5,6,7,8,9,19,30,42,55,69,84,100]
    l_r = [0,9,19,30,42,55,69,84,100,117,133,148,162,175,187,198,208]
    tr_dl = [100,117,133,148,162,175,187,198,208,209,210,211,212,213,214,215,216]

    for i in tl_dr:
      li = [i]+[ i for i in self.n_node_down(i,"DR",16) if i != None]
      self.end_checking_table.append(li)
    for i in l_r:
      li = [i]+[ i for i in self.n_node_down(i,"R",16) if i != None]
      self.end_checking_table.append(li)
    for i in tr_dl:
      li = [i]+[ i for i in self.n_node_down(i,"TR",16) if i != None]
      self.end_checking_table.append(li)
      
  def get_node_subrange(self, node_id):
    '''回傳計算分數時三個方向上所要考慮的陣列
    使用方法:
      get_node_subrange(node_id)[路徑長度][路徑方向]
        路徑長度為2~5的整數
        路徑方向為 "TL_DR", "L_R", "TR_DL" 
    回傳範例:
      get_node_subrange(103)[3]['TL_DR'] 
       => [ [70,86,103],[86,103,120], [103,120,136] ]
    '''
    return self.node_range_table[node_id]

  def __node_subrange(self,node,dir1,dir2,range_num):
    ''' Create subranges to go through with given node_id and the length of the subrange
    '''
    def build_subrange( list1, list2, node,rng):
      ''' construct a list of list which each element have length "rng"
      the template to generate the sublist is 
          list1+[node]+list2 
      '''
      def first_n(li,n):
        if n>len(li):
          return []
        return li[0:n]
      def last_n(li,n):
        if n>len(li) or n==0:
          return []
        return li[-n:]
        
      a = [i for i in list1 if i!= None]
      b = [i for i in list2 if i!= None]
      a_list=[]
      b_list=[]
      for i in range(rng):

        #if i<=len(a) and i<=len(b):
        last_a = last_n(a,i)
        first_b = first_n(b,rng-1-i)
        if len(last_a)+len(first_b) == rng-1:
          a_list.append( last_n(a,i))
          b_list.append( first_n(b,rng-1-i))
        #if i<=len(a) and i<=len(b):
          #if i!=0:      
          #  a_list.append( a[-i:] )
          #else:
          #  a_list.append([])
          #if rng-1-i!=0:
          #  b_list.append( b[:rng-1-i] )
          #else:
          #  b_list.append( [])
      result = []

      #if node == 4:
      #  print(f'node={node}, rng={rng}')
      #  print(f'a={a}, b={b}')
      #  print(f'alist={a_list},blist={b_list}')
      #  print('----')

      for i,j in zip(a_list,b_list):
        #print(f'i:{i}, node:{node} j:{j}')
        result.append( i+[node]+j)

      return result

    return build_subrange(
      list1=self.n_node_down(node,dir1,range_num)[::-1],
      list2=self.n_node_down(node,dir2,range_num),
      node=node,
      rng=range_num
    )

  def __build_node_subrange(self):
    # 0~216
    self.node_range_table = [ {2:{},3:{},4:{},5:{}} for i in range(217)]

    
    for i in range(217):
      for rng in [2,3,4,5]:
        #print("TL-DR:")
        tl_dr = self.__node_subrange(i, "TL","DR", rng)
        #print("L-R:")
        l_r = self.__node_subrange(i, "L","R", rng)
        #print("TR-DL")
        tr_dl = self.__node_subrange(i, "DL", "TR", rng)

        self.node_range_table[i][rng]['TL_DR'] = tl_dr
        self.node_range_table[i][rng]['L_R'] = l_r
        self.node_range_table[i][rng]['TR_DL'] = tr_dl
    
      #if i==4:
      #  print(f'node :{i}')
      #  pprint( self.node_range_table[i]) 
      #  exit(0)


  def __init__(self):
    self.table_hash = dict(self.build_table_dict())
    self.row_list = [[] for _ in range(17)]
    #print(len(row_list))
    for k,v in self.table_hash.items():
      self.row_list[v['row']].append(k)
    for li in self.row_list:
      li.sort()
    self.__build_n_node_down_cache()
    self.__build_node_subrange()
    self.__build_end_checking_table()

table = table_lookup()

# neighbot_table.py

operation = ["TL","TR","L","R","DL","DR"]
'''
gene_six : 用來產生target點的最裡面一圈 return list
gene_n_edge:用來產生target點附近N圈 return dict包set的形式  e.g. {1:{0,10,11,2},2:{......}}
			1代表，離target最近一圈的點
			2代表，離target最近二圈的點
			看你要多少，就用N去改變，但我沒有測極大值，可能會壞掉
gene_n_table:把上面從target = 0 ~ 216 都弄出來給你  return list + dict
			 e.g.
			 table = gene_n_table(2)
			 如果要取target = 10，就table[10] 會和 用gene_n_edge(10)產生出一樣的東西			 
gene_surroundings:把盤面丟進去，會回傳離那一坨子最靠近N圈，return dict包set的形式 同gene_n_edge
'''
def gene_six(table,target):
    ans = []
    for i in range(0,6):
        #print("target",target)
        temp = table.get_id_by_relation(target, operation[i])
        if (temp != None):
            ans.append(temp)
    
    return ans

def gene_n_edge(table,target,depth):
    ans = {}
    explo = set()
    explo.add(target)
    for i in range(1,depth+1):
        temp = set()
        ans[i] = set()
        exploed = set()
        for item in explo:
            new_temp = set(gene_six(table,item))           
            temp.update(new_temp)
            ans[i].update(new_temp)
            exploed.add(item)
        explo.difference_update(exploed)
        exploed.clear()
        explo.update(temp)
        ans[i].discard(target)
        if i > 1:
            ans[i].difference_update(ans[i-1])
    return ans

def gene_n_table(depth,new_table = table):
    ans = []
    for i in range(0,217):
        temp = gene_n_edge(new_table,i,depth)
        ans.append(temp)
    return ans

neighbors_table = gene_n_table(2)

def gene_surroundings(board,table = neighbors_table):
    exist_chess = []
    non_exist_chess = []
    ans = {}
    for index,item in enumerate(board):
        if(item != 0):
            exist_chess.append(index)
        else:
            non_exist_chess.append(index)
    for i in table[0]:
        ans_set = set()
        ans[i] = set()
        for j in exist_chess:
            ans_set.update(table[j][i])
        ans[i].update(ans_set)
        ans[i].difference_update(set(exist_chess))
        if i > 1:
            ans[i].difference_update(ans[i-1])
    return ans


# ====
#evaluate.py
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


# ===
# minimax.py

n_table = gene_n_table(max_neighbor_distance)
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
    'live3':450,
    'dead4':150,
    'half4':700,
    'live4':10000,
    '5':1000000
  }
  result = 0
  if match_dic['live3'] >= 2:
    result += 4500*(match_dic['live3']-1)
  if match_dic['live2'] >=2:
    result += 200
  result = 0
  for k,v in match_dic.items():
    result +=  value[k]* v 
  return result

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

def minimax(board,lookup_table, max_depth):
  '''max 為我方的最優化方向,且每次進入max時皆代表為我方執子
     mini 為對手的最優化方向
  '''
  start_time = time.time()
  max_depth = max_depth
  bview = board_view(
    board=board,
    point_scores=None,
    lookup_table=lookup_table,
    evaluation_function= eva_function,
    recompute_all=True
  )
  def _max(cur_bview, depth,path, alpha, beta,points=None):
    '''進入時永遠為我方執子
    '''
    if depth >= max_depth:
      #回傳我方的分數
      return cur_bview.get_board_score(1),path

    # max_value  為目前偵測到的最大值
    max_value = negative_inf
    max_path = None

    if points == None:
      points = get_eva_pts(cur_bview)
    #if depth ==0:
    #  print(f'pts:{points}')
    for i in points:
      if time.time()- start_time > 5:
        return max_value,max_path
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

  if len([ i for i in range(217) if bview.board[i] != 0 ]) ==0:
    val,path=1,[108,None] 
  else:
    val,path = _max(bview,depth=0,path=[],alpha=negative_inf,beta=positive_inf)
  
  print(f'val:{val}, max path:{path}')
  return path[0]

#====
# dummy.py
# This is a dummy AI example to help you doing program assignment 2.
# We implemented the file I/O part. 
# You may focus on the method, _get_next_move(), 
# which is a method to decide where to place your stone based on the current game state,
# including (1) valid position, (2) your position, (3) your opponent position, 
# (4) board and (5) the winner of first game.
# !! Remember to change the team number in main() !!


class Agent:
    """
    Game agent.
    The procedure:
        1. process_state_info: check game state
        2. is_my_turn: if it is my turn, decide a position to put stone
        3. step: call get_next_move and write the result to move file
    """
    def __init__(self, team_number):
        self.team_number = team_number
        self.stat_file = "state_" + str(team_number) + ".txt"
        self.move_file = "move_" + str(team_number) + ".txt"

        self.cur_move = -1
        self.next_first_move = -1
        self.first_winner = -1
        self.game_stop = False

        self.valid_pos = []
        self.my_pos = []
        self.opponent_pos = []
    
    def process_state_info(self):
        """
        Read state file and get valid position.
        If not my turn to make move, return an empty list.
        """
        self.valid_pos = []
        self.my_pos = []
        self.opponent_pos = []

        # get state file info
        try:
            if not os.path.isfile(self.stat_file):
                return

            sfile = open(self.stat_file, "r")
            if os.stat(self.stat_file).st_size == 0:
                return

            move = int(sfile.readline())
            self.board = map(int, sfile.readline().split())
            self.first_winner = int(sfile.readline())
            sfile.close()
        except:
            return

        if move == -100:
            self.game_stop = True
            return

        # The only condition of move read from state file being less than our record move (cur_move)
        # is that the second game starts.
        # So, if move is less than cur_move and is not next_first_move,
        # just skip it
        if move > self.cur_move or (move == self.next_first_move and self.cur_move != self.next_first_move):
            # If we are making the first move of first game,
            # record the first move of the second game
            if self.cur_move == -1:
                self.next_first_move = 2 if move == 1 else 1
            
            # Record current move
            self.cur_move = move

            self.valid_pos = [i for i in range(217) if self.board[i] == 0]
            self.my_pos = [i for i in range(217) if self.board[i] == 1]
            self.opponent_pos = [i for i in range(217) if self.board[i] == 2]
        else:
            return

    def step(self):
        """
        Get the next move and write it into move file.
        """
        pos = self._get_next_move()
        self._write_move(pos)

    def _get_next_move(self):
        """
        Get a position from valid_pos randomly.
        You should implement your algorithm here.
        These utilities may be helpful:
            self.get_valid_pos()
            self.get_my_pos()
            self.get_opponent_pos()
            self.get_board()

        Check them below for more detail
        """
        return minimax(board=self.get_board(),lookup_table=table, max_depth=max_depth)
        #return self.valid_pos[randint(0, len(self.valid_pos)-1)]

    def _write_move(self, pos):
        """
        Write my move into move file.
        """
        with open(self.move_file, "w") as mfile:
            mfile.write(str(self.cur_move) + " " + str(pos))

    def is_my_turn(self):
        """
        If the valid position is not empty, it is my turn.
        """
        return len(self.valid_pos) != 0

    def is_game_stop(self):
        return self.game_stop

    # some utilities to get the game state
    def get_valid_pos(self):
        """
        Get the valid position where you can put your stone.
        A list of int. e.g. [0, 1, 3, 5, 6, 9, 12,...]
        """
        return self.valid_pos

    def get_my_pos(self):
        """
        Get the position where you have put.
        A list of int. e.g. [2, 4, 7, 8, ...]
        """
        return self.my_pos

    def get_opponent_pos(self):
        """
        Get the position where your opponent have put.
        A list of int. e.g. [10, 11, 13, ...]
        """
        return self.opponent_pos

    def get_board(self):
        """
        Get current board. 0: valid pos, 1: your pos, 2: opponent pos
        A list of int. e.g. [0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 2, 2, 0, 2...]
        """
        return self.board

    def is_first_winner(self):
        """
        Are you the winner of first game?
        Return -1: the first game is still continuing.
                1: yes, you are.
                0: no, you are not.
        """
        return self.first_winner

def main():
    # Change the team number to yours.
    global group_id
    agent = Agent(group_id)

    while True:
        agent.process_state_info()
        if (agent.is_game_stop()):
            break

        if (agent.is_my_turn()):
            agent.step()


if __name__ == "__main__":
    main()