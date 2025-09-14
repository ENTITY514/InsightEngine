from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
# ВАЖНО: get_client_profile переименована в get_full_client_data
from data_processor import get_full_client_data 
# Импортируем наш "мозг"
from logic_engine import find_best_product
from models import ClientDashboardData, RecommendationRequest, RecommendationResponse

app = FastAPI(title="InsightEngine API", version="1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/clients/{client_code}", response_model=ClientDashboardData)
def get_client_data(client_code: int):
    full_data = get_full_client_data(client_code)
    if full_data:
        # Собираем ответ для дашборда из полных данных
        dashboard_data = {**full_data['profile'], **full_data['metrics']}
        return dashboard_data
    raise HTTPException(status_code=404, detail=f"Client with code {client_code} not found")

@app.post("/api/recommend", response_model=RecommendationResponse)
def get_recommendation(request: RecommendationRequest):
    full_data = get_full_client_data(request.client_code)
    if not full_data:
        raise HTTPException(status_code=404, detail=f"Client with code {request.client_code} not found")

    # Получаем лучший продукт от нашего движка
    best_product, benefit = find_best_product(request.client_code, full_data)
    
    # ЗАГЛУШКА для текста пуша (следующий шаг - notification_generator.py)
    push_text = f"Для вас есть выгодное предложение по продукту '{best_product}' с потенциальной выгодой {benefit} ₸. Подробности скоро."

    return {
        "product": best_product,
        "push_notification": push_text,
    }