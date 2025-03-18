# AutoTask Python框架

这是一个用于规范化自动化任务执行和结果反馈的Python框架。

## 安装

```bash
# 从Git仓库安装
pip install git+https://github.com/mykana/automation-task.git#subdirectory=autotask

# 或者从本地安装
pip install -e .
```

## 使用方法

### 基本用法

```python
from autotask import task, step, TaskResult, StepResult

@task("登录测试")
def main(result):
    # 任务代码
    return result

if __name__ == "__main__":
    import sys
    sys.exit(main())
```

### 添加步骤

```python
from autotask import task, step, TaskResult, StepResult

@task("登录测试")
def main(result):
    # 任务代码
    return result

@step("打开登录页面")
def open_login_page(result, step_result):
    # 步骤代码
    return result

@step("输入用户名密码")
def input_credentials(result, step_result):
    # 步骤代码
    if success:
        step_result.success("成功输入用户名密码")
    else:
        step_result.failure("输入用户名密码失败")
    return result

@step("点击登录按钮")
def click_login(result, step_result):
    # 步骤代码
    try:
        # 执行操作
        step_result.success("成功点击登录按钮")
    except Exception as e:
        step_result.error("点击登录按钮异常", exception=e)
    return result

@task("登录测试")
def main(result):
    result = open_login_page(result)
    result = input_credentials(result)
    result = click_login(result)
    
    if all_success:
        result.success("登录测试成功")
    else:
        result.failure("登录测试失败")
    
    return result

if __name__ == "__main__":
    import sys
    sys.exit(main())
```

### 输出结果

任务执行完成后，会自动将结果以JSON格式输出到标准输出，例如：

```json
{
  "task_name": "登录测试",
  "status": "success",
  "message": "任务执行成功",
  "start_time": "2023-05-20T10:15:30.123456",
  "end_time": "2023-05-20T10:15:35.654321",
  "duration": 5.530865,
  "steps": [
    {
      "name": "打开登录页面",
      "status": "success",
      "message": "成功打开登录页面",
      "start_time": "2023-05-20T10:15:30.234567",
      "end_time": "2023-05-20T10:15:31.345678",
      "duration": 1.111111,
      "data": {}
    },
    {
      "name": "输入用户名密码",
      "status": "success",
      "message": "成功输入用户名密码",
      "start_time": "2023-05-20T10:15:31.456789",
      "end_time": "2023-05-20T10:15:32.567890",
      "duration": 1.111101,
      "data": {}
    },
    {
      "name": "点击登录按钮",
      "status": "success",
      "message": "成功点击登录按钮",
      "start_time": "2023-05-20T10:15:32.678901",
      "end_time": "2023-05-20T10:15:33.789012",
      "duration": 1.110111,
      "data": {}
    }
  ],
  "data": {}
}
```

## 任务命名规范

为了与自动化任务执行系统集成，请按照以下规范命名Python脚本文件：

1. 脚本文件应放在`scripts`目录下
2. 文件名应使用`taskN.py`格式，其中N是任务编号，例如`task1.py`、`task2.py`等
3. 如果需要按模块组织任务，可以创建子目录，例如`scripts/login/task1.py`

## 示例

### 简单任务示例

```python
# scripts/task1.py
from autotask import task, step

@step("步骤1")
def step1(result, step_result):
    # 步骤代码
    step_result.success("步骤1成功")
    return result

@step("步骤2")
def step2(result, step_result):
    # 步骤代码
    step_result.success("步骤2成功")
    return result

@task("示例任务1")
def main(result):
    result = step1(result)
    result = step2(result)
    result.success("任务执行成功")
    return result

if __name__ == "__main__":
    import sys
    sys.exit(main())
```

### 模块化任务示例

```python
# scripts/login/task1.py
from autotask import task, step

@step("打开登录页面")
def open_login_page(result, step_result):
    # 步骤代码
    step_result.success("成功打开登录页面")
    return result

@step("输入用户名密码")
def input_credentials(result, step_result):
    # 步骤代码
    step_result.success("成功输入用户名密码")
    return result

@step("点击登录按钮")
def click_login(result, step_result):
    # 步骤代码
    step_result.success("成功点击登录按钮")
    return result

@task("登录测试")
def main(result):
    result = open_login_page(result)
    result = input_credentials(result)
    result = click_login(result)
    result.success("登录测试成功")
    return result

if __name__ == "__main__":
    import sys
    sys.exit(main())
``` 


任务ID/名称 -> Git仓库脚本路径的映射规则：
- 模块名/task{任务ID}.py
例如：
- login-task1 -> login/task1.py
- user-task2 -> user/task2.py


### 命名规范
scripts/
  ├── login/
  │   ├── task1.py  -> login-task1
  │   └── task2.py  -> login-task2
  ├── user/
  │   ├── task1.py  -> user-task1
  │   └── task2.py  -> user-task2
