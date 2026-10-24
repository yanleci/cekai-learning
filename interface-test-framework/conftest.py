# conftest.py（位置：项目根目录，和 pytest.ini 同级）
import pytest  # type: ignore
from api.client import HttpClient
import logging
import os

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                    )
os.makedirs("logs", exist_ok=True)
file_handler = logging.FileHandler(filename="logs/test.log", encoding="utf_8")
file_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s",))
logging.getLogger().addHandler(file_handler)

@pytest.fixture(scope="session")
def client():
    return HttpClient()


@pytest.fixture(scope="session")
def auth_token(client):
    # 1. 先登录获取 Token
    login_resp = client.post('/auth', json={"username": "admin", "password": "password123"})

    # 如果登录失败，就直接抛错（防止带着错误的 token 去删除，掩盖了真实问题）
    assert login_resp.status_code == 200, "登录失败，无法获取 token"
    return login_resp.json()["token"]


@pytest.fixture
def prepare_bookings(client, auth_token):
    booking1 = {"firstname": "Alice", "lastname": "Wang", "totalprice": 100}
    booking2 = {"firstname": "Bob", "lastname": "Li", "totalprice": 200}

    res1 = client.post('/booking', json=booking1)
    res2 = client.post('/booking', json=booking2)
    assert res1.status_code == 200 and res2.status_code == 200
    ids = [res1.json()["bookingid"], res2.json()["bookingid"]]

    yield ids  # ========= 这里是测试用例执行的分界线 =========

    #  构造带有 Token 的请求头
    headers = {"Authorization": f"Bearer {auth_token}"}

    #  循环删除，把 headers 传进去
    for bid in ids:
        del_resp = client.delete(f'/booking/{bid}', headers=headers)
        # 验证1：断言删除接口返回 200
        assert del_resp.status_code == 200, f"清理数据 ID={bid} 失败，删除接口返回：{del_resp.status_code}"

        # 验证2：真正去查一下这个 ID，断言接口返回 404 证明数据真的没了
        check_resp = client.get(f'/booking/{bid}')
        assert check_resp.status_code == 404, f"数据清理不干净！ID={bid} 依然能查到！"
