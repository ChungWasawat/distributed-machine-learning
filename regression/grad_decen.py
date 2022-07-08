import os

from collections import Counter
from math import floor, ceil

import numpy as np
import pandas as pd
from numpy.random import seed
from numpy.random import randn
from numpy.random import uniform
from numpy.random import shuffle
# from sklearn.linear_model import LinearRegression
# from sklearn.preprocessing import StandardScaler

# import matplotlib.pyplot as plt

def theta_init(seed_num: int, row: int) -> np.array:
    seed(seed_num)
    theta = randn(1, row).flatten()
    return theta[0], theta[1:]

def y_hat(w: np.array, X: np.array, b: np.array) -> np.array:
    X_T = X.reshape(X.size,1)
    xx = np.dot(w.reshape(1, w.size), X_T).flatten() + b
    return xx

def compute_grad(y_h,y ,X_T):
    loss = y_h-y
    grad = loss * X_T
    return grad.flatten()

def cost(y_h,y):
    return 0.5 * ((y_h-y)**2)

def all_grad():
####################################################################

    return 0


# def contour(m, path, lr, node):
#     plt.figure()
#     x,y = m[0], m[1]
#     plt.xlim(-x*3, x*3)
#     plt.ylim(-y*7, y*7)
#     plt.grid()
    
#     for i in range(path.shape[0]-1):
#         if i == 0:
#             plt.annotate('', xy=path[i + 1, :], xytext=path[i, :],
#                          arrowprops={'arrowstyle': '->', 'color': 'green', 'lw': 1},
#                          va='center', ha='center')
#         else:
#             plt.annotate('', xy=path[i + 1, :], xytext=path[i, :],
#                          arrowprops={'arrowstyle': '->', 'color': 'red', 'lw': 1},
#                          va='center', ha='center')            
        
#     plt.plot(x, y, marker="o", markersize=10, markeredgecolor="blue", markerfacecolor="none", zorder=10)
#     title = f"learning rate = {lr}, node = {node}"
#     plt.title(title)
#     plt.xlabel("theta1")
#     plt.ylabel("theta2")
#     plt.show()

# def converge(error, step, lr):
#     plt.figure()
#     plt.xlim(0, step)
#     plt.plot(error, color = 'b')
#     title = f"learning rate = {lr}"
#     plt.title(title)
#     plt.xlabel("step")
#     plt.ylabel("error")
#     plt.show()

def random_network(node: int, p: float) -> np.array:
    nw = np.zeros((node,node))

    route = {}
    for i in range(node):
        route[i] = []

    c = (node **2)
    for i in range(node-1,0,-1):
        c -= i

    i,j = 0,0
    while c > 0:
        if i==j:
            nw[i,j] = 1
            nw[j,i] = 1
        else:
            x = uniform(0,1)
            if x <= p:
                nw[i,j] = 1
                nw[j,i] = 1 
                if j not in route[i]:
                    route[i].append(j)  
                    route[j].append(i)
        j+=1
        if j == node:
            i += 1
            j = i
        c -=1
    return nw, route

def visit_adj(adj_m:dict, node:int, neighbour:int, visited:list) -> list:
    if adj_m[node] == []:
        #print("case0", node, neighbour, "nothing", visited)
        visited.append(node)
        return visited
    elif adj_m[node] == [] and node == len(adj_m.keys())-1:
        #print("case0.5", node, neighbour, "nothing", visited)
        return visited 
    if visited[node] == False:
        visited[node] = True
    if visited[adj_m[node][neighbour]] ==True and adj_m[node][neighbour] == adj_m[node][-1]:
        #print("case1", node, neighbour, adj_m[node][neighbour], visited)
        return visited
    elif visited[adj_m[node][neighbour]] ==True :
        #print("case2", node, neighbour, adj_m[node][neighbour], visited)
        return visit_adj(adj_m, node, neighbour+1, visited) 
    elif visited[adj_m[node][neighbour]] == False and adj_m[node][neighbour] == adj_m[node][-1]:
        #print("case3", node, neighbour, adj_m[node][neighbour], visited)
        return visit_adj(adj_m, adj_m[node][neighbour], 0, visited)
    else:
        #print("case4", node, neighbour, adj_m[node][neighbour], visited)
        visited = visit_adj(adj_m, adj_m[node][neighbour], 0, visited) 
        return visit_adj(adj_m, node, neighbour+1, visited)

def visit_adj2(adj_m:dict, node:int, neighbour:int, visited:list) -> list:
    if adj_m[node] == []:
        visited.append(node)
        return visited
    elif adj_m[node] == [] and node == len(adj_m.keys())-1:
        return visited 
    if node not in visited:
        visited.append(node)
    if adj_m[node][neighbour] in visited and adj_m[node][neighbour] == adj_m[node][-1]:
        return visited
    elif adj_m[node][neighbour] in visited :
        return visit_adj2(adj_m, node, neighbour+1, visited) 
    elif adj_m[node][neighbour] not in visited and adj_m[node][neighbour] == adj_m[node][-1]:
        return visit_adj2(adj_m, adj_m[node][neighbour], 0, visited)
    else:
        visited = visit_adj2(adj_m, adj_m[node][neighbour], 0, visited) 
        return visit_adj2(adj_m, node, neighbour+1, visited)


def create_path(adj_m: np.array, adj_m_d:dict):
    temp_v = []
    
    for i in range(len(adj_m_d.keys())):
        v = visit_adj2(adj_m_d, i, 0, [])  
        if len(v) == len(adj_m_d.keys()):
            break                 
        if len(v) > 1:
            if i == len(adj_m_d.keys())-1:
                if i-1 not in v:
                    adj_m_d[i].append(i-1)
                    adj_m_d[i-1].append(i)
                    adj_m[i,i-1] = 1
                    adj_m[i-1,i] = 1
                else:
                    if temp_v == []:
                        temp_v = v.copy()
                    elif len( set(temp_v).intersection(set(v)) ) == 0:
                        print("v =", v[0]," i =", i)
                        adj_m_d[v[0]].append(temp_v[0])
                        adj_m_d[temp_v[0]].append(v[0])
                        adj_m[v[0],temp_v[0]] = 1
                        adj_m[temp_v[0],v[0]] = 1     
                        temp_v = []                   
                    else:
                        continue
            else:
                if i+1 not in v:
                    adj_m_d[i].append(i+1)
                    adj_m_d[i+1].append(i)
                    adj_m[i,i+1] = 1
                    adj_m[i+1,i] = 1                   
                else:
                    if temp_v == []:
                        temp_v = v.copy()
                    elif len( set(temp_v).intersection(set(v)) ) == 0:
                        print("v =", v[0]," i =", i)
                        adj_m_d[v[0]].append(temp_v[0])
                        adj_m_d[temp_v[0]].append(v[0])
                        adj_m[v[0],temp_v[0]] = 1
                        adj_m[temp_v[0],v[0]] = 1     
                        temp_v = []                   
                    else:
                        continue
        else:
            if i == len(adj_m_d.keys())-1:
                adj_m_d[i].append(i-1)
                adj_m_d[i-1].append(i)
                adj_m[i,i-1] = 1
                adj_m[i-1,i] = 1
            else:
                adj_m_d[i].append(i+1)
                adj_m_d[i+1].append(i)
                adj_m[i,i+1] = 1
                adj_m[i+1,i] = 1

    return adj_m, adj_m_d

#################################################################
## import data
# path = os.getcwd()

# data1 = path + "\data\\airfoil_self_noise.dat"
# col1 = ['freq', 'angle', 'chord', 'velocity', 'thickness', 'sound']
# df1 = pd.read_table(data1, sep="\t", names=col1)

# # X = df1.values[:, 0::3] #freq and velocity
# X = df1.values[:, 0:2] 
# y = df1.values[:, 5]

# std_scaler = StandardScaler()
# X = std_scaler.fit_transform(X)
# all_data = np.c_[X,y]

#################################################################
## linear regression
# model = LinearRegression()
# model.fit(X, y)

# print("from linear regression", model.intercept_.round(decimals=3), model.coef_.round(decimals=3))

# col_table = ["model", "learning rate", "batch", "epoch", "intercept"]
# table = [["linear regression", 0, 0, 0, model.intercept_.round(decimals=3)]]
# for z in range(model.coef_.size):
#     table[0].append(model.coef_[z].round(decimals=3))
#     col_table.append(f"theta{z+1}")

#################################################################
## crete network
node = 5
prob = 0.1
network_matrix, network_matrix_dict = random_network(node, prob)

#network_matrix_dict = {0: [], 1: [], 2: [], 3: [6], 4: [], 5: [7], 6: [3], 7: [5], 8: [], 9: []}
#print(network_matrix)
print("start matrix", network_matrix_dict)

#visit_graph = visit_adj(network_matrix_dict, 0, 0, [False]*5)
#visit_graph = visit_adj2(network_matrix_dict, 0, 0, [])
#print("show connectivity 1", visit_graph)

new_matrix,new_matrix_dict = create_path(network_matrix, network_matrix_dict)
#print(new_matrix)
#print("new matrix", new_matrix_dict)

#visit_graph = visit_adj2(new_matrix_dict, 0, 0, [])
#print("show connectivity 2", visit_graph)

#print(network_matrix_dict,"\n",new_matrix_dict)

##########################################################
## sgd
# theta_is_zero = True
# visual = True
# visual2 = True
# seed_num = 99
# epoch = 10
# every_t = 1
# batch_size = 32
# learning_rate = [0.005, 0.01, 0.05, 0.1]

# nrows = all_data.shape[0]
# divided_n = floor(nrows/node)
# max_divided_n = ceil(nrows/node) 
# remain_d = nrows%node

# datasets = []
# start, stop = 0, divided_n
# # divide the entire dataset to n nodes
# for n in range(node):   
#     if remain_d > 0:
#         stop+=1
#         remain_d -= 1
#     # shuffle for sgd
#     seed(seed_num)
#     shuffle(all_data[ start : stop, : ])
#     datasets.append( all_data[ start : stop, : ] )
#     start, stop = stop, stop+divided_n

# old_theta = []
# errors = [] 

# for lr in learning_rate: 
#     ############################################ thetas for every node not one  
#     if theta_is_zero == True:
#         theta0,theta = 0, np.zeros(X.shape[1])
#     else:
#         theta0, theta = theta_init(seed_num)
        
#     old_th = []
#     old_th.append(theta)
#     error = []    
    
#     for t in range(epoch):
#         for d in range(max_divided_n):
#             #####
#             mean_grad0, mean_grad, ne, c = all_grad(node-1, d, theta0, theta,  datasets) 
#             mean_grad0 /= ne
#             mean_grad /= ne
#             c /= ne
#             #####

#             theta0 = theta0 - (lr * mean_grad0)
#             theta = theta - (lr * mean_grad)
            
#             if d%batch_size==0 :
#                 old_th.append(theta) 
        
#         if t%every_t==0:
#             error.append(c/(max_divided_n-1))

#     print("learning rate=", lr, theta0.round(decimals=3), theta.round(decimals=3))
#     temp_table = [f"distributed sgd, node ={node}", lr, 0, epoch, theta0[0]]
#     for z in theta.flatten():
#         temp_table.append(z.round(decimals=3))
#     table.append(temp_table)

#     old_theta.append(old_th)  
#     errors.append(error)

# visualisation
## gradient
# if visual == True:
#     for lr in range(len(learning_rate)):
#         all_w = np.array(old_theta[lr])
#         if all_w.shape[1] > 2:
#             break
#         contour(model.coef_.flatten(), all_w, learning_rate[lr])   

## error
# if visual2 == True:
#     for lr in range(len(learning_rate)):
#         all_e = np.array(errors[lr])
#         converge(all_e, len(errors[lr]), learning_rate[lr])

##########################################################
## csv
# data2 = path + "\csv\\cla_distributed_sgd.csv"
# df999 = pd.DataFrame(table, columns=col_table)
# df999.to_csv(data2, index=False)