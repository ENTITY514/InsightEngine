import type { Client, ClientDashboardData, RecommendationResponse } from "../types/types"
import axios from 'axios';

export const fetchClients = async (): Promise<Client[]> => {
  try {
    const response = await axios.get<Client[]>("http://localhost:8000/api/clients");
    return response.data;
  } catch (error) {
    console.error("Failed to fetch clients:", error);
    // Можно вернуть пустой массив или бросить ошибку, в зависимости от логики
    return [];
  }
};

export const fetchClientData = async (clientCode: number): Promise<ClientDashboardData> => {
  try {
    const response = await axios.get<ClientDashboardData>(`http://localhost:8000/api/clients/${clientCode}`);
    return response.data;
  } catch (error) {
    console.error("Failed to fetch client data:", error);
    // Возвращаем null или бросаем ошибку в зависимости от вашей логики
    throw error;
  }
};

export const generateRecommendation = async (clientCode: number): Promise<RecommendationResponse> => {
  try {
    const requestBody = { client_code: clientCode };
    const response = await axios.post<RecommendationResponse>("http://localhost:8000/api/recommend", requestBody);
    return response.data;
  } catch (error) {
    console.error("Failed to generate recommendations:", error);
    throw error;
  }
};