"""
装饰器模块
提供任务和步骤的装饰器
"""

import functools
import sys
import traceback
from typing import Callable, Any, Optional

from .result import TaskResult, StepResult


def task(name: Optional[str] = None) -> Callable:
    """
    任务装饰器
    用于装饰主任务函数，自动处理结果输出和异常
    
    用法:
    @task("登录任务")
    def main():
        # 任务代码
        return result
    
    或者:
    @task()  # 使用函数名作为任务名
    def login_task():
        # 任务代码
        return result
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> int:
            # 确定任务名称
            task_name = name or func.__name__
            
            # 创建任务结果对象
            result = TaskResult(task_name)
            
            try:
                # 执行任务函数
                func_result = func(result, *args, **kwargs)
                
                # 如果函数返回了结果对象，使用它
                if isinstance(func_result, TaskResult):
                    result = func_result
                
                # 标记任务完成
                if result.status == result.status.SUCCESS:
                    result.success()
            except Exception as e:
                # 捕获异常并记录
                tb = traceback.format_exc()
                result.error(f"任务执行异常: {str(e)}", exception=e, traceback=tb)
            
            # 打印结果
            result.print_result()
            
            # 返回退出码
            return result.exit_code()
        
        return wrapper
    
    # 处理不带参数的装饰器调用
    if callable(name):
        func, name = name, None
        return decorator(func)
    
    return decorator


def step(name: str) -> Callable:
    """
    步骤装饰器
    用于装饰任务中的步骤函数，自动处理结果记录和异常
    
    用法:
    @step("打开登录页面")
    def open_login_page(result):
        # 步骤代码
        return result
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(result: TaskResult, *args, **kwargs) -> TaskResult:
            # 创建步骤结果
            step_result = StepResult(name)
            
            try:
                # 执行步骤函数
                func_result = func(result, step_result, *args, **kwargs)
                
                # 如果函数返回了结果对象，使用它
                if isinstance(func_result, StepResult):
                    step_result = func_result
                elif isinstance(func_result, TaskResult):
                    result = func_result
                
                # 如果步骤没有明确设置状态，默认为成功
                if step_result.end_time is None:
                    step_result.success()
            except Exception as e:
                # 捕获异常并记录
                tb = traceback.format_exc()
                step_result.error(f"步骤执行异常: {str(e)}", exception=e, traceback=tb)
            
            # 将步骤结果添加到任务结果中
            result.add_step(step_result)
            
            return result
        
        return wrapper
    
    return decorator 