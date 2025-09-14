import React from 'react';
import { Loader2, Sparkles, CreditCard } from 'lucide-react';

import { RecommendationResponse } from '../types/types';

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

export default RecommendationPanel;