import re
import math
import random
import multiprocessing as mp
import time
from pprint import pprint
from typing import List, Dict, Union


DUPLICATE_VARIFIED_TIMES =5
NUM_DATA_CHUNK= 51

NUM_DATA_CHUNK_FOR_TRAINING= 25
NUM_ATTR_BAGGING_TIMES= 5

class LearningData:
    '''儲存單一筆學習用的資料
    '''
    def __init__(self,in_arr, idx=None):
        '''輸入陣列的最後一個元素為label
        '''
        if idx!=None:
            self.idx = idx 
        self.data = [float(i) for i in in_arr[0:-1]]
        self.label = in_arr[-1]
    def __repr__(self):
        return f'<LearningData .label:{self.label}, .data:{self.data}>'

def chunkify(lst:List,n) -> List[List]:
    return [ lst[i::n] for i in range(n) ]

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
    #print(f'ignore:{ignore_attrs}')
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
    def __init__(self, datas:List[LearningData], ignore_attrs:List[int]=[], init_depth=0):
        self.impurity = calc_data_list_impurity(datas)
        self.depth = init_depth
        self.data_list = datas[:]
        self.ignore_attrs = ignore_attrs

        self.isLeaf = False
        self.split_idx = None
        self.split_val = None
        self.leftNode = None # 小於等於
        self.rightNode = None # 大於

    def build_tree(self, max_depth):
        if self.depth > max_depth:
            self.isLeaf = True
            return

        result = best_split_node(self.data_list,ignore_attrs=self.ignore_attrs)
        #print(f'tree node imp:{self.impurity}, split result:{result}')
        #判斷是否要繼續往下建立節點
        if result==None or result['impurity'] >= self.impurity:
            self.isLeaf = True
            return
        self.split_idx = result['attr_idx']
        self.split_val = result['split_value']
        left_list, right_list = split_list(
                data_list=self.data_list,
                attr_idx=self.split_idx,
                split_val=self.split_val,
                new_instance=True
        )
        self.leftNode  = decision_node( datas=left_list,  ignore_attrs=self.ignore_attrs, init_depth=self.depth+1)
        self.rightNode = decision_node( datas=right_list, ignore_attrs=self.ignore_attrs, init_depth=self.depth+1)
        self.leftNode.build_tree(max_depth=max_depth)
        self.rightNode.build_tree(max_depth=max_depth)

    def show_tree(self, indent=""):
        if self.isLeaf is True:
            print(indent+"leaf node")
            for idx,d in enumerate(self.data_list):
                print(f'{indent}idx:{idx+1}, label:{d.label}. origin_idx={d.idx}')
            print()
        else:
            self.leftNode.show_tree(indent=indent+'L-> ')
            self.rightNode.show_tree(indent=indent+'R-> ')
      
    def classify(self, input_data:LearningData) -> Union[str, float]:
        cur_node = self
        if cur_node.isLeaf is True:
            return None

        # 直接到最最終端點
        while cur_node.isLeaf is not True:
            cur_idx = cur_node.split_idx
            cur_val = cur_node.split_val
            d = input_data
            if d.data[cur_idx] <= cur_val:
                cur_node = cur_node.leftNode
            else:
                cur_node = cur_node.rightNode
        
        histo = dict()
        for d in cur_node.data_list:
            if histo.get(d.label) is None:
                histo[d.label] = 1
            else:
                histo[d.label] += 1
        
        #print(f'hostogram:{histo}')

        # 使用多數決預測資料種類
        max_label = None
        max_count = -1
        for k,v in histo.items():
            if v > max_count:
                max_label = k
                max_count = v
        #print(f'predict : {max_label}')
      
        # 顯示底層資料夾
        #for idx,d in enumerate(cur_node.data_list):
        #    print(f'leaf idx:{idx}, label:{d.label}, data_idx:{d.idx}')
        return max_label

class decision_trees:
    '''包含眾多 decision root nodes
        可以進行投票來回傳結果
    '''
    def __init__(self, tree_list ):
        self.num = len(tree_list)
        self.trees = tree_list

    def classify(self, input_data:LearningData,show=False) -> Union[str,float]:
        histo = dict()
        for t in self.trees:
            label = t.classify(input_data )
            if histo.get(label) is None:
                histo[label] = 1
            else:
                histo[label] += 1

        # 使用多數決預測資料種類
        max_label = None
        max_count = -1
        for k,v in histo.items():
            if v > max_count and k != None:
                max_label = k
                max_count = v
        if show is True:
            print(histo)
        return max_label

def train_by_data(data_chunks: List[List[LearningData]],max_tree_depth=20 ) -> decision_trees:
    '''回傳訓練好的樹群
    '''
    num_attributes = len(data_chunks[0][0].data)

    def get_ignore_attribute_list():
        num_items = NUM_ATTR_BAGGING_TIMES
        num_attr = num_attributes
        num_ignore = int(num_attr**0.5)
       
        lg_list = [ random.sample( [i for i in range(num_attr)] ,num_ignore) for _ in range(num_items) ]

        return lg_list
 
    traning_data = data_chunks

    # tree bagging
    Primary_dtree = None #不同訓練資料產生出的決策樹
    diff_data_dtrees = []
    ig_attrs = get_ignore_attribute_list()
    
    
    # mp
    #num_cpu =  mp.cpu_count()
    #def collect_mp_result( val_tuple):
    #    pass

    #def get_mp_failed(msg):
    #    print(f'failed :{msg}')


    for idx,data in enumerate(traning_data):
        print(f'training tree: {idx}/{len(traning_data)}')
        #attribute bagging 
        diff_attr_dnodes = [] # 忽略不同參數而產生出的決策樹List
        for idx2,ig_list in enumerate(ig_attrs):
            print(f' bagging :{idx2}/{len(ig_attrs)}')
            ignore_attr_idx = ig_list
            dnode = decision_node(data,ignore_attrs=ignore_attr_idx)
            dnode.build_tree(max_tree_depth)
            diff_attr_dnodes.append(dnode)

        sub_dtree = decision_trees(diff_attr_dnodes)
        diff_data_dtrees.append( sub_dtree )

    Primary_dtree = decision_trees(diff_data_dtrees)

    return Primary_dtree

def main(fname):
    
    data_list = []
    with open(fname, 'r') as input_file:
        i = 0
        for line in input_file.readlines():
            line = line.strip()
            if line!='':
                learn_data = LearningData([i for i in re.split('\s|,', line) if i !=''],idx=i)
                data_list.append(learn_data)
                i += 1

        random.shuffle(data_list)

        origin_impurity =calc_data_list_impurity(data_list)
        print(f'origin_impurity {origin_impurity}')


        num_chunk = NUM_DATA_CHUNK
        num_training_chunk = NUM_DATA_CHUNK_FOR_TRAINING

        data_chunks = chunkify(data_list, num_chunk)
        validation_data = data_chunks[0]
        
        #training_data = data_chunks[1:num_training_chunk+1]


        validate_outcomes = []
        for _ in range(DUPLICATE_VARIFIED_TIMES):
            dchunk = data_chunks[1:]
            random.Random(time.time()).shuffle(dchunk)
            training_data = dchunk[:num_training_chunk]

            primary_tree = train_by_data(training_data)
            good = 0
            bad = 0 
            for vdata in validation_data:
                result = primary_tree.classify(vdata)
                if result == vdata.label:
                    good +=1
                else:
                    bad +=1
            vrate = good/(good+bad)*100
            vrate = round(vrate,2)
            print(f'validation :{vrate}%')
            validate_outcomes.append(vrate)
        t = NUM_DATA_CHUNK_FOR_TRAINING
        b = NUM_ATTR_BAGGING_TIMES
        print( f't:{t}, b:{b}')
        print( f'vrates:{validate_outcomes}')
        oc = validate_outcomes
        oc = round(sum(oc)/len(oc),2)
        print( f'avg vrate:{ oc }' )

        #print(f" Primary  tree result: {result}")


if __name__ =="__main__":
    s1='../sampledata/cross200.txt'
    s2 = '../sampledata/iris.txt'
    s3 = '../sampledata/optical-digits.txt'
    main(s3)
    #im = gini_impurity([30,10])
    #print(f'impurity:{im}')