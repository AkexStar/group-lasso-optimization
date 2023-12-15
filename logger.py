import logging
import os
import time
# 使用一个名字为ATC-CDG的logger
logger = logging.getLogger('LASSO')

# 设置logger的level为INFO
logger.setLevel(logging.INFO)

# 创建一个输出日志到控制台的StreamHandler
hdr = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s: %(message)s')
hdr.setFormatter(formatter)

# 给logger添加上handler
logger.addHandler(hdr)

# 同时写入日志文件
current_work_dir = os.path.dirname(__file__)
if not os.path.exists(current_work_dir+'/logs'):
    os.makedirs(current_work_dir+'/logs')
now = time.strftime("%m%d-%H%M%S",time.localtime(time.time()))
logging.basicConfig(filename = current_work_dir+f'/logs/LASSO-{now}.log',
                    level = logging.INFO,
                    encoding='utf-8',
                    format = '[%(asctime)s] %(filename)s: %(funcName)s: %(levelname)s: %(message)s')
logger.info(f"日志文件保存在{current_work_dir}\logs\LASSO-{now}.log")

def setLevel(level: str):
    """设置日志级别
    Args:
        - _level (str): 日志级别，可选值为DEBUG, INFO, WARNING, ERROR, CRITICAL，默认为INFO
    """
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('输入不正确的日志级别: %s' % level)
    logger.setLevel(numeric_level)
    logger.info(f"日志级别设置为{level.upper()}")