# utils/assert_util.py
"""断言库：断言失败时输出"人话"，方便定位问题"""

def assert_status(actual, expected, msg=""):
    """断言状态码相等"""
    assert actual == expected, f"{msg or '状态码断言'}失败：期望 {expected}，实际 {actual}"

def assert_contains(container, key, msg=""):
    """断言 key 存在于 container（dict 键 / list 元素）"""
    assert key in container, f"{msg or '字段断言'}失败：在 {container} 里找不到 {key!r}"

def assert_equal(actual, expected, msg=""):
    """断言两个值相等"""
    assert actual == expected, f"{msg or '值断言'}失败：期望 {expected}，实际 {actual}"