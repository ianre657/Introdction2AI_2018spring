import re
import math
import random
import json
import itertools
import atexit
import multiprocessing as mp
import time
from pprint import pprint
from typing import List, Dict, Union


# 重新train資料的次數，多次一點比較可以代表參數的效果如何
DUPLICATE_TRAINING_TIMES = 10

# 越多次驗證測資的測定結果越可靠
VALIDATE_TIMES =400


VALIDATE_DATA_SIZE = 80
TRAINING_DATA_SIZE = 40


# 主要要調的參數
NUM_ATTR_BAGGING_TIMES = 10
FOREST_SIZE = 150


#DUPLICATE_TRAINING_TIMES =5
#NUM_ATTR_BAGGING_TIMES = 3
#FOREST_SIZE = 25

start_t= time.time()
para_results = []

def log_data(filename =None):
    if filename is None:
        filename = 'result.json'
    with open(filename,'w') as fp:
        para_results.sort( key=lambda x:x['avg_rate'],reverse=True)
        #json.dump(para_results,fp,indent=4)
        print('[',file=fp)
        for d in para_results:
            json.dump(d,fp)
            if d != para_results[-1]:
                print(',',file=fp)
            else:
                print('',file=fp)
        print(']',file=fp)

    end_t=time.time()
    print('----------current result---------------')
    pprint(para_results)
    print(f'running time: {end_t -start_t}')

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

def dot_product(lst1, lst2):
    '''回傳兩個list的cartesian product
    '''
    result =[] 
    for i in lst1:
        for j in lst2:
            tmp = []
            if type(i) != list:
                i = [i]
            if type(j) != list:
                j = [j]
            tmp.extend(i)
            tmp.extend(j)
            result.append(tmp)
    return result

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

def calculate_sub_dtree(data,ig_attrs,max_tree_depth):
    diff_attr_dnodes = [] # 忽略不同參數而產生出的決策樹List
    #print(f'datasize:{len(data)}')
    for idx,ig_list in enumerate(ig_attrs):
        #print(f' bagging :{idx}/{len(ig_attrs)}')
        ignore_attr_idx = ig_list
        dnode = decision_node(data,ignore_attrs=ignore_attr_idx)
        dnode.build_tree(max_tree_depth)
        diff_attr_dnodes.append(dnode)

    sub_dtree = decision_trees(diff_attr_dnodes)
    return sub_dtree

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
    done= 0
    def collect_mp_result( sub_dtree):
        nonlocal done
        diff_data_dtrees.append(sub_dtree)
        done += 1
        #print(f'finished :{done} trees')

    def get_mp_failed(msg):
        print(f'failed :{msg}')
    
    pool = mp.Pool(processes=mp.cpu_count())
    for idx,data in enumerate(traning_data):
        pool.apply_async(
            calculate_sub_dtree,
            args=(data,ig_attrs,max_tree_depth),
            callback=collect_mp_result,
            error_callback=get_mp_failed
        )
    pool.close()
    pool.join()

    Primary_dtree = decision_trees(diff_data_dtrees)

    return Primary_dtree

def validate_single_time(examine_dataset,trained_tree):
    good,bad = 0,0
    for vdata in examine_dataset:
        result = trained_tree.classify(vdata)
        if result == vdata.label:
            good +=1
        else:
            bad +=1
    vrate = good/(good+bad)*100
    vrate = round(vrate,2)
    return vrate

def validate(data, trained_tree):
    random.seed()
    vd_outcome = []

    args_list = []
    for _ in range(VALIDATE_TIMES):
        vds = random.sample(data,VALIDATE_DATA_SIZE//2)
        args_list.append((vds,trained_tree))

    with mp.Pool(processes=mp.cpu_count() ) as pool:
        vd_outcome = pool.starmap(validate_single_time,args_list)

    #print(f'vd:{vd_outcome}')
    avg_rate = round(sum(vd_outcome)/len(vd_outcome),2)
    return avg_rate

def main(in_fname, grid=None, ):
    data_list = []
    with open(in_fname, 'r') as input_file:
        i = 0
        for line in input_file.readlines():
            line = line.strip()
            if line!='':
                learn_data = LearningData([i for i in re.split('\s|,', line) if i !=''],idx=i)
                data_list.append(learn_data)
                i += 1
    random.shuffle(data_list)

    #origin_impurity =calc_data_list_impurity(data_list)
    #print(f'origin_impurity {origin_impurity}')
    
    global para_results
    global NUM_ATTR_BAGGING_TIMES,FOREST_SIZE
    global VALIDATE_DATA_SIZE,TRAINING_DATA_SIZE


    # try a range
    bagsize = range(1,5,2)
    fsize = range(1,201,10)
    vd_size = range(20,21,5)
    td_size = range(5,135,10)
    g1 = dot_product(bagsize,fsize) 
    g2 = dot_product(g1,vd_size)
    g3 = dot_product(g2,td_size)

    grid = g3
    #grid = dot_product(bagsize,fsize)
    
    # try for single config
    #grid = [[11,125]]

    # single config imported for outside
    #grid = [[NUM_ATTR_BAGGING_TIMES,FOREST_SIZE,VALIDATE_DATA_SIZE,TRAINING_DATA_SIZE]]

    for NUM_ATTR_BAGGING_TIMES,FOREST_SIZE,VALIDATE_DATA_SIZE,TRAINING_DATA_SIZE in grid:
        data_size = VALIDATE_DATA_SIZE
        num_trees = FOREST_SIZE
        
        validation_data = data_list[0:data_size]
        training_data_pool = data_list[data_size:]
            
        validate_outcomes = []
        for _ in range(DUPLICATE_TRAINING_TIMES):          
            training_data = [ random.sample(training_data_pool,TRAINING_DATA_SIZE) for _ in range(num_trees)]
            primary_tree = train_by_data(training_data)
            accuracy = validate( validation_data,primary_tree)
            #print(f'rate:{accuracy}%')
            validate_outcomes.append(accuracy)

        bag_size = NUM_ATTR_BAGGING_TIMES
        avg_rate = round(sum(validate_outcomes)/len(validate_outcomes),2)

        cur_result = {
            'avg_rate':avg_rate,
            'forest_size': num_trees,
            'bag_size':bag_size,
            'validate_pool_size':data_size,
            'model_training_size':TRAINING_DATA_SIZE,
        }
        
        para_results.append(cur_result)
        print('----------- current result ------------------')
        para_results.sort( key=lambda x:x['avg_rate'])
        pprint(para_results)
        #print(para)
    

    para_results.sort( key=lambda x:x['avg_rate'])
    print('----------- finished ------------------')
    pprint(para_results)

if __name__ =="__main__":
    atexit.register(log_data)
    s1 ='../sampledata/cross200.txt'
    s2 = '../sampledata/iris.txt'
    s3 = '../sampledata/optical-digits.txt'

    sample_input = s2


    # best_parameter
    if sample_input == s3:
        VALIDATE_DATA_SIZE = 80
        TRAINING_DATA_SIZE = 40
        NUM_ATTR_BAGGING_TIMES = 10
        FOREST_SIZE = 150
    elif sample_input == s2:
        VALIDATE_DATA_SIZE = 30
        TRAINING_DATA_SIZE = 10
        NUM_ATTR_BAGGING_TIMES = 10
        FOREST_SIZE = 150
        
    elif sample_input == s1:
        VALIDATE_DATA_SIZE = 20
        TRAINING_DATA_SIZE = 5
        NUM_ATTR_BAGGING_TIMES = 5
        FOREST_SIZE = 40

    main(sample_input)