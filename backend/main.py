from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from data_processor import get_full_client_data, get_all_clients
from logic_engine import find_best_product
from notification_generator import generate_push_notification
from models import ClientDashboardData, RecommendationRequest, RecommendationResponse, ClientInfo
from typing import List

app = FastAPI(title="InsightEngine API", version="1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/clients", response_model=List[ClientInfo])
def get_clients_list():
    """
    Возвращает список всех клиентов.
    """
    return get_all_clients()

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

    best_product, benefit = find_best_product(request.client_code, full_data)
    
    # Генерируем финальный, персонализированный текст
    push_text = generate_push_notification(best_product, full_data, benefit)

    return {
        "product": best_product,
        "push_notification": push_text,
    }