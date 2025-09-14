from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import ClientDashboardData, RecommendationRequest, RecommendationResponse

# Создание экземпляра приложения
app = FastAPI(
    title="InsightEngine API",
    version="1.0"
)

# Настройка CORS для Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Адрес вашего React-приложения
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===================================================================
# API Эндпоинты
# ===================================================================

@app.get("/api/clients/{client_code}", response_model=ClientDashboardData)
def get_client_data(client_code: int):
    # ЗАГЛУШКА: Здесь будет логика получения данных из data_processor.py
    # Пока что возвращаем фейковые данные для проверки работы
    if client_code == 1:
        return {
            "client_code": 1,
            "name": "Айгерим",
            "status": "Зарплатный клиент",
            "age": 28,
            "city": "Алматы",
            "avg_monthly_balance_KZT": 250000.00,
            "total_spending_3m": 750000.00,
            "top_categories": [
                {"category": "Такси", "amount": 85000.00},
                {"category": "Кафе и рестораны", "amount": 65000.00},
                {"category": "Продукты питания", "amount": 50000.00}
            ]
        }
    raise HTTPException(status_code=404, detail=f"Client with code {client_code} not found")

@app.post("/api/recommend", response_model=RecommendationResponse)
def get_recommendation(request: RecommendationRequest):
    # ЗАГЛУШКА: Здесь будет вызов logic_engine и notification_generator
    if request.client_code == 1:
        return {
            "product": "Карта для путешествий",
            "push_notification": "Айгерим, в августе вы сделали 15 поездок на такси на 85 000 ₸. С картой для путешествий вернули бы ≈3 400 ₸. Откройте карту в приложении. 🚀"
        }
    raise HTTPException(status_code=404, detail=f"Client with code {request.client_code} not found")