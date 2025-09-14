from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List

# Импортируем обновленные модели и логику
from data_processor import get_full_client_data, get_all_clients
from logic_engine import rank_top_products # Новое имя функции
from notification_generator import generate_push_notification
from models import (
    ClientDashboardData, RecommendationRequest, RecommendationResponse, 
    ClientInfo, RecommendationItem
)

app = FastAPI(title="InsightEngine API", version="1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"], # Добавим порт 3001 на всякий случай
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/clients", response_model=List[ClientInfo])
def get_clients_list():
    return get_all_clients()

@app.get("/api/clients/{client_code}", response_model=ClientDashboardData)
def get_client_data(client_code: int):
    full_data = get_full_client_data(client_code)
    if full_data:
        dashboard_data = {**full_data['profile'], **full_data['metrics']}
        return dashboard_data
    raise HTTPException(status_code=404, detail=f"Client with code {client_code} not found")

@app.post("/api/recommend", response_model=RecommendationResponse)
def get_recommendations(request: RecommendationRequest):
    full_data = get_full_client_data(request.client_code)
    if not full_data:
        raise HTTPException(status_code=404, detail=f"Client with code {request.client_code} not found")

    # 1. Получаем ранжированный список топ-4 продуктов
    top_products = rank_top_products(full_data)
    
    # 2. Создаем список для хранения готовых рекомендаций
    recommendations_list = []
    
    # 3. В цикле генерируем уведомление для КАЖДОГО продукта из топ-4
    for product_name, benefit in top_products:
        push_text = generate_push_notification(product_name, full_data, benefit)
        recommendations_list.append(
            RecommendationItem(product=product_name, push_notification=push_text)
        )
        
    # 4. Собираем финальный ответ в соответствии с новой моделью
    return RecommendationResponse(recommendations=recommendations_list)