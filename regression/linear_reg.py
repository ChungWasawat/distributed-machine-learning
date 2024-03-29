import os
import numpy as np
import pandas as pd
from numpy.random import seed, randn, shuffle

from sklearn.preprocessing import StandardScaler
from linear_reg_func import lin_reg

import matplotlib.pyplot as plt


def gradient(pos, theta, x, y):
    if pos==0:
        # print(pos, theta[0,pos], y)
        return theta[0,pos] - y
    else:
        # print(pos, theta[0,pos], x[pos-1])
        return gradient(pos-1, theta, x, y) + (theta[0,pos] * x[pos-1])
  
def contour(m, path, lr):
    plt.figure()
    x,y = m[0], m[1]
    plt.xlim(-x*3, x*3)
    plt.ylim(-y*7, y*7)
    plt.grid()
    
    for i in range(path.shape[0]-1):
        if i == 0:
            plt.annotate('', xy=path[i + 1, :], xytext=path[i, :],
                         arrowprops={'arrowstyle': '->', 'color': 'green', 'lw': 1},
                         va='center', ha='center')
        else:
            plt.annotate('', xy=path[i + 1, :], xytext=path[i, :],
                         arrowprops={'arrowstyle': '->', 'color': 'red', 'lw': 1},
                         va='center', ha='center')            
        
    plt.plot(x, y, marker="o", markersize=10, markeredgecolor="blue", markerfacecolor="none", zorder=10)
    title = f"learning rate = {lr}"
    plt.title(title)
    plt.xlabel("theta1")
    plt.ylabel("theta2")
    plt.show()
    
def converge(error, step, lr):
    if step > 300:
        step = 300
    
    plt.figure()
    plt.xlim(0, step)
    plt.plot(error, color = 'b')
    title = f"learning rate = {lr}"
    plt.title(title)
    plt.xlabel("step")
    plt.ylabel("error")
    plt.show()
    
"""
Data1 has the following inputs:
1. Frequency, in Hertzs.
2. Angle of attack, in degrees.
3. Chord length, in meters.
4. Free-stream velocity, in meters per second.
5. Suction side displacement thickness, in meters.

The only output is:
6. Scaled sound pressure level, in decibels.
"""

path = os.getcwd()

data1 = path + "\data\\airfoil_self_noise.dat"
col1 = ['freq', 'angle', 'chord', 'velocity', 'thickness', 'sound']
df1 = pd.read_table(data1, sep="\t", names=col1)

n = 5
if n ==2:
    X = df1.values[:, 1::3] #angle and thickness
if n >2:
    X = df1.values[:, 0:n] 
y = df1.values[:, 5]

##########################################################
###### linear regression 

model = lin_reg(X,y)
print("from linear regression", model.intercept_.round(decimals=3), model.coef_.round(decimals=3))

col_table = ["model", "learning rate", "batch", "epoch", "intercept"]
table = [["linear regression", 0, 0, 0, model.intercept_.round(decimals=3)]]
for z in range(model.coef_.size):
    table[0].append(model.coef_[z].round(decimals=3))
    col_table.append(f"theta{z+1}")

##########################################################
###### stochastic gradient descent

learning_rate = [0.01]
# learning_rate = [0.005, 0.01, 0.05, 0.1]
epoch =30
batch_size = 128
nrows = X.shape[0]

#threshold for convergence
conv = 5

## standardisation
std_scaler = StandardScaler()
X = std_scaler.fit_transform(X)
all_data = np.c_[X,y].copy()

old_theta = []
errors = []

for lr in learning_rate:
    seed(42)
    theta = randn(1, X.shape[1]+1)
    old_th = []
    old_th.append(theta[:,1:].reshape(theta.size-1,))
    error = []
    
    for i in range(epoch):
        shuffle(all_data)
        train_x = all_data[:, :-1]
        train_y = all_data[:, -1] 
        
        for start in range(0, nrows):
            y_hat = gradient(theta.size-1, theta, train_x[start], train_y[start])
            
            # threshold epsilon to stop before 
            if abs(loss) < conv:
                print("epoch= ",i," row= ", start)
                break
            
            for j in range(theta.size):
                if j ==0:
                    temps = theta[0,j] - (lr * y_hat)
                else:
                    temp = theta[0,j] - (lr * y_hat * train_x[start,j-1] )
                    temps = np.c_[temps,temp]        
            theta = temps
            
            # store only for a start point or every batch
            if start == 0 or (start+1) % batch_size == 0:
                old_th.append(theta[:,1:].reshape(theta.size-1,))
            # store only for the first iteration.
            if i ==0:
                loss = 0.5 * ((y_hat)**2 )
                error.append(abs(loss))
            
        if abs(loss) < conv:
            break
        
    print("learning rate=", lr, theta.flatten().round(decimals=3))    
    temp_table = ["sgd", lr, 0, epoch]
    for z in theta.flatten():
        temp_table.append(z.round(decimals=3))
    table.append(temp_table)
    
    old_theta.append(old_th)    
    errors.append(error)

# visualisation
## gradient
for lr in range(len(learning_rate)):
    all_w = np.array(old_theta[lr])
    if all_w.shape[1] > 2:
        break
    contour(model.coef_, all_w, learning_rate[lr])    
## error
for lr in range(len(learning_rate)):
    all_e = np.array(errors[lr])
    converge(all_e, len(errors[lr]), learning_rate[lr])
    

##########################################################
####### stochastic gradient descent (mini-batch)
mini_batch = False

if mini_batch == True:
    epoch =40
    old_theta = []
    errors = []
    all_data = np.c_[X,y].copy()
    
    for lr in learning_rate:
        seed(42)
        theta = randn(1, X.shape[1]+1)
        sum_grad = np.zeros(theta.shape)
        
        old_th = []
        old_th.append(theta[:,1:].reshape(theta.size-1,))
        error = []
        
        for i in range(epoch):
            shuffle(all_data)
            train_x = all_data[:, :-1]
            train_y = all_data[:, -1]
            for start in range(0, nrows):
                #stop = start + batch_size
                y_hat = gradient(theta.size-1, theta, train_x[start], train_y[start])
                     
                for j in range(theta.size):
                    if j ==0:
                        temps = y_hat
                    else:
                        temp = y_hat * train_x[start,j-1] 
                        temps = np.c_[temps,temp]              
                sum_grad += temps
                
                if (start+1) % batch_size == 0 or start == nrows -1: 
                    if start == nrows-1:
                        
                        sum_grad /= (nrows%batch_size)
                    else:
                        sum_grad /= batch_size
                    theta = theta - (lr * sum_grad)
                    sum_grad = np.zeros(theta.shape)
                    
                    old_th.append(theta[:,1:].reshape(theta.size-1,)) 
                    loss = 0.5 * ((y_hat)**2 )
                    error.append(abs(loss))
            
                # threshold epsilon to stop before 
                if abs(loss) < conv:
                    print("epoch= ",i," row= ", start)
                    break
            if abs(loss) < conv:
                break
        print("learning rate=", lr, theta.flatten().round(decimals=3))    
        temp_table = ["sgd with mini-batch", lr, batch_size, epoch]
        for z in theta.flatten():
            temp_table.append(z.round(decimals=3))
        table.append(temp_table)   
        
        old_theta.append(old_th)    
        errors.append(error)
    
    # visualisation
    ## gradient
    for lr in range(len(learning_rate)):
        all_w = np.array(old_theta[lr])
        if all_w.shape[1] > 2:
            break
        contour(model.coef_, all_w, learning_rate[lr])    
    ## error
    for lr in range(len(learning_rate)):
        all_e = np.array(errors[lr])
        converge(all_e, len(errors[lr]), learning_rate[lr])

# data2 = path + "\csv\\reg_normal_sgd.csv"
# df999 = pd.DataFrame(table, columns=col_table)
# df999.to_csv(data2, index=False)