import pytest  # type:ignore
import json
import allure  #type:ignore

from utils.assert_util import assert_status, assert_contains, assert_equal


def load_booking_cases():
    with open('data/booking_cases.json', encoding='utf-8') as f:
        return json.load(f)



@allure.feature("订单模块")
@allure.story("正常查询订单")
@allure.title("正确传参查询返回对应订单")
@pytest.mark.parametrize('case', load_booking_cases()["get_booking_list"],
                         ids=lambda c: c["name"])
def test_get_booking_list(client, prepare_bookings, case):
    param = case["params"]
    allure.attach(
        json.dumps(param, indent=2, ensure_ascii=False),  # 格式化JSON，并确保中文正常显示
        name="请求体 (Request Body)",
        attachment_type=allure.attachment_type.JSON
    )
    resp = client.get('/booking', params=param)
    allure.attach(
        resp.text,
        name="响应体 (Response Body)",
        attachment_type=allure.attachment_type.JSON
    )
    assert_status(resp.status_code, case["expected"], "订单列表")
    data = resp.json()
    for b in data: assert_contains(prepare_bookings, b["bookingid"], "订单ID在预置数据中")
    assert_equal(len(data), case["bookings_len"], "订单数量")

@allure.feature("订单模块")
@allure.story("查询订单详情")
@allure.title("查询返回对应订单详情")
@pytest.mark.parametrize('case', load_booking_cases()["get_booking_detail"],
                         ids=lambda c: c["name"])
def test_get_booking_detail(client, prepare_bookings, case):
    if case["id_source"] == "exist":
        bid = prepare_bookings[0]  # 拿真实存在的 ID
    else:
        bid = 99999  # 随便创造一个不存在的ID


    allure.attach(
        str(bid),
        name="请求体 (Request Body)",
        attachment_type=allure.attachment_type.TEXT
    )
    resp = client.get(f'/booking/{bid}')
    allure.attach(
        resp.text,
        name="响应体 (Response Body)",
        attachment_type=allure.attachment_type.JSON
    )
    assert_status(resp.status_code, case["expected_status"], "订单详情")

    # 正向用例：状态码 + 核心业务字段（firstname）
    # 反向用例：状态码 + 错误提示信息（error）
    data = resp.json()
    assert_contains(data, case["expected_key"], "订单详情字段")
