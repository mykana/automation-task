"""
结果类模块
定义任务执行结果的数据结构
"""

import enum
import json
import time
from datetime import datetime
from typing import List, Dict, Any, Optional


class Status(enum.Enum):
    """状态枚举"""
    SUCCESS = "success"
    FAILURE = "failure"
    ERROR = "error"
    SKIPPED = "skipped"


class StepResult:
    """步骤执行结果"""
    
    def __init__(self, name: str):
        self.name = name
        self.status = Status.SUCCESS
        self.message = ""
        self.start_time = datetime.now()
        self.end_time = None
        self.duration = 0
        self.data = {}
    
    def success(self, message: str = "", **data):
        """标记步骤成功"""
        self.status = Status.SUCCESS
        self.message = message
        self.data.update(data)
        self._complete()
        return self
    
    def failure(self, message: str, **data):
        """标记步骤失败"""
        self.status = Status.FAILURE
        self.message = message
        self.data.update(data)
        self._complete()
        return self
    
    def error(self, message: str, exception: Optional[Exception] = None, **data):
        """标记步骤错误"""
        self.status = Status.ERROR
        self.message = message
        if exception:
            self.data["exception"] = str(exception)
            self.data["exception_type"] = type(exception).__name__
        self.data.update(data)
        self._complete()
        return self
    
    def skip(self, message: str = "步骤已跳过", **data):
        """标记步骤跳过"""
        self.status = Status.SKIPPED
        self.message = message
        self.data.update(data)
        self._complete()
        return self
    
    def _complete(self):
        """完成步骤，计算执行时间"""
        self.end_time = datetime.now()
        self.duration = (self.end_time - self.start_time).total_seconds()
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "name": self.name,
            "status": self.status.value,
            "message": self.message,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration": self.duration,
            "data": self.data
        }


class TaskResult:
    """任务执行结果"""
    
    def __init__(self, task_name: str):
        self.task_name = task_name
        self.status = Status.SUCCESS
        self.message = ""
        self.start_time = datetime.now()
        self.end_time = None
        self.duration = 0
        self.steps: List[StepResult] = []
        self.data = {}
    
    def add_step(self, step_result: StepResult) -> 'TaskResult':
        """添加步骤结果"""
        self.steps.append(step_result)
        
        # 如果步骤失败或错误，任务也标记为失败或错误
        if step_result.status == Status.FAILURE:
            self.status = Status.FAILURE
        elif step_result.status == Status.ERROR and self.status != Status.FAILURE:
            self.status = Status.ERROR
            
        return self
    
    def success(self, message: str = "任务执行成功", **data):
        """标记任务成功"""
        if self.status == Status.SUCCESS:  # 只有当前状态为成功时才能设置为成功
            self.message = message
            self.data.update(data)
        self._complete()
        return self
    
    def failure(self, message: str, **data):
        """标记任务失败"""
        self.status = Status.FAILURE
        self.message = message
        self.data.update(data)
        self._complete()
        return self
    
    def error(self, message: str, exception: Optional[Exception] = None, **data):
        """标记任务错误"""
        if self.status != Status.FAILURE:  # 失败优先级高于错误
            self.status = Status.ERROR
        self.message = message
        if exception:
            self.data["exception"] = str(exception)
            self.data["exception_type"] = type(exception).__name__
        self.data.update(data)
        self._complete()
        return self
    
    def _complete(self):
        """完成任务，计算执行时间"""
        self.end_time = datetime.now()
        self.duration = (self.end_time - self.start_time).total_seconds()
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "task_name": self.task_name,
            "status": self.status.value,
            "message": self.message,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration": self.duration,
            "steps": [step.to_dict() for step in self.steps],
            "data": self.data
        }
    
    def to_json(self, pretty: bool = False) -> str:
        """转换为JSON字符串"""
        if pretty:
            return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
        return json.dumps(self.to_dict(), ensure_ascii=False)
    
    def print_result(self):
        """打印结果到标准输出"""
        print(self.to_json(pretty=True))
    
    def exit_code(self) -> int:
        """获取退出码"""
        if self.status == Status.SUCCESS:
            return 0
        elif self.status == Status.FAILURE:
            return 1
        elif self.status == Status.ERROR:
            return 2
        else:
            return 3 