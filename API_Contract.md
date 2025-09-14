API Спецификация: InsightEngine v1.1
Базовый URL: http://127.0.0.1:8000/api

Этот документ описывает все доступные эндпоинты, их структуру и типы данных.

1. Получение списка всех клиентов
Эндпоинт для загрузки и отображения списка всех клиентов в интерфейсе.

Путь: GET /clients

Описание: Возвращает массив с краткой информацией по каждому клиенту.

Пример ответа (JSON)
JSON

[
  {
    "client_code": 1,
    "name": "Айгерим"
  },
  {
    "client_code": 2,
    "name": "Данияр"
  },
  {
    "client_code": 3,
    "name": "Сабина"
  }
]
Интерфейс (TypeScript)
TypeScript

export interface ClientInfo {
  client_code: number;
  name: string;
}

// Тип для всего ответа
export type ClientListResponse = ClientInfo[];


2. Получение детальных данных по клиенту
Эндпоинт для загрузки аналитической панели (Dashboard) по конкретному, выбранному клиенту.

Путь: GET /clients/{client_code}

Описание: Возвращает подробный JSON-объект с профилем клиента и его ключевыми метриками. {client_code} в пути нужно заменить на ID клиента (например, /clients/1).

Пример ответа (JSON)
JSON

{
  "client_code": 1,
  "name": "Айгерим",
  "status": "Зарплатный клиент",
  "age": 29,
  "city": "Алматы",
  "avg_monthly_balance_KZT": 92643.0,
  "total_spending_3m": 2626914.27,
  "top_categories": [
    {
      "category": "Продукты питания",
      "amount": 645267.06
    },
    {
      "category": "Кафе и рестораны",
      "amount": 518757.59
    },
    {
      "category": "Путешествия",
      "amount": 275433.72
    }
  ]
}
Интерфейс (TypeScript)
TypeScript

export interface TopCategory {
  category: string;
  amount: number;
}

export interface ClientDashboardData {
  client_code: number;
  name: string;
  status: 'Студент' | 'Зарплатный клиент' | 'Премиальный клиент' | 'Стандартный клиент';
  age: number;
  city: string;
  avg_monthly_balance_KZT: number;
  total_spending_3m: number;
  top_categories: TopCategory[];
}
3. Получение продуктовой рекомендации
Основной эндпоинт для запуска аналитики и получения персонализированного предложения.

Путь: POST /recommend

Описание: Принимает ID клиента в теле запроса и возвращает лучший продукт с готовым текстом push-уведомления.

Пример запроса (JSON)
JSON

{
  "client_code": 1
}
Интерфейс запроса (TypeScript)
TypeScript

export interface RecommendationRequest {
  client_code: number;
}
Пример ответа (JSON)
JSON

{
  "product": "Кредитная карта",
  "push_notification": "Айгерим, ваши топ-категории — Продукты питания, Кафе и рестораны и Путешествия. Кредитная карта даёт до 10% кешбэка в любимых категориях. С ней вы бы дополнительно получили 143 945 ₸. Оформить карту."
}
Интерфейс ответа (TypeScript)
TypeScript

export interface RecommendationResponse {
  product: string;
  push_notification: string;
}