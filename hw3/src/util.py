import re
import math
from pprint import pprint
from typing import List, Dict, Union

class LearningData:
    '''儲存單一筆學習用的資料
    '''
    def __init__(self,in_arr):
        '''輸入陣列的最後一個元素為label
        '''
        self.data = [float(i) for i in in_arr[0:-1]]
        self.label = in_arr[-1]
    def __repr__(self):
        return f'<LearningData .label:{self.label}, .data:{self.data}>'

def calc_data_list_impurity( data_list: List[LearningData]) -> float:
    def gini_impurity(dist_array: List[int]) -> float:
        '''輸入:不同label下的累積資料數
        '''
        total_elements = sum(dist_array)
        result = 1.0
        for num in dist_array:
            result -= (num/total_elements)**2 
        return result

    def make_histogram(d_list: List[LearningData]) -> List[int]:
        '''根據現有的Learning Data建立分布統計
        '''
        histo = dict()

        for i in d_list:
            if histo.get(i.label) is None:
                histo[i.label] = 1
            else:
                histo[i.label] += 1
        
        #pprint(f'hostogram:{histo}')
        return histo.values()

    hist = make_histogram(data_list)
    return gini_impurity(hist)

def split_list(data_list,attr_idx:int, split_val:float, new_instance=False) -> (List[LearningData],List[LearningData]):
    '''將data串列依據 val進行分割，回傳 under, upper兩個list
    under: val 小於 attr_val 的List.
    upper: val 大於等於 attr_val 的List .
    '''
    low_list = []
    high_list = []
    for d in data_list:
        if d.data[attr_idx] < split_val:
            low_list.append(d)
        else:
            high_list.append(d)
    #pprint(f'high_list:{high_list}')
    #pprint(f'low_list:{low_list}')
    if new_instance is True:
        return low_list[:], high_list[:]
    return low_list, high_list

def get_mids(vals: List[float]) -> List[float]:
    '''回傳陣列中不重複數值的平均點，以升冪排序
    '''
    values = list(set(vals))
    values.sort()

    mid_points = []
    for i in range(len(values)-1):
        mid_points.append( (values[i] + values[i+1])/2 )
    return mid_points

def best_split_node( data_list: List[LearningData], ignore_attrs:List[int]=[]) -> Union[Dict,None]:
    '''回傳最適合作為分割點的index以及分割後的impurity
    '''
    min_impurity = math.inf
    min_atr_idx = None
    min_split_val = None
    find = False

    ignore_idx_set = set(ignore_attrs)
    
    for atr_idx in range(len(data_list[0].data)):
        if atr_idx in ignore_attrs:
            continue
        atr_vals = [d.data[atr_idx] for d in data_list]
        mid_vals = get_mids(atr_vals)
        for val in mid_vals:
            low, high = split_list(data_list,atr_idx,val)
            low_imp = calc_data_list_impurity(low)
            high_imp = calc_data_list_impurity(high)
            split_impurity = low_imp+high_imp
            if split_impurity < min_impurity:
                #print(f'atr:{atr_idx}, val:{val:.3f},  split imp:{split_impurity:.3f}')
                min_impurity = split_impurity
                min_atr_idx = atr_idx
                min_split_val = val
                find=True
    if find is True:
        return {'attr_idx':min_atr_idx, 'impurity':min_impurity, 'split_value':min_split_val }
    else:
        return None

class decision_node:
    def __init__(self, datas:List[LearningData], depth, ignore_attrs=None):
        self.impurity = calc_data_list_impurity(datas)
        self.depth = depth
        self.data_list = datas
        self.ignore_attrs = ignore_attrs

        self.isLeaf = False
        self.split_idx = None
        self.split_val = None
        self.leftNode = None # 小於等於
        self.rightNode = None # 大於 

    def build_tree(self, max_depth):
        if self.depth > max_depth:
            self.isLeaf = True
            return

        result = best_split_node(self.data_list,ignore_attrs=self.ignore_attrs)
        #判斷是否要繼續往下建立節點
        if result!=None and result['impurity'] >= self.impurity:
            self.isLeaf = True
            return
        self.split_idx = result['attr_idx']
        self.split_val = result['split_value']
        left_list, right_list = split_list(
                data_list=self.data_list,
                attr_idx=self.split_idx,
                split_val=self.split_val
        )
        self.leftNode  = decision_node( datas=left_list,  depth=self.depth+1,ignore_attrs=self.ignore_attrs)
        self.rightNode = decision_node( datas=right_list, depth=self.depth+1,ignore_attrs=self.ignore_attrs)
        self.leftNode.build_tree(max_depth=max_depth)
        self.rightNode.build_tree(max_depth=max_depth)

def main(fname):
    data_list = []
    with open(fname, 'r') as input_file:
        for line in input_file.readlines():
            line = line.strip()
            if line!='':
                learn_data = LearningData([i for i in re.split('\s|,', line) if i !=''])
                data_list.append(learn_data)
        #pprint(data_list, compact=True)
        imp = calc_data_list_impurity(data_list)
        #print(f'out {out}: impurity:{imp}')


        origin_impurity =calc_data_list_impurity(data_list)
        print(f'origin_impurity {origin_impurity}')

        result = best_split_node(data_list)
        print(f'result:{result}')

if __name__ =="__main__":
    s1='../sampledata/cross200.txt'
    s2 = '../sampledata/iris.txt'
    s3 = '../sampledata/optical-digits.txt'
    main(s2)
    #im = gini_impurity([30,10])
    #print(f'impurity:{im}')