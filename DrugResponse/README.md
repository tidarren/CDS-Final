

# Summary

The classification problem of the drug response of Lapatinib, with IC50 of 2.0 as threshold.

| Feature Selection   | Recall | Precision | F1       |
| ------------------- | ------ | --------- | -------- |
| None                | 0.95   | 0.09      | 0.17     |
| removeLowVar(80%)   | 0.25   | 0.36      | 0.29     |
| ANOVA(80%)          | 0.04   | 0.18      | 0.07     |
| LinearSVC(65)       | 0.63   | 0.17      | 0.28     |
| **ExtraTree(1628)** | 0.38   | 0.35      | **0.36** |

[HackMD Link](https://hackmd.io/@tidarren/SJ9R3bwhI)

# Project: DrugResponse_Lapatinib (Team 1)

## 1. Data Overview
### 1.1 Training Data
GDSC (Genomics of Drug Sensitivity in Cancer)
- number of samples: 396 (postive: 25 / negative: 371, threshold: 2.0) 
- number of features: 17489 (including `CELL_LINE_NAME` & `IC50`)

### 1.2 Testing Data
CCLE (Cancer Cell Line Encyclopedia)
- number of samples: 470 (postive: 44 / negative: 426, threshold: 2.0) 
- number of features: 17183 (including `CELL_LINE_NAME` & `IC50`)

## 2. Preprocess & Thinking
留下GDSC和CCLE共同有的features，剛好CCLE有的feature GDSC也都有，故最後選擇完的feature總數為17181 (17183減去`CELL_LINE_NAME`和`IC50`兩項)。

觀察資料可以發現以下兩點：
1. feature總數遠大於samples數
2. data是imblanced

首先，將此次任務視為分類問題，因應上述第一點，先feature selection以降維，再使用SVM作為分類模型。
再者，因應第二點，使用 Oversampling。

## 3. Approach
### 3.1 Feature Selection
本次任務所使用的feature selection方法可分為以下4種：
1. Removing features with low variance: removeLowVar
2. univariate statistical test: ANOVA
3. L1-based: LASSO、LinearSVC
4. tree-based: ExtraTree


### 3.2 Classifier
本次任務所使用到的Classifier有以下3種：
1. SVM: `sklearn.svm.SVC`
2. linear SVM: `sklearn.svm.LinearSVC`
3. XGBoost: `xgboost.XGBClassifier`

主要使用SVM，且基本上先都使用default setting，針對peformance較好的才會再finetune。

### 3.3 Oversampling
針對imblanced data，使用 Synthetic Minority Oversampling Technique (SMOTE)

## 4. Experiments 

### 4.1 Classifier: SVM 
| Feature Selection            | Recall | Precision | F1   | Recall | Precision | F1   |
| ---------------------------- | ------ | --------- | ---- | ------ | --------- | ---- |
| None                         | 0.0    | 0.0       | 0.0  | 0.0    | 0.0       | 0.0  |
| LASSO(59)                    | 0.36   | 1.0       | 0.52 | 0.0    | 0.0       | 0.0  |
| removeLowVar(80%)+ Lasso(62) | 0.44   | 1.0       | 0.61 | 0.0    | 0.0       | 0.0  |
| removeLowVar(80%)            | 0.2    | 1.0       | 0.33 | 0.0    | 0.0       | 0.0  |
| ANOVA(80%)                   | 0.2    | 1.0       | 0.33 | 0.0    | 0.0       | 0.0  |
| ANOVA(80%) + LASSO(67)       | 0.48   | 1.0       | 0.64 | 0.0    | 0.0       | 0.0  |
| LinearSVC(7)                 | 0.52   | 1.0       | 0.68 | 0.02   | 0.25      | 0.04 |
| ExtraTree(1128)              | 0.88   | 1.0       | 0.93 | 0.0    | 0.0       | 0.0  |


Feature Selection 中括號所代表的是最後所選的features數或是占比，表格先顯示 training set (GDSC)的各項metric，再顯示 testing set (CCLE)的。

由table 4.1 可知，training set的performance大部分不是表現的很好，而testing set更不用說，懷疑主要原因是imblanced data，故將training set 作 oversampling

### 4.2 Oversampling + SVM 
| Feature Selection | Recall | Precision | F1   | Recall | Precision | F1   |
| ----------------- | ------ | --------- | ---- | ------ | --------- | ---- |
| None              | 1.0    | 0.95      | 0.97 | 0.0    | 0.0       | 0.0  |
| removeLowVar(80%) | 1.0    | 1.0       | 1.0  | 0.0    | 0.0       | 0.0  |
| ANOVA(80%)        | 1.0    | 1.0       | 1.0  | 0.04   | 0.18      | 0.07 |
| LinearSVC(65)     | 1.0    | 1.0       | 1.0  | 0.0    | 0.0       | 0.0  |
| ExtraTree(1628)   | 1.0    | 1.0       | 1.0  | 0.0    | 0.0       | 0.0  |

Training set Oversampling 
- Before: number of samples: 396 (postive: 25 / negative: 371, threshold: 2.0) 
- After:  number of samples: 472 (postive: 371 / negative: 371, threshold: 2.0) 

由於使用Oversampling須先將 label轉為binary的形式，故之後用到Oversampling LASSO皆不適用。

由table 4.2 可知，training的performance有效地提升，不過因為testing仍不甚理想，懷疑可能overfitting，或是classifier、也就是default setting的SVM需要再調整。
而oversmapling後，包含像是`LinearSVC`和`ExtraTree`所選的feature數，都有所更動：
- `LinearSVC`: 7 > 65
- `ExtraTree`: 1128 > 1628

### 4.3 Oversampling + SVM with linear kernel (SVC)
| Feature Selection | Recall | Precision | F1  | Recall | Precision | F1       |
| ----------------- | ------ | --------- | --- | ------ | --------- | -------- |
| None              | 1.0    | 1.0       | 1.0 | 0.65   | 0.20      | 0.31     |
| removeLowVar(80%) | 1.0    | 1.0       | 1.0 | 0.59   | 0.23      | 0.33     |
| **ANOVA(80%)**    | 1.0    | 1.0       | 1.0 | 0.38   | 0.30      | **0.34** |
| LinearSVC(65)     | 1.0    | 1.0       | 1.0 | 0.75   | 0.12      | 0.22     |
| ExtraTree(1628)   | 1.0    | 1.0       | 1.0 | 0.25   | 0.30      | 0.27     |

將SVM default setting中的kernel function從`rbf`改成`linear`。，並作5-fold的cross-validation。
由table 4.3可知，testing的performance都有效地提升，而以F1 metric來看，表現最好的是在選擇feature時使用ANOVA留下八成的feature。


### 4.4 Oversampling + linear SVM (LinearSVC)
| Feature Selection   | Recall | Precision | F1  | Recall | Precision | F1       |
| ------------------- | ------ | --------- | --- | ------ | --------- | -------- |
| None                | 1.0    | 1.0       | 1.0 | 0.95   | 0.09      | 0.17     |
| removeLowVar(80%)   | 1.0    | 1.0       | 1.0 | 0.25   | 0.36      | 0.29     |
| ANOVA(80%)          | 1.0    | 1.0       | 1.0 | 0.04   | 0.18      | 0.07     |
| LinearSVC(65)       | 1.0    | 1.0       | 1.0 | 0.63   | 0.17      | 0.28     |
| **ExtraTree(1628)** | 1.0    | 1.0       | 1.0 | 0.38   | 0.35      | **0.36** |

這邊嘗試使用不同的Classifier：linear SVM (`LinearSVC`)
由table 4.4可知，以F1 metric來看，表現最好的是在選擇feature時使tree-based的ExtraTree。
這邊補充 SVM with linear kernel `SVC(kernel='linear')`和 `LinearSVC`的差別，主要有以下兩點：
1. 目標函數不同：`SVC`就只是minimize hinge loss，而`LinearSVC`則是minimize squared hinge loss
2. 懲罰截距與否：`LinearSVC`的estimators是liblinear，會penalize the intercept，`SVC`則不會。

### 4.5 Oversampling + XGBoost
| Feature Selection | Recall | Precision | F1  | Recall | Precision | F1   |
| ----------------- | ------ | --------- | --- | ------ | --------- | ---- |
| None              | 1.0    | 1.0       | 1.0 | 0.0    | 0.0       | 0.0  |
| removeLowVar(80%) | 1.0    | 1.0       | 1.0 | 0.0    | 0.0       | 0.0  |
| ANOVA(80%)        | 1.0    | 1.0       | 1.0 | 0.06   | 0.17      | 0.09 |
| LinearSVC(65)     | 1.0    | 1.0       | 1.0 | 0.40   | 0.13      | 0.19 |
| ExtraTree(1628)   | 1.0    | 1.0       | 1.0 | 0.79   | 0.09      | 0.17 |

這邊也嘗試使用另一個的Classifier：XGBoost
不過由table 4.4可知，testing 的performance不是很理想。


## 5. Conclusion
若以F1作為最終評斷best method的依據，4.4 的方法，也就是先作Oversampling，feature selection使用ExtraTree選出1628個features，Classifier則使用linear SVM (`LinearSVC`)，performance是最好的。
以下再附上針對Regularization parameter finetune，和5-fold cross-validation後的結果


### Best Method: Oversampling + linear SVM (LinearSVC)
| Feature Selection   | Recall | Precision | F1  | Recall | Precision | F1       |
| ------------------- | ------ | --------- | --- | ------ | --------- | -------- |
| **ExtraTree(1628)** | 1.0    | 1.0       | 1.0 | 0.38   | 0.35      | **0.36** |
