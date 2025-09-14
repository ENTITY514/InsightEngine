import type React from "react"
import { Loader2, Sparkles, CreditCard, MessageCircle, Mail } from "lucide-react"

import type { RecommendationResponse } from "../types/types"

const RecommendationPanel: React.FC<{
  selectedClientCode: number | null
  recommendation: RecommendationResponse | null
  loading: boolean
}> = ({ selectedClientCode, recommendation, loading }) => {
  return (
    <div className="bg-gray-800/50 backdrop-blur-xl rounded-2xl border border-gray-700/50 h-full p-4 relative overflow-hidden">
      <div className="absolute top-0 left-0 w-32 h-32 bg-gradient-to-br from-blue-500/10 to-blue-600/10 rounded-full blur-2xl -translate-y-16 -translate-x-16"></div>

      <div className="relative z-10 h-full flex flex-col">
        <h2 className="text-lg font-semibold text-white mb-4 flex items-center">
          <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center mr-2">
            <Sparkles className="h-4 w-4 text-white" />
          </div>
          AI Рекомендации
        </h2>

        {loading ? (
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <div className="w-12 h-12 mx-auto mb-3 bg-blue-600 rounded-xl flex items-center justify-center">
                <Loader2 className="animate-spin h-6 w-6 text-white" />
              </div>
              <p className="text-gray-300 font-medium text-sm">Анализируем поведение клиента</p>
              <p className="text-gray-500 text-xs mt-1">Генерируем персонализированную рекомендацию...</p>
            </div>
          </div>
        ) : recommendation ? (
          <div className="h-full flex items-center justify-center">
            <div className="w-full max-w-[350px] h-full flex items-center justify-center">
              {/* Phone Frame */}
              <div className="bg-gradient-to-br from-gray-900 to-black rounded-[2.5rem] p-2 shadow-2xl border border-gray-600/30 w-full max-w-[320px]">
                {/* Phone Screen */}
                <div className="bg-black rounded-[2rem] p-1">
                  <div className="bg-gradient-to-b from-gray-900 to-gray-800 rounded-[1.75rem] h-[550px] relative overflow-hidden">
                    {/* Status Bar */}
                    <div className="flex justify-between items-center px-6 py-3 text-white text-xs">
                      <span className="font-medium">9:41</span>
                      <div className="flex items-center space-x-1">
                        <div className="w-4 h-2 border border-white/60 rounded-sm">
                          <div className="w-3/4 h-full bg-white rounded-sm"></div>
                        </div>
                      </div>
                    </div>

                    {/* SMS Header */}
                    <div className="px-4 py-3 bg-gray-800/80 border-b border-gray-700/50">
                      <div className="flex items-center space-x-3">
                        
                          <img src="/BCC_logo.jpeg" alt="BCC Logo" className="h-8 w-8 object-contain rounded-full" />
                        
                        <div>
                          <p className="text-white font-medium text-sm">BCC Hub</p>
                          <p className="text-gray-400 text-xs">сейчас</p>
                        </div>
                      </div>
                    </div>

                    {/* SMS Messages */}
                    <div className="flex-1 overflow-y-auto p-5 space-y-4 max-h-[380px] custom-scrollbar">
                      {recommendation.recommendations.map((rec, index) => (
                        <div key={index} className="flex justify-start">
                          <div className="max-w-[200px] bg-gray-700/80 rounded-2xl rounded-bl-md px-4 py-3 backdrop-blur-sm">
                            <div className="flex items-center mb-2">
                              <Mail className="h-3 w-3 text-yellow-400 mr-2" />
                              <span className="text-blue-400 font-semibold text-xs">{rec.product}</span>
                            </div>
                            <p className="text-white text-xs leading-relaxed">{rec.push_notification}</p>
                            <div className="flex justify-between items-center mt-2 pt-2 border-t border-gray-600/50">
                              <span className="text-gray-400 text-xs">сейчас</span>
                              <MessageCircle className="h-3 w-3 text-gray-400" />
                            </div>
                          </div>
                        </div>
                      ))}

                      {/* Typing indicator */}
                      <div className="flex justify-start">
                        <div className="bg-gray-700/60 rounded-2xl rounded-bl-md px-4 py-2">
                          <div className="flex space-x-1">
                            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                            <div
                              className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                              style={{ animationDelay: "0.1s" }}
                            ></div>
                            <div
                              className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                              style={{ animationDelay: "0.2s" }}
                            ></div>
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Message Input */}
                    <div className="px-4 py-3 bg-gray-800/80 border-t border-gray-700/50">
                      <div className="flex items-center space-x-2">
                        <div className="flex-1 bg-gray-700/60 rounded-full px-4 py-2">
                          <span className="text-gray-500 text-sm">Сообщение...</span>
                        </div>
                        <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                          <span className="text-white text-sm">↑</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        ) : !selectedClientCode ? (
          <div className="flex items-center justify-center h-full text-center text-gray-500">
            <div>
              <div className="w-12 h-12 mx-auto mb-3 bg-gray-700/50 rounded-xl flex items-center justify-center">
                <CreditCard className="h-6 w-6 text-gray-600" />
              </div>
              <p className="text-gray-400 font-medium text-sm">Выберите клиента</p>
              <p className="text-gray-400 text-xs mt-1">Рекомендация сгенерируется автоматически</p>
            </div>
          </div>
        ) : (
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <div className="w-12 h-12 mx-auto mb-3 bg-blue-600 rounded-xl flex items-center justify-center">
                <Loader2 className="animate-spin h-6 w-6 text-white" />
              </div>
              <p className="text-gray-300 font-medium text-sm">Анализируем поведение клиента</p>
              <p className="text-gray-500 text-xs mt-1">Генерируем персонализированную рекомендацию...</p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default RecommendationPanel
