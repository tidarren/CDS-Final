import numpy as np
from numpy.linalg import norm
import matplotlib.pyplot as plt 
import logging
from time import time
import sys
import argparse


NUM_Of_OBSVS = 200
NUM_OF_COLS = 200
BETA_TRUE_100 = np.array([-1, 1, -1, 1, -1])
BETA_TRUE_200 = np.array([1, -1, 1, -1, 1])
RANDOM_SEED = 0

# MAX_ITER = 10000
MAX_ITER = 10
TOL = 5e-6

# %% [markdown]
# ## Data Generation

# %%
def gennerateX(test=False):
    np.random.seed(RANDOM_SEED) # force to output the same result
    if test:
        n = NUM_Of_OBSVS*10
    else:
        n = NUM_Of_OBSVS
    p = NUM_OF_COLS
    X = np.random.normal(0, 1, size=(n, p, 5))
    return X

def deriveY(obsv):
    np.random.seed(RANDOM_SEED) # force to output the same result
    tmp = obsv[99].dot(BETA_TRUE_100)+obsv[199].dot(BETA_TRUE_200)
    p = np.exp(tmp)/(1+np.exp(tmp))
    y_i = np.random.binomial(size=1, n=1, p=p)
    return y_i

def generateY(X):
    n = X.shape[0]
    y = np.zeros(n)
    for i,obsv in enumerate(X):
        y[i] = deriveY(obsv)
    y = y.reshape(-1,1)
    return y

# %% [markdown]
# ## Loss function construction

# %%
def computeF(x_i, beta):
    return x_i.dot(beta)

def computeGradient(X, y, beta):
    grad = np.zeros(beta.shape)
    f_i_max = 0
    for x_i, y_i in zip(X,y):
        f_i = computeF(x_i, beta)
        if f_i>f_i_max:
            f_i_max=f_i
        # fix exp overflow
        if f_i>709:
            f_i = 709
        grad_tmp = (np.exp(f_i)/(1+np.exp(f_i))-y_i)*x_i
        grad += grad_tmp.reshape(beta.shape)
    logging.debug('f_i_max: {}'.format(f_i_max))
    return grad

# %% [markdown]]
# ## (fast) Proximal Gradient Algorithm
# %%
def hardThresholding(x_j, _lambda):
    """The proximal operator of l0-norm 
    :param x_j:     (float) the j-th element of x
    :param _lambda: (float) penalized term in estimation 
    :return x_j or 0: (float)
    """
    if np.sqrt(2*_lambda)<np.abs(x_j):
        return x_j
    else:
        return 0


def softThresholding(x_j, _lambda):
    """The proximal operator of l1-norm (course_slide_week14 p.17)
    :param x_j:     (float) the j-th element of x
    :param _lambda: (float) penalized term in estimation 
    """
    if x_j>_lambda:
        return x_j-_lambda
    elif x_j<-_lambda:
        return x_j+_lambda
    else:
        return 0


def proxOperator(beta, _lambda, estimation):
    """Proximal operators
    :param beta:       (np.array) 
    :param _lambda:    (float)    penalized term in estimation 
    :param estimation: (str)      determine estimation method
    :return beta_new:  (np.array)  
    """
    beta_new = np.zeros(beta.shape)
    for j in range(beta.shape[0]):
        if estimation=='l0':
            beta_new[j]  = hardThresholding(beta[j], _lambda)
        elif estimation=='l1':
            beta_new[j]  = softThresholding(beta[j], _lambda)
    return beta_new


def getStepsize(X):
    w, _ = np.linalg.eig(X.T.dot(X))
    lambda_1 = max(w)
    c_r = 1/(2*lambda_1)
    return c_r


def initValue(X, zeroValue=False):
    p = X.shape[1]
    if zeroValue:
        beta = np.zeros((p, 1))
    else:
        np.random.seed(RANDOM_SEED) # force to output the same result
        beta = np.random.normal(0, 1, size=(p, 1))
    return beta


def proximalGradient(_lambda, estimation, fast=False, zeroValue=False):
    """(Fast) Proximal Gradient Algorithm.
    :param _lambda:    (float)    penalized term in estimation
    :param fast:       (bool)     determine fast version or not
    :param zeroValue:  (bool)     initialize beta with all zero or not
    :return beta_star: (np.array) trainned beta
    :return h:         (dict)     iteration error history
    """
    beta = initValue(X_train, zeroValue=zeroValue)
    # logging.debug('beta: {}'.format(beta.flatten()))

    h = {} # record history
    h['Euclidean_Norm'] = []
    
    if fast:
        s = 1
        beta_z = beta
    
    for i in range(MAX_ITER):
        if fast:
            beta_tmp = beta_z-c_r*computeGradient(X_train, y_train, beta_z)
            beta_new = proxOperator(beta_tmp.real, _lambda, estimation)
            s_new = (1+np.sqrt(1+4*s**2))/2
            beta_z = beta_new+((s-1)/s_new)*(beta_new-beta)
            
            s = s_new # update for next iteration
        
        else:
            beta_tmp = beta-c_r*computeGradient(X_train, y_train, beta)
            beta_new = proxOperator(beta_tmp.real, _lambda, estimation)        
        
        # report
        euclideanNorm = norm(beta_new-beta,2)
        h['Euclidean_Norm'].append(euclideanNorm) # for plot 1
        
        logging.debug('\niteration: {}'.format(i))
        logging.debug('Euclidean_Norm: {}'.format(euclideanNorm))
        logging.debug('beta_tmp: {}'.format(beta_tmp.real.flatten()[:5]))
        logging.debug('beta_new: {}'.format(beta_new.flatten()[:5]))

        # stopping criterion
        if euclideanNorm<TOL:
            break
        
        beta = beta_new # update for next iteration
    
    # output
    beta_star = beta_new
    
    return beta_star, h

# %% [markdown]]
# ## Report

# %%
def getBetaTrue():
    beta_true = np.zeros((NUM_OF_COLS*5,1))
    # BETA_TRUE_100 = np.array([-1, 1, -1, 1, -1])
    idx_100 = 100*5
    for idx in range(idx_100-5, idx_100):
        for val in BETA_TRUE_100:
            beta_true[idx] = val
    # BETA_TRUE_200 = np.array([1, -1, 1, -1, 1])
    idx_200 = 200*5
    for idx in range(idx_200-5, idx_200):
        for val in BETA_TRUE_200:
            beta_true[idx] = val
    return beta_true


def MSE(beta, beta_true):
    return np.square(norm(beta-beta_true,2))


def err(X,beta,y):
    return np.mean(X.dot(beta)!=y)


def reportTable(betas, _lambdas, beta_true, X_train,y_train, X_test, y_test):
    for beta,_lambda in zip(betas,_lambdas):
        logging.info('\nlambda: {:.6f}'.format(_lambda.real))
        logging.info('MSE: {:.4f}'.format(MSE(beta, beta_true)))
        logging.info('Train Error: {:.4f}'.format(err(X_train, beta, y_train)))
        logging.info('Test Error: {:.4f}'.format(err(X_test, beta, y_test)))


def plot(scale, history_1, history_2, estimation, c_r):
    _lambda = c_r*scale
    plt.figure(figsize=(10,7))
    
    x_1 = range(1,len(history_1['Euclidean_Norm'])+1)
    y_1 = history_1['Euclidean_Norm']
    x_2 = range(1,len(history_2['Euclidean_Norm'])+1)
    y_2 = history_2['Euclidean_Norm']
    
    plt.plot(x_1, y_1, color='black', label='Proximal Gradient Algorithm')
    plt.plot(x_2, y_2, color='red', label='Fast Proximal Gradient Algorithm')
    
    plt.xlabel('Iteration')
    plt.ylabel('Error')
    plt.title('Lambda = {:.6f}'.format(_lambda.real))
    plt.legend()
    plt.savefig('{e}_{s}_{l:.6f}.png'.format(e=estimation, 
                                             s=scale, 
                                             l=_lambda.real))


def main(args):
    scales = [args.scale1, args.scale2]
    _lambdas = [c_r*scale for scale in scales]

    beta_true = getBetaTrue()
    
    betas_1, betas_2 = [], []
    history_1, history_2 = [], []

    for _lambda in _lambdas:
        beta_star, h = proximalGradient(_lambda, 
                                        estimation=args.estimation, 
                                        fast=False)
        beta_star_fast, h_fast = proximalGradient(_lambda, 
                                                  estimation=args.estimation, 
                                                  fast=True)
        betas_1.append(beta_star)
        betas_2.append(beta_star_fast)
        
        history_1.append(h)
        history_2.append(h_fast)
    
    for scale, h1, h2 in zip(scales, history_1, history_2):
        plot(scale, h1, h2, args.estimation, c_r)

    logging.info('\n[Proximal Gradient]')
    reportTable(betas_1, _lambdas, beta_true, X_train, y_train, X_test, y_test)
    logging.info('\n[Fast Proximal Gradient]')
    reportTable(betas_2, _lambdas, beta_true, X_train, y_train, X_test, y_test)

# %%
if __name__ == "__main__":
    logging.basicConfig(format='%(message)s', level=logging.INFO)
    logging.getLogger('matplotlib.font_manager').disabled = True

    parser = argparse.ArgumentParser(description="Final Project")
    parser.add_argument(
        "-e", "--estimation", type=str, 
        help="Choose an estimation method: l0 or l1.", default='l0')
    parser.add_argument(
        "-s1", "--scale1", type=float, 
        help="Choose a scale for lambda.", default=1000)
    parser.add_argument(
        "-s2", "--scale2", type=float, 
        help="Choose a scale for lambda.", default=10000)

    # train
    X_train = gennerateX(test=False)
    y_train = generateY(X_train)
    X_train = X_train.reshape(NUM_Of_OBSVS,-1)
    
    # test
    X_test = gennerateX(test=True)
    y_test = generateY(X_test)
    X_test = X_test.reshape(NUM_Of_OBSVS*10,-1)
    
    # stepsize
    c_r  = getStepsize(X_train)
    
    sys.exit(main(parser.parse_args()))
