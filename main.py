import requests
from fastapi import FastAPI, HTTPException

app = FastAPI()

# Пример ключа с https://app.exchangerate-api.com/
EXCHANGE_API_KEY = "cfed6d5a738767d5d223da26"

# Внешний API для получения курсов валют
EXCHANGE_RATE_API_URL = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/latest/"


@app.get("/api/rates")
def get_exchange_rate(from_currency: str = "USD", to_currency: str = "RUB", value: float = 1.0):
    try:
        # Получаем данные о курсах валют из внешнего API
        response = requests.get(f"{EXCHANGE_RATE_API_URL}{from_currency}")
        response.raise_for_status()  # Проверка на успешный статус ответа
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching exchange rates: {e}")

    try:
        data = response.json()
    except ValueError:
        raise HTTPException(status_code=500, detail="Error parsing exchange rates response")

    if to_currency not in data["conversion_rates"]:
        raise HTTPException(status_code=400, detail="Invalid target currency")

    try:
        exchange_rate = data["conversion_rates"][to_currency]
        result = round(value * exchange_rate, 2)
    except KeyError:
        raise HTTPException(status_code=500, detail="Error processing exchange rates data")

    return {"result": result}
