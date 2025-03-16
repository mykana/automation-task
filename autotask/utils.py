"""
工具函数模块
提供常用的工具函数
"""

import os
import sys
import time
import json
import logging
from typing import Dict, Any, Optional, List, Union

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger('autotask')


def setup_logging(log_file: Optional[str] = None, level: int = logging.INFO):
    """
    设置日志
    
    Args:
        log_file: 日志文件路径，如果为None则只输出到控制台
        level: 日志级别
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # 清除现有的处理器
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # 添加控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    root_logger.addHandler(console_handler)
    
    # 如果指定了日志文件，添加文件处理器
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        root_logger.addHandler(file_handler)


def save_json(data: Dict[str, Any], file_path: str, ensure_dir: bool = True):
    """
    保存数据为JSON文件
    
    Args:
        data: 要保存的数据
        file_path: 文件路径
        ensure_dir: 是否确保目录存在
    """
    if ensure_dir:
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_json(file_path: str, default: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    从JSON文件加载数据
    
    Args:
        file_path: 文件路径
        default: 如果文件不存在或加载失败，返回的默认值
        
    Returns:
        加载的数据
    """
    if not os.path.exists(file_path):
        return default if default is not None else {}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"加载JSON文件失败: {file_path}, 错误: {str(e)}")
        return default if default is not None else {}


def retry(times: int = 3, delay: float = 1.0, exceptions: Union[List[Exception], Exception] = Exception):
    """
    重试装饰器
    
    Args:
        times: 重试次数
        delay: 重试延迟（秒）
        exceptions: 捕获的异常类型
        
    Returns:
        装饰器函数
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < times:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempt += 1
                    if attempt >= times:
                        raise
                    logger.warning(f"函数 {func.__name__} 执行失败，将在 {delay} 秒后重试 ({attempt}/{times}): {str(e)}")
                    time.sleep(delay)
        return wrapper
    return decorator 