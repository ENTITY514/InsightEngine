import React from 'react';
import { ChevronRight, Users } from 'lucide-react';

import { Client } from '../types/types';

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
          {[...Array(10)].map((_, i) => (
            <div key={i} className="h-12 bg-gray-700/50 rounded-xl animate-pulse"></div>
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
      <div className="space-y-2 max-h-[600px] overflow-y-auto custom-scrollbar">
        {clients.map((client) => (
          <button
            key={client.client_code}
            onClick={() => onClientSelect(client.client_code)}
            className={`w-full p-1 text-left rounded-xl transition-all duration-300 flex items-center justify-between group relative overflow-hidden ${
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

export default ClientSelector;