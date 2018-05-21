import re
import math
from pprint import pprint
from typing import List

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

class decision_tree_node:
    def __init__(self):
        ...

class decision_node:
    def __init__(self, ldatas:List[LearningData]):
        self.
        ...

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

def calc_split_val(data_list,attr_idx:int ) -> List[float]:
    '''以平均數作為分割點
    '''
    values = [d.data[attr_idx] for d in data_list]
    #拿取不重複的點
    values = list(set(values))
    values.sort()


    mid_points = []
    for i in range(len(values)-1):
        mid_points.append( (values[i] + values[i+1])/2 )
    #print(f'values:{values}')
    #print(f'md_pts:{mid_points}')
    return mid_points

def select_split_node( data_list: List[LearningData]) -> int,int:
    '''回傳最適合作為分割點的index以及分割後的impurity
    '''
    min_imp = math.inf
    min_atr_idx = None
    
    min_info = { 'sp_impurity':None, 'atr_idx': None, 'val':None}
        
    for atr_idx in range(len(data_list[0].data)):
        mid_vals = calc_split_val(data_list,atr_idx)
        for val in mid_vals:
            low, high = split_list(data_list,atr_idx,val)
            low_imp = calc_data_list_impurity(low)
            high_imp = calc_data_list_impurity(high)
            split_impurity = low_imp+high_imp
            if split_impurity < origin_impurity:
                print(f'atr:{atr_idx}, val:{val:.3f},  split imp:{split_impurity:.3f}')
                if split_impurity < min_info['sp_impurity']:
                    min_info['sp_impurity'] = split_impurity
                    min_info['atr_idx'] = atr_idx
                    min_info['val'] = val
    for k,v in min_info.items():
        print(f'{k}:{v}')


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

        min_info = { 'sp_impurity':origin_impurity, 'atr_idx': None, 'val':None}
        
        for atr_idx in range(len(data_list[0].data)):
            #print(f'atr_idx :{atr_idx}')
            mid_vals = calc_split_val(data_list,atr_idx)
            #print(f'mds:{mid_vals}')
            for val in mid_vals:
                low, high = split_list(data_list,atr_idx,val)
                low_imp = calc_data_list_impurity(low)
                high_imp = calc_data_list_impurity(high)
                sp_val = low_imp+high_imp
                if sp_val < origin_impurity:
                    print(f'atr:{atr_idx}, val:{val:.3f},  split imp:{sp_val:.3f}')
                    if sp_val < min_info['sp_impurity']:
                        min_info['sp_impurity'] = sp_val
                        min_info['atr_idx'] = atr_idx
                        min_info['val'] = val
        for k,v in min_info.items():
            print(f'{k}:{v}')
        #pprint(f'low list:{low}')        


if __name__ =="__main__":
    s1='../sampledata/cross200.txt'
    s2 = '../sampledata/iris.txt'
    s3 = '../sampledata/optical-digits.txt'
    main(s2)
    #im = gini_impurity([30,10])
    #print(f'impurity:{im}')