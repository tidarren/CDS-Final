# Summary

Estimate a logistic regression model using different estimation methods and dierent optimization algorithms.

| Estimation + Algorithm | lambda   | MSE      | Err_train | Err_test |
| ---------------------- | -------- | -------- | --------- | -------- |
| zero + PG              | 2.413233 | 190.1131 | 1.0000    | 1.0000   |
| zero + FPG             | 2.413233 | 166.2967 | 1.0000    | 1.0000   |
| lasso + PG             | 2.413233 | 10.0000  | 0.4850    | 0.50750  |
| lasso + FPG            | 2.413233 | 10.0000  | 0.4850    | 0.50750  |

[HackMD Link](https://hackmd.io/@tidarren/ryilE4J0I)

Final Project
===

## 1. Line plots for iteration errors (2%):
### Estimation Method: zero
![](https://i.imgur.com/KjsrEVb.png)

![](https://i.imgur.com/qPUiWny.png)


## 2. Line plots for iteration errors (2%):
### Estimation Method: lasso
![](https://i.imgur.com/b3C80re.png)

![](https://i.imgur.com/rWBY70w.png)


## 3. Table for performance measures (6%)
| Estimation + Algorithm | lambda | MSE    | Err_train | Err_test |
| -------------------- | ----------- | -------- | ------------- | ------------ |
| zero + PG            | 2.413233    | 190.1131 | 1.0000        | 1.0000       |
| zero + FPG           | 2.413233    | 166.2967 | 1.0000        | 1.0000       |
| lasso + PG           | 2.413233    | 10.0000  | 0.4850        | 0.50750      |
| lasso + FPG          | 2.413233    | 10.0000  | 0.4850        | 0.50750      |


## Commands and raw output
### Estimation Method: zero
```
$ python final.py -e l0
```
```
[Proximal Gradient]

lambda: 0.241323
MSE: 894.8769
Train Error: 1.0000
Test Error: 1.0000

lambda: 2.413233
MSE: 190.1131
Train Error: 1.0000
Test Error: 1.0000

[Fast Proximal Gradient]

lambda: 0.241323
MSE: 882.8088
Train Error: 1.0000
Test Error: 1.0000

lambda: 2.413233
MSE: 166.2967
Train Error: 1.0000
Test Error: 1.0000
```

### Estimation Method: lasso
```
$ python final.py -e l1
```
```
[Proximal Gradient]

lambda: 0.241323
MSE: 10.9661
Train Error: 1.0000
Test Error: 1.0000

lambda: 2.413233
MSE: 10.0000
Train Error: 0.4850
Test Error: 0.5075

[Fast Proximal Gradient]

lambda: 0.241323
MSE: 10.0000
Train Error: 0.4850
Test Error: 0.5075

lambda: 2.413233
MSE: 10.0000
Train Error: 0.4850
Test Error: 0.5075
```
