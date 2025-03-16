#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
示例任务1 - 基本演示
"""

from autotask import task, step


@step("步骤1 - 初始化")
def step1(result, step_result):
    """初始化步骤"""
    print("执行步骤1 - 初始化")
    step_result.success("初始化成功", init_data={"key": "value"})
    return result


@step("步骤2 - 处理数据")
def step2(result, step_result):
    """处理数据步骤"""
    print("执行步骤2 - 处理数据")
    
    # 模拟数据处理
    data = {"processed": True, "count": 10}
    
    step_result.success("数据处理成功", processed_data=data)
    return result


@step("步骤3 - 输出结果")
def step3(result, step_result):
    """输出结果步骤"""
    print("执行步骤3 - 输出结果")
    
    # 模拟输出结果
    output = "处理完成，共处理10条数据"
    print(output)
    
    step_result.success("结果输出成功", output=output)
    return result


@task("示例任务1")
def main(result):
    """主任务函数"""
    print("开始执行示例任务1")
    
    # 执行步骤
    result = step1(result)
    result = step2(result)
    result = step3(result)
    
    # 设置任务结果
    result.success("示例任务1执行成功", total_steps=3)
    return result


if __name__ == "__main__":
    import sys
    sys.exit(main()) 