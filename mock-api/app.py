"""
酒店预订 Mock API（本地被测系统）
功能：登录拿 token + 预订的增删改查（CRUD）

启动：python app.py
访问：http://127.0.0.1:8000

默认账号：admin / password123
"""
import uuid
from flask import Flask, request, jsonify

app = Flask(__name__)

# ===== 用两个字典模拟"数据库"（重启即清空，天然适合测试） =====
USERS = {"admin": "password123", "user": "123456"}   # 用户名 -> 密码
BOOKINGS = {}                      # 预订id -> 预订数据
VALID_TOKENS = set()               # 已发放的登录token


# ---------- 1. 登录：POST /auth ----------
# 规则（对学生设计的用例）：
#   - 密码要求 6-12 位，不满足返回 400"密码长度需在6-12位"
#   - 用户名不存在/密码错误，统一返回 401"用户名或密码错误"（不泄露用户是否存在）
#   - 用户名或密码为空，返回 400
@app.post("/auth")
def login():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")

    # 空值校验（等价类-空值）
    if not username or not password:
        return jsonify({"reason": "用户名或密码不能为空"}), 400

    # 密码长度边界（等价类-无效 + 边界值：5/13 离点）
    if not (6 <= len(password) <= 12):
        return jsonify({"reason": "密码长度需在6-12位"}), 400

    # 用户不存在 / 密码错误 -> 统一提示（安全：不泄露用户是否存在）
    if USERS.get(username) != password:
        return jsonify({"reason": "用户名或密码错误"}), 400

    token = str(uuid.uuid4())      # 生成一个随机的 token
    VALID_TOKENS.add(token)
    return jsonify({"token": token})


# ---------- 2. 创建预订：POST /booking ----------
@app.post("/booking")
def create_booking():
    data = request.get_json()
    bid = max(BOOKINGS.keys(), default=0) + 1
    BOOKINGS[bid] = data
    return jsonify({"bookingid": bid, "booking": data})


# ---------- 3. 查询预订列表：GET /booking ----------
@app.get("/booking")
def list_bookings():
    firstname = request.args.get("firstname")
    if firstname:
        ids = [bid for bid, b in BOOKINGS.items() if b.get("firstname") == firstname]
    else:
        ids = list(BOOKINGS.keys())
    return jsonify([{"bookingid": bid} for bid in ids])


# ---------- 4. 查询预订详情：GET /booking/<id> ----------
@app.get("/booking/<int:bid>")
def get_booking(bid):
    data = BOOKINGS.get(bid)
    if data is None:
        return jsonify({"error": "预订不存在"}), 404
    data.pop("firstname")
    return jsonify(data)


# ---------- 5. 更新预订：PUT /booking/<id>（需要登录） ----------
@app.put("/booking/<int:bid>")
def update_booking(bid):
    if not _check_token():
        return jsonify({"error": "未登录"}), 403
    data = BOOKINGS.get(bid)
    if data is None:
        return jsonify({"error": "预订不存在"}), 404
    BOOKINGS[bid] = request.get_json()
    return jsonify(BOOKINGS[bid])


# ---------- 6. 删除预订：DELETE /booking/<id>（需要登录） ----------
@app.delete("/booking/<int:bid>")
def delete_booking(bid):
    if not _check_token():
        return jsonify({"error": "未登录"}), 403
    if bid not in BOOKINGS:
        return jsonify({"error": "预订不存在"}), 404
    del BOOKINGS[bid]
    return jsonify({"message": "已删除"})


def _check_token():
    """检查请求头里有没有合法的 token"""
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    return token in VALID_TOKENS


if __name__ == "__main__":
    # debug=True 代码改动会自动重载，不用手动重启
    app.run(host="127.0.0.1", port=8000, debug=True)
