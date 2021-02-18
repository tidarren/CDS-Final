# Summary

Find out a shortest cycle path to go through all of the 7-11 in Nangang, Taipei.

![](https://i.imgur.com/s7CIbxc.png)

### Metaheuristic Algorithm

- Genetic Algorithm
- Simulated Annealing
- Particle Swarm Optimization
- Tabu Search

[HackMD Link](https://hackmd.io/@tidarren/Sy7I3Grj8)

# Modern Optimization Methods Final Project

## 1. A Revision on Traveler Salesman Problem. 

**(a) What is TSP?**
中文翻譯「推銷員旅行問題」，給定n個城市及其相互間距離，求取一條經過所有城市各一次的最短循環路徑。

**(b) Find the references (journal papers) that investigate in TSP, state as many as you can.**

1. [The multiple traveling salesman problem: an overview of formulations and solution procedures (Omega, 2006)](https://www.sciencedirect.com/science/article/pii/S0305048304001550?casa_token=55rahsaDbDIAAAAA:2C0z7U_oCA20TdchKgcjQ8AHpyZD3pvZZ35dfQ7j8u_ee4XDYLy6k6rkbpwG-lYWRNfBzN3FfsDr)
2. [A hybrid heuristic for the traveling salesman problem (IEEE 2001)](https://ieeexplore.ieee.org/abstract/document/974843/?casa_token=MIGhIDwo-IwAAAAA:GYtGWSNnVPXgb75O-NtZtgWxmGUvEfBoigvGvXwicttavJncrY2OuI52IeNiqe4ZkJ04fW5QG48)
3. [Genetic algorithm for the traveling salesman problem using sequential constructive crossover operator (IJBB 2010)](https://pdfs.semanticscholar.org/a1e6/50daed4ed9c6a403b08e5d50b3ea9f3b5de4.pdf)
4. [Discrete Particle Swarm Optimization, illustrated by the Traveling Salesman Problem](https://link.springer.com/content/pdf/10.1007%2F978-3-540-39930-8_8.pdf)

**(c.) What are the difficulties in TSP?**
TSP是一個NPC問題，也就是說其時間複雜度隨著城市數量的增加，會比多項式再更高級別的成長。

**(d) What are the applications of TSP in real life?**
- 基因組定序：生成radiation hybrid maps 
- 優化半導體電路中掃描鏈的路徑以降低功耗
- 光纖網路配線


## 2. Data Collection.
**(a) Gather all addresses of Nangang 7-Eleven stores.**
[南港7-11 Google Map](https://www.google.com/maps/d/drive?state=%7B%22ids%22%3A%5B%221vMaXJQafYZ2NWYJ1ti_96OYnB_u07PoV%22%5D%2C%22action%22%3A%22open%22%2C%22userId%22%3A%22113713413174088450892%22%7D&usp=sharing)

**(b) Measure pairwise store distances**
將(a)輸出成kml檔(詳見 `南港7-11.kml`)，並在Google Cloud Program 新增專案，利用Google Map Distance Matrix API，將kml檔中的資訊送出request，再來把response整理即可得到distance matrix。

**(c ) distance matrix**
python 34*34 numpy array in pickle file，詳見 `distance_matrix.pickle`
相對應位置的店名詳見 `distance_matrix_name.pickle`

## 3. An Implementation of Known Metaheuristic Methods.
**State all necessary information**

- particle defnition：一個陣列，元素為數字0~33，每個數字代表南港7-11共34家的其中一家，陣列內的元素不重複，長度為34，最後輸出答案時會於陣列內加入起點以及再多加上回到起點的距離。
- objective function：每個particle代表遍歷各店家的順序，依序將之間的距離加總。
- goal：讓總遍歷長度最小化
- constraints：沒有特別限制


**implement algorithms**
1. GA：詳見`GA_TSP.py`
2. SA：詳見`SA_TSP.py`
3. PSO：詳見`PSO_TSP.py`


## 4. A Self-Study on New Metaheuristic Methods.
**(a) State all necessary information**
同3

**(b) Write a pseudo-code on Tabu Search Algorithm.**
```c
bestSol <- s0 
bestCandidate <- s0
tabuList <- []
tabuList.push(s0)
while (not stoppingCondition()) do # MAX_ITER
    neighborhood <- getNeighbors(bestCandidate) # 1-1 swap method
    bestCandidate <- neighborhood[0]
    for (candidate in neighborhood) do
        if ( (not tabuList.contains(candidate)) and (fitness(candidate) > fitness(bestCandidate)) )
            bestCandidate <- candidate
        end
    end
    if (fitness(bestCandidate) > fitness(bestSol))
        bestSol <- bestCandidate
    end
    tabuList.push(bestCandidate)
    if (tabuList.size > maxTabuSize)
        tabuList.removeFirst()
    end
end
return bestSol
```
**(c ) implement algorithm**
Tabu：詳見`Tabu_TSP.py`

## 5. Method Comparison.

**(a) all parameters & why choose such values**
#### GA
```
POPULATION_SIZE: 300       #和PSO的swarm size統一
NUM_GENERATION: 300        #和各個algorithm統一
CROSSOVER_PROBABILITY: 0.5 #一半的機率作Ordered crossover 
MUTATION_PROBABILITY:  0.5 #一半的機率作swap mutation
```
#### SA
```
Iteration: 300                     #和各個algorithm統一
Temperature_Threshold_Factor: 0.05 #最多降溫95%
Temperature_Reduction_Factor: 0.5  #decay一半
Boltzmann_Constant: 1.0            #簡易化
```

#### PSO
```
Swarm Size: 300 #和GA的POPULATION_SIZE統一
Iteration: 300  #和各個algorithm統一
```

#### Tabu
```
Iteration: 300    #和各個algorithm統一
Tabu List Size: 5 #記太多candidate選擇變少效果不好
```

**(b) Results**

#### GA: 
64212公尺
```
慈愛 -> 向揚 -> 忠陽 -> 經貿 -> 港勝 -> 中研 -> 中貿 -> 馥樺 -> 耀港 -> 聯坊 -> 
研究 -> 港捷 -> 鑫貿 -> 港興 -> 玉成 -> 中坡 -> 玉德 -> 凱松 -> 雄強 -> 林坊 -> 
昆陽 -> 香城 -> 鵬馳 -> 聯成 -> 華技 -> 胡適 -> 港高鐵 -> 港泰 -> 港環球 -> 港麗 -> 
庄研 -> 港運 -> 新福玉 -> 港德 -> 慈愛
```
![](https://i.imgur.com/yNDijJ3.png)


#### SA: 
78446公尺
```
林坊 -> 鵬馳 -> 香城 -> 耀港 -> 雄強 -> 玉成 -> 港興 -> 港捷 -> 港勝 -> 中研 -> 
經貿 -> 昆陽 -> 鑫貿 -> 慈愛 -> 港運 -> 凱松 -> 新福玉 -> 聯成 -> 華技 -> 胡適 -> 
忠陽 -> 聯坊 -> 向揚 -> 中坡 -> 馥樺 -> 玉德 -> 港環球 -> 港高鐵 -> 港德 -> 港泰 -> 
中貿 -> 研究 -> 庄研 -> 港麗 -> 林坊
```
![](https://i.imgur.com/sQ3vYaq.png)

#### PSO: 
43159公尺
```
港德 -> 昆陽 -> 新福玉 -> 中坡 -> 凱松 -> 港泰 -> 港環球 -> 玉德 -> 林坊 -> 港麗 -> 
馥樺 -> 港興 -> 慈愛 -> 胡適 -> 中研 -> 華技 -> 庄研 -> 經貿 -> 香城 -> 港勝 -> 
港捷 -> 耀港 -> 研究 -> 中貿 -> 鑫貿 -> 港高鐵 -> 玉成 -> 港運 -> 聯成 -> 向揚 -> 
鵬馳 -> 忠陽 -> 雄強 -> 聯坊 -> 港德
```
![](https://i.imgur.com/Aonckqg.png)

### Tabu
31747公尺
```
港興 -> 港高鐵 -> 港捷 -> 港勝 -> 經貿 -> 港麗 -> 聯成 -> 林坊 -> 玉德 -> 中坡 -> 
港運 -> 凱松 -> 鵬馳 -> 向揚 -> 玉成 -> 忠陽 -> 昆陽 -> 研究 -> 中研 -> 庄研 -> 
華技 -> 胡適 -> 耀港 -> 港泰 -> 港環球 -> 港德 -> 新福玉 -> 聯坊 -> 雄強 -> 慈愛 -> 
馥樺 -> 鑫貿 -> 中貿 -> 香城 -> 港興
```
![](https://i.imgur.com/QCNK0lF.png)


**(c ) computational times**


| Algorithm | time      |
| --------- | --------- |
| GA        | 0m5.352s  |
| SA        | 0m0.249s  |
| PSO       | 0m20.248s |
| Tabu      | 0m29.012s  |


## 6. Conclusion.
**(a) Summarize your comparison results on four methods.**
統一限制迭代次數為300的情況下，Tabu花的時間最長，但效果也最好，僅31747公尺。
SA的效果不甚理想，僅比隨機順序好一些。
GA較SA稍好一些，但仍不易產生選擇附近的後代。
PSO又更好一些，路線有明顯的分群，不會再頻繁的跨群，但群內還是稍嫌劇烈。
Tabu的效果則更好，既沒有那麼頻繁的跨群，群內方面也沒PSO劇烈。
整體來說，都較無法選擇到附近店家走。

**(b) State the advantages and disadvantages of all four methods shown in this application to TSP.**
在限制相同迭代次數的情況下，GA、SA等算法算是相當快速，但要選擇到附近的點去走還是相當困難。
SA的perturb相當於1-1 swap，每次迭代僅這樣效果不彰。
GA相對應1-1 swap算是mutation，此外在之前多做crossover，但改善仍有限。
PSO雖說計算時間稍長，但「速度」相當於多次的1-1 swap，推測在和localBest或globalBest多次比較下，能有效避免跨群頻繁的現象。
Tabu所需的計算時間最長，但由於在找neighborhood階段即已過濾出1-1 swap最好的方式，故又更能有效避免群內劇烈。

**(c ) State at least one potential improvement on the best method to make the algorithm even better on this TSP application.**

改變initalization策略，不再使用random initalization。

### Redundant Resolution Strategy
給定一個起始點，選擇離當前最近的店家走且不重複，依序走回起始點。

#### Baseline: 
28178公尺
```
中坡 -> 玉德 -> 林坊 -> 聯坊 -> 雄強 -> 昆陽 -> 忠陽 -> 玉成 -> 鵬馳 -> 向揚 -> 
慈愛 -> 港興 -> 港泰 -> 港環球 -> 港高鐵 -> 香城 -> 經貿 -> 港勝 -> 馥樺 -> 鑫貿 -> 
中貿 -> 耀港 -> 港捷 -> 研究 -> 胡適 -> 庄研 -> 華技 -> 中研 -> 聯成 -> 港麗 -> 
港運 -> 凱松 -> 新福玉 -> 港德 -> 中坡 
```
![](https://i.imgur.com/l7eAT0T.png)

這個策略的效果已經相當不錯，但很明顯的可以看到還是有一條跨群的路徑。


#### 將Baseline作為 initalization，再使用Tabu: 
24071公尺
```
中坡 -> 玉德 -> 林坊 -> 聯坊 -> 聯成 -> 昆陽 -> 忠陽 -> 鵬馳 -> 玉成 -> 向揚 -> 
慈愛 -> 港興 -> 港高鐵 -> 港泰 -> 港環球 -> 經貿 -> 香城 -> 馥樺 -> 港勝 -> 港捷 -> 
鑫貿 -> 中貿 -> 研究 -> 胡適 -> 華技 -> 庄研 -> 中研 -> 耀港 -> 港麗 -> 雄強 -> 
港運 -> 凱松 -> 港德 -> 新福玉 -> 中坡
```
![](https://i.imgur.com/s7CIbxc.png)

可以看到比之baseline已沒有那條跨群的路徑，且之前ramdom initalization所遇到的跨群頻繁和群內劇烈等問題都大幅改善。

也試著在GA、SA和PSO使用，但效果不彰。