# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 10:22:03 2022

@author: grace_elizabeth
"""

from gurobipy import *

try:
    
    # Parameters
    f = [
        [0, 10, 15, 20, 0],
        [10, 0, 30, 35, 10],
        [15, 30, 0, 10, 20],
        [20, 35, 10, 0, 15],
        [0, 10, 20, 15, 0]
        ]
    l = [25, 25, 35, 30, 35]
    b = [20, 20, 30, 20, 20]
    dh = 0
    dv = 0
    c = 1
    M = 999
    
    # Indices
    n = len(f)
    
    # Create model
    m = Model("Example 11.4")
    
    # Decision variables
    x = m.addVars(n, lb = 0, vtype = GRB.CONTINUOUS, name = "X")
    y = m.addVars(n, lb = 0, vtype = GRB.CONTINUOUS, name = "Y")
    xp = m.addVars(n, n, lb = 0, vtype = GRB.CONTINUOUS, name = "XP")
    yp = m.addVars(n, n, lb = 0, vtype = GRB.CONTINUOUS, name = "YP")
    xn = m.addVars(n, n, lb = 0, vtype = GRB.CONTINUOUS, name = "XN")
    yn = m.addVars(n, n, lb = 0, vtype = GRB.CONTINUOUS, name = "YN")
    z = m.addVars(n, n, vtype = GRB.BINARY, name = "Z")

    # Objective fuction
    m.setObjective(quicksum(c * f[i][j] * (xp[i,j] + xn[i,j] + yp[i,j] + yn[i,j]) for i in range(n-1) for j in range(i+1, n)), GRB.MINIMIZE)
    
    # Write constraints
    for i in range(n-1):
        for j in range(i+1, n):
            m.addConstr(x[i] - x[j] == xp[i,j] - xn[i,j], name = "Absolute value")
            m.addConstr(y[i] - y[j] == yp[i,j] - yn[i,j], name = "Absolute value")
            m.addConstr(x[i] - x[j] + M * z[i,j] >= 1/2*(l[i] + l[j]) + dh, name = "Constraint 11.23")
            m.addConstr(y[i] - y[j] + M *(1 - z[i,j]) >= 1/2*(b[i] + b[j]) + dv, name = "Constraint 11.24")
    
    
    # Call Gurobi Optimizer
    m.optimize()
    if m.status == GRB.OPTIMAL:
       for v in m.getVars():
           if v.x > 0:
               print('%s = %g' % (v.varName, v.x)) 
       print('Obj = %f' % m.objVal)
    elif m.status == GRB.INFEASIBLE:
       print('LP is infeasible.')
    elif m.status == GRB.UNBOUNDED:
       print('LP is unbounded.')
except GurobiError:
    print('Error reported')