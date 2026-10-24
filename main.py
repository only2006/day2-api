"""汇率查询 CLI —— Day 2 工程化练习

用法:
    uv run main.py 100 USD CNY
"""

import logging
import sys

import httpx
from pydantic import BaseModel, ValidationError

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

API_URL = "https://open.er-api.com/v6/latest/{base}"


class ExchangeRate(BaseModel):
    base_code: str
    rates: dict[str, float]
    time_last_update_utc: str


def fetch_rates(base: str, timeout: float = 10.0) -> ExchangeRate:
    """从公开 API 拉取以 base 为基准的汇率。"""
    url = API_URL.format(base=base)
    logger.info("请求汇率数据：%s", url)

    try:
        response = httpx.get(url, timeout=timeout)
        response.raise_for_status()
        payload = response.json()
    except httpx.TimeoutException:
        logger.error("请求超时（%.1f 秒），请检查网络", timeout)
        raise
    except httpx.HTTPStatusError as exc:
        logger.error("接口返回错误状态码：%s", exc.response.status_code)
        raise
    except httpx.RequestError as exc:
        logger.error("网络连接失败：%s", exc)
        raise

    try:
        data = ExchangeRate.model_validate(payload)
    except ValidationError as exc:
        logger.error("返回数据格式异常：%s", exc)
        raise

    logger.info("数据校验通过，共 %d 种货币", len(data.rates))
    return data


def convert(amount: float, target: str, data: ExchangeRate) -> float:
    """按汇率把金额换算成目标货币。"""
    code = target.upper()
    if code not in data.rates:
        raise ValueError(f"不支持的货币代码：{code}")
    return amount * data.rates[code]


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        print("用法：uv run main.py <金额> <源货币> <目标货币>")
        print("例如：uv run main.py 100 USD CNY")
        return 1

    amount_text, source, target = argv[1], argv[2].upper(), argv[3].upper()

    try:
        amount = float(amount_text)
    except ValueError:
        logger.error("金额必须是数字，收到：%r", amount_text)
        return 2

    try:
        data = fetch_rates(source)
        result = convert(amount, target, data)
    except (httpx.HTTPError, ValidationError, ValueError) as exc:
        logger.error("查询失败：%s", exc)
        return 3

    logger.info("汇率更新时间：%s", data.time_last_update_utc)
    print()
    print(f"  {amount:,.2f} {source} = {result:,.2f} {target}")
    print(f"  汇率：1 {source} = {data.rates[target]:.4f} {target}")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))