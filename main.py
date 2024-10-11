from decimal import Decimal, ROUND_HALF_UP

import requests
from fastapi import FastAPI, HTTPException

app = FastAPI()

# Пример ключа с https://app.exchangerate-api.com/
EXCHANGE_API_KEY = "cfed6d5a738767d5d223da26"

# Внешний API для получения курсов валют
EXCHANGE_RATE_API_URL = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/latest/"


@app.get("/api/rates")
def get_exchange_rate(from_currency: str = "USD", to_currency: str = "RUB", value: float = 1.0) -> dict:
    """
    Получает текущий обменный курс и конвертирует сумму из одной валюты в другую.

    :param from_currency: (str) Исходная валюта. По умолчанию "USD".
    :param to_currency: (str) Целевая валюта. По умолчанию "RUB".
    :param value: (float) Сумма для конвертации. По умолчанию 1.0.
    :return: (dict) Результат конвертации с ключом "result" и значением, округленным до двух знаков после запятой.

    :raises HTTPException:
        - 400, если указана недопустимая целевая валюта.
        - 500, если произошла ошибка при получении данных o курсах валют или их обработке.
    """
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
        exchange_rate = Decimal(data["conversion_rates"][to_currency])
        value_dec = Decimal(value)
        result = (value_dec * exchange_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    except KeyError:
        raise HTTPException(status_code=500, detail="Error processing exchange rates data")

    return {"result": float(result)}
