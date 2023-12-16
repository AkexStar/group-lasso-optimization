import numpy as np
import time
import utils
from utils import logger
from tabulate import tabulate
import matplotlib.pyplot as plt

plot_curve = True

def test_solver(solver, kw):
    from group_lasso_data import n, m, l, x0, A, b, mu, u
    tic = time.time_ns()
    [obj, x, it, out] = solver(x0.copy(), A, b, mu)
    toc = time.time_ns()
    time_elapsed = (toc - tic) * 10**(-9)
    err = np.linalg.norm(u - x) / np.linalg.norm(u)
    sparsity = np.sum(np.abs(x) > 1e-5) / x.size
    logger.info(f'Time: {time_elapsed}')
    logger.info(f'Objective: {obj}')
    logger.info(f'Error: {err}')
    logger.info(f'Sparsity: {sparsity}')
    if 'iters' in out and plot_curve:
        logger.info(f"iters: {out['iters']}")
        x, y = zip(*out['iters'])
        plt.plot(x, y, '*-', label=kw)
    return obj, err, time_elapsed, it, sparsity

if __name__ == '__main__':
    import sys
    import importlib
    solvers = {}
    tab = []
    with open('./logs/gl_cvx.log', "w", encoding='utf-8') as devlog, utils.RedirectStdStreams(stdout=devlog, stderr=devlog):
        for name in sys.argv[1:]:
            solvers = {**solvers, **importlib.import_module(name).solvers}
        for kw, solver in solvers.items():
            logger.info(f'Solver: {kw}')
            utils.cleanUpLog()
            obj, err, time_elapsed, it, sparsity = test_solver(solver, kw)
            tab.append([kw, obj, err, time_elapsed, it, sparsity])

    print(tabulate(tab, headers=['Solver', 'Objective', 'Error', 'Time(s)', 'Iter', 'Sparsity']))
    if plot_curve:
        plt.yscale('log')
        plt.legend()
        plt.show()
