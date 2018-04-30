from pprint import pprint
import time
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

    result = []
    cur_point = point_index
    #print(f'idx:{point_index}, dir:{direction}')
    for _ in range(n):
      next_node = self.get_id_by_relation( cur_point,direction)
      result.append(next_node)
      cur_point = next_node
    return result

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


def main():
  table = table_lookup()
  print( table.n_node_down(4,"DL",5) )
  exit(0)

  #start = time.time()
  while True:
    nid = int(input("Node id:"))
    di = input("direction:").upper()
    i = table.n_node_down(nid,di,4)
    pprint(i)
  #end = time.time()
  #print('{:2f} sec'.format(end-start))

if __name__ == "__main__":
  main()