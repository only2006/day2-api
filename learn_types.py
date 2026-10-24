from typing import Optional


def greet(name: str, times: int = 1) -> str:
    """重复问候指定次数。"""
    return (f"你好，{name}！" * times).strip()


def average(scores: list[float]) -> Optional[float]:
    """求平均分；列表为空时返回 None。"""
    if not scores:
        return None
    return sum(scores) / len(scores)


def find_user(user_id: int) -> dict[str, str] | None:
    """按 ID 查用户。"""
    users = {1: {"name": "小明", "city": "杭州"}}
    return users.get(user_id)


if __name__ == "__main__":
    print(greet("小明", 2))
    print(average([80.0, 92.5, 77.0]))
    print(average([]))
    print(find_user(1))