# HW3

    Introdunction to AI @ NCTU, Spring 2018
    0411276 陳奕安
    測試環境: 
        OS: Ubuntu Linux with cpython 3.6.5
        CPU: Intel i7-4790 (4C8T)
        RAM: 16GB.

## Achievements

##### Basic

* 根據給予的資料建立搜尋樹(CART)
* 實作 Tree bagging, Attribute Bagging
* 實作 Random Forests
* 利用 Cross validation 手法進行驗證

##### Extra Effort

* 提升驗證結果的穩定程度，以及確定驗證資料在總資料集中涵蓋的完整性
* 平行化訓練模型以及驗證的過程
* 給予一定的資料點範圍，程式能透過普查的方式找出最適合的訓練參數

## 實驗結果

##### 驗證方法

所有的資料會被分成兩種，驗證用以及訓練用的資料，且實際驗證時的資料組是由驗證資料中隨機抽取特定筆數來進行驗證。必須先澄清，訓練模型用的資料跟驗證用的資料是完全不重疊的，以此方法比較能夠確定訓練出來的模型有學習到真正模型的情況。再者，在每一輪的測試中，都盡量保證驗證資料必須包含到所有可能label的資料集，如此一來才不會造成驗證資料的過度偏頗。

###### 效能評估

|資料集|最高平均模型正確率|
|:-:|:-:|
|cross200|76.5%|
|iris|98%|
|optical-digits|83.64%|

## 實作簡述



## 實驗心得