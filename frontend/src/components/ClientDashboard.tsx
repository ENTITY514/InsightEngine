import React from 'react';
import { TrendingUp, BarChart3, Wallet } from 'lucide-react';

import { ClientDashboardData } from '../types/types';

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
          <div className="h-16 bg-gray-700/50 rounded-xl mb-10 w-2/3"></div>
          
          <div className="h-8 bg-gray-700/50 rounded-xl mb-6 w-2/4"></div>
          <div className="grid grid-cols-3 gap-6 mb-8">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="p-8 bg-gray-700/30 rounded-xl">
                <div className="h-4 bg-gray-600/50 rounded mb-3 w-3/4"></div>
                <div className="h-8 bg-gray-600/50 rounded w-1/2"></div>
              </div>
            ))}
          </div>

          <div className="h-8 bg-gray-700/50 rounded-xl mb-6 w-2/4"></div>
          <div className="space-y-4">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="flex justify-between items-center p-6 bg-gray-700/30 rounded-xl">
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

export default ClientDashboard;