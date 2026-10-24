import pytest   # type:ignore
import json
import allure # type:ignore

from utils.assert_util import assert_status, assert_contains


def load_login_cases():
    """从数据文件读取登录用例"""
    with open('data/login_cases.json', encoding='utf-8') as f:
        return json.load(f)


@allure.feature("登录模块")
@allure.story("正常登录")
@allure.title("正确账号密码返回 token")
@pytest.mark.parametrize('case', load_login_cases()["login_success"],
                         ids=lambda c: c["name"])
def test_login_success(client, case):
    payload = {'username': case["username"], 'password': case["password"]}
    allure.attach(
        json.dumps(payload, indent=2, ensure_ascii=False),  # 格式化JSON，并确保中文正常显示
        name="请求体 (Request Body)",
        attachment_type=allure.attachment_type.JSON
    )
    resp = client.post('/auth', json=payload)
    allure.attach(
        resp.text,  # 直接使用响应文本
        name="响应体 (Response Body)",
        attachment_type=allure.attachment_type.JSON  # 如果响应是JSON格式，用JSON类型渲染更友好
    )
    assert_status(resp.status_code, case["expected"], "登录成功")
    assert_contains(resp.json(), "token", "登录成功返回TOKEN" )

@allure.feature("登录模块")
@allure.story("异常登录")
@allure.title("错误账号密码登录")
@pytest.mark.parametrize('case', load_login_cases()["login_invalid"],
                         ids=lambda c: c["name"])
def test_login_invalid_credentials(client, case):
    payload = {'username': case["username"], 'password': case["password"]}
    allure.attach(
        json.dumps(payload, indent=2, ensure_ascii=False),  # 格式化JSON，并确保中文正常显示
        name="请求体 (Request Body)",
        attachment_type=allure.attachment_type.JSON
    )
    resp = client.post('/auth', json=payload)
    allure.attach(
        resp.text,  # 直接使用响应文本
        name="响应体 (Response Body)",
        attachment_type=allure.attachment_type.JSON  # 如果响应是JSON格式，用JSON类型渲染更友好
    )
    assert_status(resp.status_code, case["expected"], "异常登录")