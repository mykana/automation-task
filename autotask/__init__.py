"""
AutoTask - Python自动化任务执行框架
用于规范化自动化任务的执行和结果反馈
"""

from .decorators import task, step
from .result import TaskResult, StepResult, Status

__all__ = ['task', 'step', 'TaskResult', 'StepResult', 'Status'] 