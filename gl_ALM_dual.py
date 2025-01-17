import numpy as np
from utils import stopRange

MAX_ITER = 9999
th_converge = 1e-4
MAX_INNER_ITER = 100

def solver_ALM_dual(x0, A, b, mu, opts={}):
    m, n = A.shape
    l = b.shape[1]

    def primal_obj(X):
        return 0.5 * np.linalg.norm(A @ X - b, 'fro')**2 \
            + mu * np.sum(np.linalg.norm(X, axis=1))

    def dual_obj(z):
        return 0.5 * np.linalg.norm(z, 'fro')**2 \
            + np.sum(z * b)

    def project(v, mu):
        norm = np.linalg.norm(v, axis=1, keepdims=True)
        norm[norm < mu] = mu
        return v * (mu / norm)

    iters_primal = []
    iters_dual = []

    la = -x0
    
    t = opts.get('t', 10)   # assume constant here. need to enable EIG otherwise
    # dAAT, qAAT = np.linalg.eig(A @ A.T)
    inv = np.linalg.inv(np.eye(m) + t * A @ A.T)
    v = np.zeros((n, l))

    for it, report_outer_converge in stopRange(MAX_ITER, 3):
        for it2, report_inner_converge in stopRange(MAX_INNER_ITER, 3):
            z = inv @ (t * A @ v - A @ la - b)
            v0 = v
            v = project(A.T @ z + la / t, mu)
            inner_gap = np.linalg.norm(v - v0, 'fro')
            if report_inner_converge(inner_gap < th_converge):
                print(it, 'inner', it2)
        
        la = la + t * (A.T @ z - v)

        iters_primal.append((it, primal_obj(-la)))
        iters_dual.append((it, dual_obj(z)))

        dual_sat = np.linalg.norm(A.T @ z - v)
        report_outer_converge(dual_sat < th_converge)

    return iters_primal[-1][1], -la, len(iters_primal),\
        {'iters': iters_primal, 'iters_dual': iters_dual}

solvers = {'ALM_dual': solver_ALM_dual}

# If you want to test the effect of tuning hyperparameter t,
# Uncomment below and run >> python test.py gl_ALM_dual

# solvers = {'ALM_dual_t_%f' % t: lambda *a, t=t: solver_ALM_dual(*a, opts={'t': t})
#            for t in [0.5, 1, 5, 10, 50, 100, 200, 500, 1000]}
