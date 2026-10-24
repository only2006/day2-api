import requests

r = requests.get("https://open.er-api.com/v6/latest/USD")
print(r.json()["rates"]["CNY"])