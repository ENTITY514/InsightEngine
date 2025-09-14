API Contract: InsightEngine v1.0
Этот документ описывает API для проекта InsightEngine. Backend-сервер предоставляет две основные точки входа (эндпоинта) для взаимодействия с Frontend-приложением.

Базовый URL: http://127.0.0.1:8000/api

1. Получение данных о клиенте
Этот эндпоинт предоставляет агрегированную информацию о конкретном клиенте для отображения на панели управления.

URL: /clients/{client_code}

Метод: GET

Параметры URL:

client_code (integer, required): Уникальный идентификатор клиента.

Успешный ответ (Код 200 OK)
Возвращает JSON-объект со структурированной информацией о клиенте.

Структура ответа (ClientDashboardData):

JSON

{
  "client_code": 1,
  "name": "Айгерим",
  "status": "Зарплатный клиент",
  "age": 28,
  "city": "Алматы",
  "avg_monthly_balance_KZT": 250000.00,
  "total_spending_3m": 750000.00,
  "top_categories": [
    {
      "category": "Такси",
      "amount": 85000.00
    },
    {
      "category": "Кафе и рестораны",
      "amount": 65000.00
    },
    {
      "category": "Продукты питания",
      "amount": 50000.00
    }
  ]
}
Ответ при ошибке (Код 404 Not Found)
Возвращается, если клиент с указанным client_code не найден.

JSON

{
  "detail": "Client with code 999 not found"
}
2. Генерация продуктовой рекомендации
Основной эндпоинт, который запускает логику анализа и генерирует персонализированное предложение для клиента.

URL: /recommend

Метод: POST

Заголовки:

Content-Type: application/json

Тело запроса (RecommendationRequest)
JSON-объект, содержащий идентификатор клиента.

JSON

{
  "client_code": 1
}
Успешный ответ (Код 200 OK)
Возвращает JSON-объект с названием рекомендованного продукта и сгенерированным текстом push-уведомления.

Структура ответа (RecommendationResponse):

JSON

{
  "product": "Карта для путешествий",
  "push_notification": "Айгерим, в августе вы сделали 15 поездок на такси на 85 000 ₸. С картой для путешествий вернули бы ≈3 400 ₸. Откройте карту в приложении. 🚀"
}
Ответ при ошибке (Код 404 Not Found)
Возвращается, если клиент с указанным client_code не найден.

JSON

{
  "detail": "Client with code 999 not found"
}
Ответ при ошибке (Код 422 Unprocessable Entity)
Возвращается, если тело запроса некорректно (например, client_code не является числом).

JSON

{
  "detail": [
    {
      "loc": [
        "body",
        "client_code"
      ],
      "msg": "value is not a valid integer",
      "type": "type_error.integer"
    }
  ]
}