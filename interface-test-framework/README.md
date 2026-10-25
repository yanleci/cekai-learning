# 接口自动化测试框架（pytest + requests + Allure）

基于 **pytest + requests + Allure** 的接口自动化测试框架，被测对象为自研的酒店预订 Mock API（Flask）。支持数据驱动、fixture 依赖注入、会话级登录态管理、分层断言、日志埋点、Allure 可视化报告。

**亮点**：在自研被测系统中复现缺陷（登录状态码语义错误、订单详情字段缺失），自动化用例成功抓出 3 条失败并定位根因，修复后回归全绿。

## 技术栈

| 技术 | 用途 |
|---|---|
| Python + requests | HTTP 请求与响应处理 |
| pytest | 测试框架（参数化 / fixture / 断言） |
| allure-pytest + Allure CLI | 测试报告生成与可视化 |
| logging | 框架日志（控制台 + 文件双通道） |
| Flask | 自研被测系统（Mock API） |

## 目录结构

```
interface-test-framework/
├── pytest.ini          # pytest 配置（--alluredir 等）
├── conftest.py         # 全局 fixture：client / auth_token / prepare_bookings
├── api/
│   └── client.py       # HttpClient 封装（日志埋点、Session 复用）
├── testcases/
│   ├── test_auth.py    # 登录模块用例（等价类 + 边界值）
│   └── test_booking.py # 订单模块用例（列表 / 详情）
├── data/
│   ├── login_cases.json    # 登录测试数据（数据与代码分离）
│   └── booking_cases.json  # 订单测试数据
├── utils/
│   └── assert_util.py  # 断言库（状态码 / 字段 / 值，失败输出人话）
├── logs/               # 运行日志（不入库）
├── allure-results/     # Allure 原始数据（不入库）
└── allure-report/      # Allure HTML 报告（不入库）
```

## 快速开始

### 1. 启动被测系统（Mock API）

```bash
cd mock-api
python app.py        # 默认账号 admin/password123，端口 8000
```

### 2. 安装依赖并运行测试

```bash
pip install -r requirements.txt        # pytest、requests、allure-pytest
pytest -s --alluredir allure-results    # 运行全部用例并生成原始数据
```

### 3. 生成并打开 Allure 报告

```bash
allure generate allure-results -o allure-report --clean
allure open allure-report
```

## 测试设计要点

- **数据驱动**：测试数据存 JSON，加用例 0 改代码
- **会话级 fixture**：整批测试只登录 1 次，共享 token；yield 后置自动清理数据
- **分层断言**：先验状态码 → 再验业务字段，杜绝"假绿"
- **缺陷发现**：用例成功抓出被测系统的 2 类缺陷（401 误返 400、详情缺 firstname），修复后回归全绿

## 当前状态

12 条用例全部通过（登录 8 条 + 订单 4 条），Allure 报告 100% 绿。
