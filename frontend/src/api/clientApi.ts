import { Client, ClientDashboardData, RecommendationResponse } from '../types/types';

// const API_BASE = 'http://127.0.0.1:8000/api';

export const fetchClients = async (): Promise<Client[]> => {
  // Mock data - replace with actual API call
  await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate loading
  return [
    { client_code: 1, name: 'Айгерим' },
    { client_code: 2, name: 'Данияр' },
    { client_code: 3, name: 'Асель' },
    { client_code: 4, name: 'Арман' },
    { client_code: 5, name: 'Молдир' },
    { client_code: 6, name: 'Молдир' },
    { client_code: 7, name: 'Молдир' },
    { client_code: 8, name: 'Молдир' },
    { client_code: 9, name: 'Молдир' },
    { client_code: 10, name: 'Молдир' },
    { client_code: 11, name: 'Молдир' },
    { client_code: 12, name: 'Молдир' },
    { client_code: 13, name: 'Иман' },
  ];
};

export const fetchClientData = async (clientCode: number): Promise<ClientDashboardData> => {
  // Mock data - replace with actual API call
  await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate loading
  
  if (clientCode === 1) {
    return {
      client_code: 1,
      name: 'Айгерим',
      status: 'Зарплатный клиент',
      age: 28,
      city: 'Алматы',
      avg_monthly_balance_KZT: 250000.00,
      total_spending_3m: 750000.00,
      top_categories: [
        { category: 'Такси', amount: 85000.00 },
        { category: 'Кафе и рестораны', amount: 65000.00 },
        { category: 'Продукты питания', amount: 50000.00 }
      ]
    };
  }
  
  // Mock data for other clients
  return {
    client_code: clientCode,
    name: clientCode === 2 ? 'Данияр' : clientCode === 3 ? 'Асель' : clientCode === 4 ? 'Арман' : 'Молдир',
    status: 'Обычный клиент',
    age: 25 + clientCode,
    city: 'Нур-Султан',
    avg_monthly_balance_KZT: 150000.00 + clientCode * 10000,
    total_spending_3m: 450000.00 + clientCode * 50000,
    top_categories: [
      { category: 'Продукты питания', amount: 45000.00 + clientCode * 5000 },
      { category: 'Транспорт', amount: 35000.00 + clientCode * 3000 },
      { category: 'Развлечения', amount: 25000.00 + clientCode * 2000 }
    ]
  };
};

export const generateRecommendation = async (clientCode: number): Promise<RecommendationResponse> => {
  // Mock data - replace with actual API call
  await new Promise(resolve => setTimeout(resolve, 2000)); // Simulate processing
  
  if (clientCode === 1) {
    return {
      product: 'Карта для путешествий',
      push_notification: 'Айгерим, в августе вы сделали 15 поездок на такси на 85 000 ₸. С картой для путешествий вернули бы ≈3 400 ₸. Откройте карту в приложении. 🚀'
    };
  }
  
  return {
    product: 'Накопительная карта',
    push_notification: `Вы потратили значительную сумму в прошлом месяце. С накопительной картой вы могли бы получить дополнительные бонусы! 💳`
  };
};