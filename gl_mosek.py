import mosek
import numpy as np
from mosek.fusion import *
import sys
import utils
from utils import logger

def solver_mosek(x0, A, b, mu, opts={}):
    print('Note: for mosek, x0 is ignored')
    m, n = A.shape
    l = b.shape[1]
    # 模型名称为grouplasso
    with Model('grouplasso') as M:
        M.setLogHandler(sys.stdout)
        A = Matrix.dense(A)
        b = Matrix.dense(b)
        X = M.variable([n, l], Domain.unbounded())
        # X.setLevel(x0.ravel())
        Y = M.variable([m, l], Domain.unbounded())
        t1 = M.variable(1)
        ts = M.variable(n, Domain.greaterThan(0.0))
        M.constraint(Expr.sub(Expr.sub(Expr.mul(A, X), b), Y), Domain.equalsTo(0.0))
        M.constraint(Expr.vstack([Expr.add(1, t1), Expr.mul(2, Y.reshape(m * l)), Expr.sub(1, t1)]),
                    Domain.inQCone())
        for i in range(n):
            M.constraint(Expr.vstack([ts.index(i), X.slice([i, 0], [i + 1, l]).reshape(l)]), Domain.inQCone())
        obj = Expr.add(Expr.mul(0.5, t1), Expr.mul(mu, Expr.sum(ts)))
        M.objective('obj', ObjectiveSense.Minimize, obj)
        M.solve()
        outs = {}
        with open(r'./logs/gl_cvx.log', encoding='utf-8') as f:
            outs['output'] = f.read()
        iters = utils.parse_iters(outs['output'], 'MOSEK_OLD')
        logger.info(f"output: {outs['output']}")
        logger.info(f"iters: {iters}")
        return M.primalObjValue(), X.level().reshape([n, l]), len(iters), {'iters': iters}

solvers = {'mosek_SOCP': solver_mosek}
