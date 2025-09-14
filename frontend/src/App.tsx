"use client"

import type React from "react"
import { useState, useEffect } from "react"
import { Bot } from "lucide-react"

import type { Client, ClientDashboardData, RecommendationResponse } from "./types/types"
import { fetchClients, fetchClientData, generateRecommendation } from "./api/clientApi"

import ClientSelector from "./components/ClientSelector"
import ClientDashboard from "./components/ClientDashboard"
import RecommendationPanel from "./components/RecommendationPanel"

const App: React.FC = () => {
  const [clients, setClients] = useState<Client[]>([])
  const [selectedClientCode, setSelectedClientCode] = useState<number | null>(null)
  const [clientData, setClientData] = useState<ClientDashboardData | null>(null)
  const [recommendation, setRecommendation] = useState<RecommendationResponse | null>(null)
  const [loadingClients, setLoadingClients] = useState(true)
  const [loadingClientData, setLoadingClientData] = useState(false)
  const [loadingRecommendation, setLoadingRecommendation] = useState(false)

  // Load clients on mount
  useEffect(() => {
    const loadClients = async () => {
      try {
        const clientsData = await fetchClients()
        setClients(clientsData)
      } catch (error) {
        console.error("Error loading clients:", error)
      } finally {
        setLoadingClients(false)
      }
    }

    loadClients()
  }, [])

  // Load client data when selected client changes
  useEffect(() => {
    if (selectedClientCode) {
      setLoadingClientData(true)
      setClientData(null)
      setRecommendation(null)

      const loadClientData = async () => {
        try {
          const data = await fetchClientData(selectedClientCode)
          setClientData(data)
        } catch (error) {
          console.error("Error loading client data:", error)
        } finally {
          setLoadingClientData(false)
        }
      }

      loadClientData()
    } else {
      setClientData(null)
      setRecommendation(null)
    }
  }, [selectedClientCode])

  useEffect(() => {
    if (selectedClientCode && clientData && !loadingClientData) {
      setLoadingRecommendation(true)

      const autoGenerateRecommendation = async () => {
        try {
          const recommendationData = await generateRecommendation(selectedClientCode)
          setRecommendation(recommendationData)
        } catch (error) {
          console.error("Error generating recommendation:", error)
        } finally {
          setLoadingRecommendation(false)
        }
      }

      autoGenerateRecommendation()
    }
  }, [selectedClientCode, clientData, loadingClientData])

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 relative overflow-hidden">
      {/* Background Effects */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(120,119,198,0.1),transparent_50%)]"></div>
      <div className="absolute top-0 left-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl"></div>
      <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl"></div>

      <div className="relative z-10 min-h-screen p-6">
        <div className="max-w-7xl mx-auto">
          <header className="mb-10 ">
            <div className="flex items-center mb-4">
              <div className="w-12 h-12 bg-blue-600 rounded-xl flex items-center justify-center mr-4">
                <Bot className="h-7 w-7 text-white" />
              </div>
              <div>
                <h1 className="text-4xl font-bold bg-gradient-to-tr from-white to-blue-600 bg-clip-text text-transparent pb-1">
                  InsightEngine
                </h1>
                <p className="text-gray-400 ">Система аналитики и персонализированных рекомендаций</p>
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
                recommendation={recommendation}
                loading={loadingRecommendation}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
