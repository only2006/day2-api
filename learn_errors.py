import httpx


def parse_int(text: str) -> int:
    try:
        return int(text)
    except ValueError:
        print(f"「{text}」不是合法数字，返回默认值 0")
        return 0


def fetch(url: str) -> dict:
    try:
        response = httpx.get(url, timeout=5.0)
        response.raise_for_status()   # 4xx/5xx 时抛异常
        return response.json()
    except httpx.TimeoutException:
        print("请求超时")
        raise
    except httpx.HTTPStatusError as exc:
        print(f"服务器返回错误状态码：{exc.response.status_code}")
        raise
    except httpx.RequestError as exc:
        print(f"网络层错误：{exc}")
        raise


if __name__ == "__main__":
    print(parse_int("123"))
    print(parse_int("abc"))

    try:
        data = fetch("https://open.er-api.com/v6/latest/USD")
        print("拿到数据，字段有：", list(data.keys())[:5])
    except Exception:
        print("查询失败，但程序没有崩溃")