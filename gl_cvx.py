import cvxpy as cp
import numpy as np
import utils
from utils import logger, loggerName

def solver_cvx(x0, A, b, mu, solver, opts={}):
    outs = {}
    m, n = A.shape
    l = b.shape[1]
    X = cp.Variable((n, l))
    X.value = x0
    objective = cp.Minimize(0.5 * cp.square(cp.norm(A @ X - b, 'fro')) + mu * cp.sum(cp.norm(X, 2, 1)))
    prob = cp.Problem(objective)
    logger.info(f"Solver: {solver}")
    prob.solve(solver=solver, verbose=True)
    with open('./logs/gl_cvx.log', encoding='utf-8') as f:
        outs['output'] = f.read()
    iters = utils.parse_iters(outs['output'], solver)
    logger.info(f"iters: {iters}")
    logger.info(f"Time: {prob.solver_stats.solve_time}")
    logger.info(f"Objective: {prob.value}")
    logger.info(f"output:\n {outs['output']}")
    logger.info(f"CVXPY status: %s" % prob.status)
    logger.info(f"Solver stats: %s" % prob.solver_stats)
    return prob.value, X.value, len(iters), {'iters': iters}

solvers = {'cvx(%s)' % solver: lambda *args, solver=solver: solver_cvx(*args, solver)
            # for solver in ['GUROBI', 'MOSEK', 'CVXOPT']}
            # for solver in ['GUROBI']}
            for solver in ['GUROBI', 'MOSEK']}
            # for solver in ['MOSEK']}
            # for solver in ['CVXOPT']}

def solver_cvx_gurobi(x0, A, b, mu, opts):
    return solver_cvx(x0, A, b, mu, 'GUROBI', opts)

def solver_cvx_mosek(x0, A, b, mu, opts):
    return solver_cvx(x0, A, b, mu, 'MOSEK', opts)
