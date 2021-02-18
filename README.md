# CDS Final Project
Computation in Data Science (NTU Course 2020 Spring)

## Final Project Overview

- TravelerSalesmanProblem
- DrugResponse
- LogisticRegressionEstimation

## TravelerSalesmanProblem

Find out a shortest cycle path to go through all of the 7-11 in Nangang, Taipei.

![](https://i.imgur.com/s7CIbxc.png)

### Metaheuristic Algorithm

- Genetic Algorithm
- Simulated Annealing
- Particle Swarm Optimization
- Tabu Search

[Detailed Report @HackMD](https://hackmd.io/@tidarren/Sy7I3Grj8)



## DrugResponse

The classification problem of the drug response of Lapatinib, with IC50 of 2.0 as threshold.

| Feature Selection   | Recall | Precision | F1       |
| ------------------- | ------ | --------- | -------- |
| None                | 0.95   | 0.09      | 0.17     |
| removeLowVar(80%)   | 0.25   | 0.36      | 0.29     |
| ANOVA(80%)          | 0.04   | 0.18      | 0.07     |
| LinearSVC(65)       | 0.63   | 0.17      | 0.28     |
| **ExtraTree(1628)** | 0.38   | 0.35      | **0.36** |

[Detailed Report @HackMD](https://hackmd.io/@tidarren/SJ9R3bwhI)



## LogisticRegressionEstimation

Estimate a logistic regression model using different estimation methods and dierent optimization algorithms.

| Estimation + Algorithm | lambda   | MSE      | Err_train | Err_test |
| ---------------------- | -------- | -------- | --------- | -------- |
| zero + PG              | 2.413233 | 190.1131 | 1.0000    | 1.0000   |
| zero + FPG             | 2.413233 | 166.2967 | 1.0000    | 1.0000   |
| lasso + PG             | 2.413233 | 10.0000  | 0.4850    | 0.50750  |
| lasso + FPG            | 2.413233 | 10.0000  | 0.4850    | 0.50750  |

[Detailed Report @HackMD](https://hackmd.io/@tidarren/ryilE4J0I)



## Contact

If you have any question, please feel free to contact me by sending email to [r08946014@ntu.edu.tw](mailto:r08946014@ntu.edu.tw)

