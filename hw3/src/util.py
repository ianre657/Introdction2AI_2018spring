import re
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

def main(fname):
    data_list = []
    with open(fname, 'r') as input_file:
        for line in input_file.readlines():
            line = line.strip()
            if line!='':
                learn_data = LearningData([i for i in re.split('\s|,', line) if i !=''])
                data_list.append(learn_data)
        #pprint(data_list, compact=True)
        out = make_histogram(data_list)
        print(f'out {out}: impurity:{gini_impurity(out)}')

if __name__ =="__main__":
    s1='../sampledata/cross200.txt'
    s2 = '../sampledata/iris.txt'
    s3 = '../sampledata/optical-digits.txt'
    main(s3)
    #im = gini_impurity([30,10])
    #print(f'impurity:{im}')