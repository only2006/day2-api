from pydantic import BaseModel, Field, ValidationError


class ExchangeRate(BaseModel):
    base_code: str
    rates: dict[str, float]
    time_last_update_utc: str
    provider: str = Field(default="unknown")


raw = {
    "base_code": "USD",
    "rates": {"CNY": 7.12, "JPY": 149.3},
    "time_last_update_utc": "Thu, 23 Oct 2026 00:00:01 +0000",
}

data = ExchangeRate.model_validate(raw)
print(data.base_code)      # USD
print(data.rates["CNY"])   # 7.12
print(data.provider)       # unknown（用了默认值）

# 故意给错的数据
bad = {"base_code": "USD", "rates": "不是字典", "time_last_update_utc": "x"}
try:
    ExchangeRate.model_validate(bad)
except ValidationError as exc:
    print("数据不合格：", exc)