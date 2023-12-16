import gurobipy as gp
import numpy as np
import time
import os
import utils
from utils import logger

def solver_gurobi(x0, A, b, mu, opts={}):
    m, n = A.shape
    l = b.shape[1]
    # print('Note: for gurobi, x0 is ignored')
    # t1 = time.time_ns()
    model = gp.Model()
    # t2 = time.time_ns()
    X = model.addMVar((n, l), lb=-gp.GRB.INFINITY)
    X.start = x0
    Y = model.addMVar((m, l), lb=-gp.GRB.INFINITY)
    ts = model.addMVar(n)
    # t3 = time.time_ns()
    for j in range(l):
        model.addConstr(A @ X[:, j] - b[:, j] == Y[:, j])
    # t4 = time.time_ns()
    for i in range(n):
        # model.addConstr(X[i, :] @ X[i, :] <= ts[i] @ ts[i])
        model.addConstr(X[i, :] @ X[i, :] <= ts[i] * ts[i])
    # t5 = time.time_ns()
    # print(t2 - t1, t3 - t2, t4 - t3, t5 - t4)
    model.setObjective(0.5 * sum([Y[:, j] @ Y[:, j] for j in range(l)]) + mu * sum(ts), gp.GRB.MINIMIZE)
    model.optimize()
    outs = {}
    with open(r'./logs/gl_cvx.log', encoding='utf-8') as f:
        outs['output'] = f.read()
    logger.info(f"output: {outs['output']}")
    iters = utils.parse_iters(outs['output'], 'GUROBI')
    logger.info(f"iters: {iters}")
    return model.objVal, X.x, len(iters), {'iters': iters}

solvers = {'gurobi_SOCP': solver_gurobi}
