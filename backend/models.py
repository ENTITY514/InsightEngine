from pydantic import BaseModel
from typing import List, Literal, Dict

class ClientDetailsResponse(BaseModel):
    monthly_transactions: Dict[str, Dict[str, float]]
    monthly_transfers: Dict[str, Dict[str, float]]

class RecommendationItem(BaseModel):
    product: str
    push_notification: str

class RecommendationResponse(BaseModel):
    recommendations: List[RecommendationItem]

class ClientInfo(BaseModel):
    client_code: int
    name: str

class TopCategory(BaseModel):
    category: str
    amount: float

class ClientDashboardData(BaseModel):
    client_code: int
    name: str
    status: Literal['Студент', 'Зарплатный клиент', 'Премиальный клиент', 'Стандартный клиент']
    age: int
    city: str
    avg_monthly_balance_KZT: float
    total_spending_3m: float
    top_categories: List[TopCategory]

class RecommendationRequest(BaseModel):
    client_code: int