export interface Client {
  client_code: number;
  name: string;
}

export interface TopCategory {
  category: string;
  amount: number;
}

export interface ClientDashboardData {
  client_code: number;
  name: string;
  status: string;
  age: number;
  city: string;
  avg_monthly_balance_KZT: number;
  total_spending_3m: number;
  top_categories: TopCategory[];
}

export interface RecommendationResponse {
  recommendations: {
    product: string
    push_notification: string
  }[]
}