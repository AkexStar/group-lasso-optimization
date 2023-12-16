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
    logger.info('Time:', time_elapsed)
    logger.info('Objective:', obj)
    logger.info('Error:', err)
    logger.info('Sparsity:', sparsity)
    if 'iters' in out and plot_curve:
        x, y = zip(*out['iters'])
        plt.plot(x, y, '*-', label=kw)
    return obj, err, time_elapsed, it, sparsity

if __name__ == '__main__':
    import sys
    import importlib
    solvers = {}
    with open('./logs/gl_cvx.txt', "w", encoding='utf-8') as devlog, utils.RedirectStdStreams(stdout=devlog, stderr=devlog):
        for name in sys.argv[1:]:
            solvers = {**solvers, **importlib.import_module(name).solvers}
        tab = []
        for kw, solver in solvers.items():
            logger.info(f'Solver: {kw}')
            tab.append([kw, *test_solver(solver, kw)])

        print(tabulate(tab, headers=['Solver', 'Objective', 'Error', 'Time(s)', 'Iter', 'Sparsity']))
        if plot_curve:
            plt.yscale('log')
            plt.legend()
            plt.show()
