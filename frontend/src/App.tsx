import React, { useState, useEffect } from 'react';
import { ChevronRight, Users, TrendingUp, CreditCard, Loader2, Sparkles, BarChart3, Wallet } from 'lucide-react';

// Types
interface Client {
  client_code: number;
  name: string;
}

interface TopCategory {
  category: string;
  amount: number;
}

interface ClientDashboardData {
  client_code: number;
  name: string;
  status: string;
  age: number;
  city: string;
  avg_monthly_balance_KZT: number;
  total_spending_3m: number;
  top_categories: TopCategory[];
}

interface RecommendationResponse {
  product: string;
  push_notification: string;
}

// API functions
// const API_BASE = 'http://127.0.0.1:8000/api';

const fetchClients = async (): Promise<Client[]> => {
  // Mock data - replace with actual API call
  return [
    { client_code: 1, name: 'Айгерим' },
    { client_code: 2, name: 'Данияр' },
    { client_code: 3, name: 'Асель' },
    { client_code: 4, name: 'Арман' },
    { client_code: 5, name: 'Молдир' }
  ];
};

const fetchClientData = async (clientCode: number): Promise<ClientDashboardData> => {
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

const generateRecommendation = async (clientCode: number): Promise<RecommendationResponse> => {
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

// ClientSelector Component
const ClientSelector: React.FC<{
  clients: Client[];
  selectedClientCode: number | null;
  onClientSelect: (clientCode: number) => void;
  loading: boolean;
}> = ({ clients, selectedClientCode, onClientSelect, loading }) => {
  if (loading) {
    return (
      <div className="bg-gray-800/50 backdrop-blur-xl rounded-2xl border border-gray-700/50 h-full p-6">
        <h2 className="text-xl font-semibold text-white mb-6 flex items-center">
          <div className="w-10 h-10 rounded-xl bg-blue-600 flex items-center justify-center mr-3">
            <Users className="h-5 w-5 text-white" />
          </div>
          Клиенты
        </h2>
        <div className="space-y-3">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="h-16 bg-gray-700/50 rounded-xl animate-pulse"></div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="bg-gray-800/50 backdrop-blur-xl rounded-2xl border border-gray-700/50 h-full p-6">
      <h2 className="text-xl font-semibold text-white mb-6 flex items-center">
        <div className="w-10 h-10 rounded-xl bg-blue-600 flex items-center justify-center mr-3">
          <Users className="h-5 w-5 text-white" />
        </div>
        Клиенты
      </h2>
      <div className="space-y-3 max-h-96 overflow-y-auto custom-scrollbar">
        {clients.map((client) => (
          <button
            key={client.client_code}
            onClick={() => onClientSelect(client.client_code)}
            className={`w-full p-4 text-left rounded-xl transition-all duration-300 flex items-center justify-between group relative overflow-hidden ${
              selectedClientCode === client.client_code
                ? 'bg-blue-500/20 border-2 border-blue-400/50 text-white shadow-lg shadow-blue-500/25'
                : 'bg-gray-700/30 hover:bg-gray-600/40 border-2 border-transparent text-gray-300 hover:text-white hover:shadow-md'
            }`}
          >
            <div className="flex items-center">
              <div className={`w-10 h-10 rounded-lg mr-3 flex items-center justify-center font-semibold ${
                selectedClientCode === client.client_code
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-600 text-gray-300 group-hover:bg-gray-500'
              }`}>
                {client.name[0]}
              </div>
              <span className="font-medium">{client.name}</span>
            </div>
            <ChevronRight className={`h-5 w-5 transition-all duration-300 ${
              selectedClientCode === client.client_code 
                ? 'rotate-90 text-blue-400' 
                : 'group-hover:translate-x-1 group-hover:text-white'
            }`} />
            {selectedClientCode === client.client_code && (
              <div className="absolute inset-0 bg-blue-500/10 rounded-xl"></div>
            )}
          </button>
        ))}
      </div>
    </div>
  );
};

// ClientDashboard Component
const ClientDashboard: React.FC<{
  selectedClientCode: number | null;
  clientData: ClientDashboardData | null;
  loading: boolean;
}> = ({ selectedClientCode, clientData, loading }) => {
  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('kk-KZ', {
      style: 'currency',
      currency: 'KZT',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount).replace('KZT', '₸');
  };

  if (!selectedClientCode) {
    return (
      <div className="bg-gray-800/50 backdrop-blur-xl rounded-2xl border border-gray-700/50 h-full p-8 flex items-center justify-center relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-blue-500/5 via-blue-500/5 to-blue-500/5"></div>
        <div className="text-center text-gray-400 relative z-10">
          <div className="w-20 h-20 mx-auto mb-6 bg-gradient-to-r from-gray-700 to-gray-600 rounded-2xl flex items-center justify-center">
            <TrendingUp className="h-10 w-10 text-gray-400" />
          </div>
          <h3 className="text-2xl font-semibold mb-3 text-gray-200">Выберите клиента для анализа</h3>
          <p className="text-gray-500 max-w-md">Выберите клиента из списка слева для просмотра детальной аналитики и персонализированных данных</p>
        </div>
      </div>
    );
  }

  if (loading || !clientData) {
    return (
      <div className="bg-gray-800/50 backdrop-blur-xl rounded-2xl border border-gray-700/50 h-full p-8">
        <div className="animate-pulse">
          <div className="h-10 bg-gray-700/50 rounded-xl mb-8 w-2/3"></div>
          
          <div className="grid grid-cols-3 gap-6 mb-8">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="p-6 bg-gray-700/30 rounded-xl">
                <div className="h-4 bg-gray-600/50 rounded mb-3 w-3/4"></div>
                <div className="h-8 bg-gray-600/50 rounded w-1/2"></div>
              </div>
            ))}
          </div>

          <div className="h-8 bg-gray-700/50 rounded-xl mb-6 w-1/3"></div>
          <div className="space-y-4">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="flex justify-between items-center p-4 bg-gray-700/30 rounded-xl">
                <div className="h-5 bg-gray-600/50 rounded w-1/3"></div>
                <div className="h-5 bg-gray-600/50 rounded w-1/4"></div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-gray-800/50 backdrop-blur-xl rounded-2xl border border-gray-700/50 h-full p-8 relative overflow-hidden">
      <div className="absolute top-0 right-0 w-64 h-64 bg-gradient-to-br from-blue-500/10 to-blue-600/10 rounded-full blur-3xl -translate-y-32 translate-x-32"></div>
      
      <div className="relative z-10">
        <div className="flex items-center mb-8">
          <div className="w-12 h-12 rounded-xl bg-blue-600 flex items-center justify-center mr-4">
            <span className="text-white font-bold text-lg">{clientData.name[0]}</span>
          </div>
          <div>
            <h2 className="text-3xl font-bold text-white mb-1">
              {clientData.name}
            </h2>
            <p className="text-gray-400">{clientData.city} • {clientData.age} лет</p>
          </div>
        </div>

        {/* Key Metrics */}
        <div className="mb-8">
          <h3 className="text-lg font-semibold text-gray-200 mb-6 flex items-center">
            <BarChart3 className="mr-2 h-5 w-5 text-blue-400" />
            Ключевые показатели
          </h3>
          <div className="grid grid-cols-3 gap-6">
            <div className="p-6 bg-gradient-to-br from-blue-500/20 to-blue-600/10 rounded-xl border border-blue-500/30 backdrop-blur-sm relative overflow-hidden">
              <div className="absolute top-0 right-0 w-20 h-20 bg-blue-500/20 rounded-full -translate-y-10 translate-x-10"></div>
              <div className="relative z-10">
                <p className="text-sm text-blue-300 font-medium mb-2">Статус</p>
                <p className="text-xl font-bold text-white">{clientData.status}</p>
              </div>
            </div>
            <div className="p-6 bg-gradient-to-br from-blue-500/20 to-blue-600/10 rounded-xl border border-blue-500/30 backdrop-blur-sm relative overflow-hidden">
              <div className="absolute top-0 right-0 w-20 h-20 bg-blue-500/20 rounded-full -translate-y-10 translate-x-10"></div>
              <div className="relative z-10">
                <p className="text-sm text-blue-300 font-medium mb-2">Средний остаток</p>
                <p className="text-xl font-bold text-white">{formatCurrency(clientData.avg_monthly_balance_KZT)}</p>
              </div>
            </div>
            <div className="p-6 bg-gradient-to-br from-blue-500/20 to-blue-600/10 rounded-xl border border-blue-500/30 backdrop-blur-sm relative overflow-hidden">
              <div className="absolute top-0 right-0 w-20 h-20 bg-blue-500/20 rounded-full -translate-y-10 translate-x-10"></div>
              <div className="relative z-10">
                <p className="text-sm text-blue-300 font-medium mb-2">Общие траты (3 мес)</p>
                <p className="text-xl font-bold text-white">{formatCurrency(clientData.total_spending_3m)}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Top Categories */}
        <div>
          <h3 className="text-lg font-semibold text-gray-200 mb-6 flex items-center">
            <Wallet className="mr-2 h-5 w-5 text-blue-400" />
            Топ-3 категории трат
          </h3>
          <div className="space-y-4">
            {clientData.top_categories.map((category, index) => (
              <div key={index} className="flex justify-between items-center p-5 bg-gray-700/30 rounded-xl border border-gray-600/50 backdrop-blur-sm hover:bg-gray-600/40 transition-all duration-300 group relative overflow-hidden">
                <div className="absolute left-0 top-0 bottom-0 w-1 bg-blue-500"></div>
                <div className="flex items-center">
                  <div className="w-3 h-3 rounded-full bg-blue-500 mr-4"></div>
                  <span className="font-medium text-gray-200 group-hover:text-white transition-colors">{category.category}</span>
                </div>
                <span className="font-bold text-white text-lg">{formatCurrency(category.amount)}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

// RecommendationPanel Component
const RecommendationPanel: React.FC<{
  selectedClientCode: number | null;
  onGenerateRecommendation: () => void;
  recommendation: RecommendationResponse | null;
  loading: boolean;
}> = ({ selectedClientCode, onGenerateRecommendation, recommendation, loading }) => {
  return (
    <div className="bg-gray-800/50 backdrop-blur-xl rounded-2xl border border-gray-700/50 h-full p-6 relative overflow-hidden">
      <div className="absolute top-0 left-0 w-32 h-32 bg-gradient-to-br from-blue-500/10 to-blue-600/10 rounded-full blur-2xl -translate-y-16 -translate-x-16"></div>
      
      <div className="relative z-10">
        <h2 className="text-xl font-semibold text-white mb-8 flex items-center">
          <div className="w-10 h-10 rounded-xl bg-blue-600 flex items-center justify-center mr-3">
            <Sparkles className="h-5 w-5 text-white" />
          </div>
          AI Рекомендации
        </h2>

        <button
          onClick={onGenerateRecommendation}
          disabled={!selectedClientCode || loading}
          className={`w-full py-5 px-6 rounded-xl font-semibold text-lg transition-all duration-300 mb-8 relative overflow-hidden group ${
            !selectedClientCode || loading
              ? 'bg-gray-700/50 text-gray-500 cursor-not-allowed border border-gray-600/50'
              : 'bg-blue-600 hover:bg-blue-700 text-white shadow-lg shadow-blue-500/25 hover:shadow-blue-500/40 transform hover:scale-105 border border-blue-500/50'
          }`}
        >
          {!selectedClientCode || loading ? null : (
            <div className="absolute inset-0 bg-gradient-to-r from-white/0 via-white/20 to-white/0 transform -skew-x-12 -translate-x-full group-hover:translate-x-full transition-transform duration-1000"></div>
          )}
          <div className="relative z-10 flex items-center justify-center">
            {loading ? (
              <>
                <Loader2 className="animate-spin mr-3 h-5 w-5" />
                Анализируем данные...
              </>
            ) : (
              <>
                <Sparkles className="mr-3 h-5 w-5" />
                Сгенерировать рекомендацию
              </>
            )}
          </div>
        </button>

        <div className="bg-gray-900/50 rounded-xl p-6 h-80 backdrop-blur-sm border border-gray-700/50">
          {loading ? (
            <div className="flex items-center justify-center h-full">
              <div className="text-center">
                <div className="w-16 h-16 mx-auto mb-4 bg-blue-600 rounded-2xl flex items-center justify-center">
                  <Loader2 className="animate-spin h-8 w-8 text-white" />
                </div>
                <p className="text-gray-300 font-medium">Анализируем поведение клиента</p>
                <p className="text-gray-500 text-sm mt-1">Генерируем персонализированную рекомендацию...</p>
              </div>
            </div>
          ) : recommendation ? (
            <div className="max-w-sm mx-auto">
              {/* Phone mockup */}
              <div className="bg-gradient-to-br from-gray-800 to-gray-900 rounded-3xl p-2 shadow-2xl border border-gray-600/50">
                <div className="bg-black rounded-2xl p-1">
                  <div className="bg-gradient-to-br from-blue-500 via-blue-600 to-blue-700 rounded-xl p-6 text-white shadow-xl relative overflow-hidden">
                    <div className="absolute top-0 right-0 w-24 h-24 bg-white/10 rounded-full -translate-y-12 translate-x-12"></div>
                    <div className="absolute bottom-0 left-0 w-16 h-16 bg-white/10 rounded-full translate-y-8 -translate-x-8"></div>
                    
                    <div className="relative z-10">
                      <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center space-x-2">
                          <div className="w-8 h-8 bg-white/20 rounded-full backdrop-blur-sm flex items-center justify-center">
                            <CreditCard className="h-4 w-4" />
                          </div>
                          <span className="text-sm font-medium opacity-90">Bank App</span>
                        </div>
                        <span className="text-xs opacity-75 bg-white/20 px-2 py-1 rounded-full">сейчас</span>
                      </div>
                      
                      <div className="flex items-center mb-3">
                        <Sparkles className="h-5 w-5 mr-2 text-yellow-300" />
                        <h4 className="font-bold text-lg">{recommendation.product}</h4>
                      </div>
                      
                      <p className="text-sm leading-relaxed opacity-90 mb-4">{recommendation.push_notification}</p>
                      
                      <div className="flex space-x-2">
                        <button className="flex-1 bg-white/20 backdrop-blur-sm rounded-lg py-2 px-4 text-sm font-medium hover:bg-white/30 transition-colors">
                          Подробнее
                        </button>
                        <button className="px-4 py-2 bg-white/10 rounded-lg">
                          ❌
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="flex items-center justify-center h-full text-center text-gray-500">
              <div>
                <div className="w-16 h-16 mx-auto mb-4 bg-gray-700/50 rounded-2xl flex items-center justify-center">
                  <CreditCard className="h-8 w-8 text-gray-600" />
                </div>
                <p className="text-gray-400 font-medium">Готов к генерации</p>
                <p className="text-gray-600 text-sm mt-1">Выберите клиента и нажмите кнопку выше</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

// Main App Component
const App: React.FC = () => {
  const [clients, setClients] = useState<Client[]>([]);
  const [selectedClientCode, setSelectedClientCode] = useState<number | null>(null);
  const [clientData, setClientData] = useState<ClientDashboardData | null>(null);
  const [recommendation, setRecommendation] = useState<RecommendationResponse | null>(null);
  const [loadingClients, setLoadingClients] = useState(true);
  const [loadingClientData, setLoadingClientData] = useState(false);
  const [loadingRecommendation, setLoadingRecommendation] = useState(false);

  // Load clients on mount
  useEffect(() => {
    const loadClients = async () => {
      try {
        const clientsData = await fetchClients();
        setClients(clientsData);
      } catch (error) {
        console.error('Error loading clients:', error);
      } finally {
        setLoadingClients(false);
      }
    };

    loadClients();
  }, []);

  // Load client data when selected client changes
  useEffect(() => {
    if (selectedClientCode) {
      setLoadingClientData(true);
      setClientData(null);
      setRecommendation(null);

      const loadClientData = async () => {
        try {
          const data = await fetchClientData(selectedClientCode);
          setClientData(data);
        } catch (error) {
          console.error('Error loading client data:', error);
        } finally {
          setLoadingClientData(false);
        }
      };

      loadClientData();
    } else {
      setClientData(null);
      setRecommendation(null);
    }
  }, [selectedClientCode]);

  const handleGenerateRecommendation = async () => {
    if (!selectedClientCode) return;

    setLoadingRecommendation(true);
    try {
      const recommendationData = await generateRecommendation(selectedClientCode);
      setRecommendation(recommendationData);
    } catch (error) {
      console.error('Error generating recommendation:', error);
    } finally {
      setLoadingRecommendation(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 relative overflow-hidden">
      {/* Background Effects */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(120,119,198,0.1),transparent_50%)]"></div>
      <div className="absolute top-0 left-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl"></div>
      <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl"></div>
      
      <div className="relative z-10 min-h-screen p-6">
        <div className="max-w-7xl mx-auto">
          <header className="mb-10">
            <div className="flex items-center mb-4">
              <div className="w-12 h-12 bg-blue-600 rounded-xl flex items-center justify-center mr-4">
                <Sparkles className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-4xl font-bold bg-gradient-to-r from-white via-gray-100 to-gray-300 bg-clip-text text-transparent">
                  InsightEngine
                </h1>
                <p className="text-gray-400 mt-1">Система аналитики и персонализированных рекомендаций</p>
              </div>
            </div>
          </header>

          <div className="grid grid-cols-12 gap-6 h-[calc(100vh-200px)]">
            {/* Client Selector - Left Column */}
            <div className="col-span-3">
              <ClientSelector
                clients={clients}
                selectedClientCode={selectedClientCode}
                onClientSelect={setSelectedClientCode}
                loading={loadingClients}
              />
            </div>

            {/* Client Dashboard - Center Column */}
            <div className="col-span-6">
              <ClientDashboard
                selectedClientCode={selectedClientCode}
                clientData={clientData}
                loading={loadingClientData}
              />
            </div>

            {/* Recommendation Panel - Right Column */}
            <div className="col-span-3">
              <RecommendationPanel
                selectedClientCode={selectedClientCode}
                onGenerateRecommendation={handleGenerateRecommendation}
                recommendation={recommendation}
                loading={loadingRecommendation}
              />
            </div>
          </div>
        </div>
      </div>

    </div>
  );
};

export default App;