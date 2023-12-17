# Group-LASSO-problem 作业

## 软件环境版本

| **Name** | **Version** |
| :------------: | :---------------: |
|    Windows    |  11+.0(22631.2)  |
|     python     |      3.9.18      |
|      pip      |      23.3.1      |
|     cvxpy     |       1.4.1       |
|    gurobipy    |      11.0.0      |
|     Mosek     |      10.1.21      |
|   matplotlib   |       3.8.2       |
|     numpy     |      1.26.2      |
|    tabulate    |      0.9.0      |

本项目使用 `conda` 管理环境，使用 `conda create -n glp python=3.9` 创建环境，使用 `conda activate glp` 激活环境，使用 `conda deactivate` 退出环境。

项目可以使用 `conda` 或者 `pip` 安装依赖，但是 `mosek` 和 `gurobipy` 需要配置许可证书，具体方法参考官方文档[【Mosek installation】](https://docs.mosek.com/latest/install/installation.html)和[【gurobipy installation】](https://support.gurobi.com/hc/en-us/articles/360044290292)。

## 参考资料

- [[1] GitHub repo: group-lasso-optimization](https://github.com/gzz2000/group-lasso-optimization)
- [[2] 课程提供的 Matlab 代码样例](http://faculty.bicmr.pku.edu.cn/~wenzw/optbook/pages/contents/contents.html)
- [[3] CVXPY 说明文档](https://www.cvxpy.org/index.html)
- [[4] python logging 说明文档](https://docs.python.org/3/howto/logging-cookbook.html)
- [[5] CVXPY stdout 输出重定向方法](https://stackoverflow.com/questions/68863458/modifying-existing-logger-configuration-of-a-python-package)
- [[6] python 正则表达式说明文档](https://docs.python.org/3/library/re.html)
- [[7] matplotlib 说明文档](https://matplotlib.org/stable/contents.html)

## 项目致谢

- 感谢 @wenzw 老师提供的课程资料，本项目的部分函数实现参考了其内容。
- 感谢 @gzz2000 公开的代码样例，本项目部分函数的实现参考了其内容。
- 感谢 @zhangzhao2022 提供的支持，本项目的部分函数实现受到其帮助。
- 感谢 @cvxgrp 提供的 CVXPY 优化库，本项目使用了其提供的接口。


