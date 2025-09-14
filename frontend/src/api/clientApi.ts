import type { Client, ClientDashboardData, RecommendationResponse } from "../types/types"

// Mock API functions - replace with actual API calls
export const fetchClients = async (): Promise<Client[]> => {
  // Simulate API delay
  await new Promise((resolve) => setTimeout(resolve, 1000))

  return [
    { client_code: 1, name: "Алексей" },
    { client_code: 2, name: "Мария" },
    { client_code: 3, name: "Дмитрий" },
    { client_code: 4, name: "Елена" },
    { client_code: 5, name: "Андрей" },
    { client_code: 6, name: "Ольга" },
    { client_code: 7, name: "Сергей" },
    { client_code: 8, name: "Татьяна" },  
    { client_code: 9, name: "Игорь" },
    { client_code: 10, name: "Наталья" },
    { client_code: 11, name: "Виктор" },
  ]
}

export const fetchClientData = async (clientCode: number): Promise<ClientDashboardData> => {
  // Simulate API delay
  await new Promise((resolve) => setTimeout(resolve, 800))

  const mockData: Record<number, ClientDashboardData> = {
    1: {
      client_code: 1,
      name: "Алексей Иванов",
      status: "Студент",
      age: 35,
      city: "Алматы",
      avg_monthly_balance_KZT: 2500000,
      total_spending_3m: 1800000,
      top_categories: [
        { category: "Продукты питания", amount: 450000 },
        { category: "Транспорт", amount: 320000 },
        { category: "Развлечения", amount: 280000 },
      ],
    },
    2: {
      client_code: 2,
      name: "Мария Петрова",
      status: "Зарплатный клиент",
      age: 42,
      city: "Нур-Султан",
      avg_monthly_balance_KZT: 5200000,
      total_spending_3m: 3100000,
      top_categories: [
        { category: "Шоппинг", amount: 850000 },
        { category: "Рестораны", amount: 620000 },
        { category: "Путешествия", amount: 580000 },
      ],
    },
  }

  return mockData[clientCode] || mockData[1]
}

export const generateRecommendation = async (clientCode: number): Promise<RecommendationResponse> => {
  // Simulate API delay
  await new Promise((resolve) => setTimeout(resolve, 2000))

  const allRecommendations = [
    {
      product: "Премиум Карта",
      push_notification: "Получите 5% кэшбэк на все покупки и эксклюзивные привилегии с нашей Премиум картой!",
    },
    {
      product: "Инвестиционный Портфель",
      push_notification: "Увеличьте свои сбережения на 12% годовых с персональным инвестиционным портфелем",
    },
    {
      product: "Автокредит",
      push_notification: "Специальное предложение: автокредит под 8.5% годовых с быстрым одобрением за 30 минут",
    },
    {
      product: "Накопительная Карта",
      push_notification:
        "Вы потратили значительную сумму в прошлом месяце. С накопительной картой вы могли бы получить дополнительные бонусы! 💳",
    },
  ]

  return {
    recommendations: allRecommendations,
  }
}
