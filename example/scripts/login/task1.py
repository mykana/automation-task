#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
登录模块 - 任务1 - 登录测试
"""

from autotask import task, step


@step("打开登录页面")
def open_login_page(result, step_result):
    """打开登录页面步骤"""
    print("正在打开登录页面...")
    
    # 模拟打开登录页面
    login_url = "https://example.com/login"
    print(f"已打开登录页面: {login_url}")
    
    step_result.success("成功打开登录页面", url=login_url)
    return result


@step("输入用户名密码")
def input_credentials(result, step_result):
    """输入用户名密码步骤"""
    print("正在输入用户名密码...")
    
    # 模拟输入用户名密码
    username = "testuser"
    password = "********"  # 密码不应明文显示
    print(f"已输入用户名: {username}")
    
    step_result.success("成功输入用户名密码", username=username)
    return result


@step("点击登录按钮")
def click_login(result, step_result):
    """点击登录按钮步骤"""
    print("正在点击登录按钮...")
    
    # 模拟点击登录按钮
    print("已点击登录按钮")
    
    # 模拟登录成功
    login_success = True
    
    if login_success:
        step_result.success("成功点击登录按钮并登录成功")
    else:
        step_result.failure("登录失败，请检查用户名密码")
    
    return result


@step("验证登录状态")
def verify_login(result, step_result):
    """验证登录状态步骤"""
    print("正在验证登录状态...")
    
    # 模拟验证登录状态
    is_logged_in = True
    user_info = {
        "id": 12345,
        "username": "testuser",
        "email": "test@example.com",
        "role": "user"
    }
    
    if is_logged_in:
        print(f"登录验证成功，用户信息: {user_info}")
        step_result.success("登录状态验证成功", user_info=user_info)
    else:
        print("登录验证失败")
        step_result.failure("登录状态验证失败")
    
    return result


@task("登录测试")
def main(result):
    """主任务函数"""
    print("开始执行登录测试")
    
    # 执行步骤
    result = open_login_page(result)
    result = input_credentials(result)
    result = click_login(result)
    result = verify_login(result)
    
    # 设置任务结果
    if result.status == result.status.SUCCESS:
        result.success("登录测试成功完成")
    else:
        result.failure("登录测试失败")
    
    return result


if __name__ == "__main__":
    import sys
    sys.exit(main()) 