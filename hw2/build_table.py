from pprint import pprint
class table_lookup:
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

  def __init__(self):
    self.table_hash = dict(self.build_table_dict())
    self.row_list = [[] for _ in range(17)]
    #print(len(row_list))
    for k,v in self.table_hash.items():
      self.row_list[v['row']].append(k)
    for li in self.row_list:
      li.sort()
  
  def get_id_by_relation(self,node_id,direction):
    '''
    Arguments:
      @node_id(int):0~216
      @direction(str):one of  TL, TR, L, R, DL, DR
    Return Value:
        another node_id(int), or None if not exists
    '''
    if direction == "TL":
      x,y = -1,-1
    elif direction == "TR":
      x,y = 0,-1
    elif direction == "L":
      x,y = -1,0
    elif direction == "R":
      x,y = 1,0
    elif direction == "DL":
      x,y = 0,1
    elif direction == "DR":
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
    #print(f'tx:{tx}, ty:{ty}')
    if tx<0 or ty<0 or ty>len(self.row_list):
      return None

    if tx < len(self.row_list[ty]):
      return self.row_list[ty][tx]
    else:
      return None
    


def main():
  table = table_lookup()
  i = table.get_id_by_relation(10, "DR")
  pprint(i)
if __name__ == "__main__":
  main()