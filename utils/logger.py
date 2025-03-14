"""
todo:
@User: lenovo
@Date: 2025-03-14
@Time: 4:17
May the father of the gods give me power!
"""
import logging
import os
from datetime import datetime


def setup_logger(name):
    """配置日志记录器"""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # 文件处理器
    log_file = os.path.join(
        log_dir,
        f'test_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    )
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)

    # 格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger