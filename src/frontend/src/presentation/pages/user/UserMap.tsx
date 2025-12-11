// Copyright (c) 2025 Green Wave Team
//
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import React, { useState, useEffect } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { UserMapHeader } from '../../components/feature/usermap/UserMapHeader'

import { AQIGauge } from '../../components/feature/usermap/AQIGauge'
import { TrafficStatusCard } from '../../components/feature/usermap/TrafficStatusCard'

import { fetchSumoState } from '../../../data/redux/sumoSlice'
import type { RootState, AppDispatch } from '../../../data/redux/store'

export const UserMap: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>()
  const { simulationState } = useSelector((state: RootState) => state.sumo)

  const [isDarkMode, setIsDarkMode] = useState(false)

  const [searchQuery, setSearchQuery] = useState('')

  // Initialize dark mode
  useEffect(() => {
    const getInitialDarkMode = () => {
      if (typeof window !== 'undefined') {
        const stored = localStorage.getItem('darkMode')
        if (stored !== null) {
          return stored === 'true'
        }
        return window.matchMedia('(prefers-color-scheme: dark)').matches
      }
      return false
    }

    setIsDarkMode(getInitialDarkMode())
  }, [])

  // Poll SUMO Traffic Data
  useEffect(() => {
    // Fetch immediately
    dispatch(fetchSumoState())

    // Poll every 5 seconds
    const intervalId = setInterval(() => {
      dispatch(fetchSumoState())
    }, 5000)

    return () => clearInterval(intervalId)
  }, [dispatch])

  // Apply dark mode class
  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }, [isDarkMode])

  const handleThemeToggle = () => {
    const newDarkMode = !isDarkMode
    setIsDarkMode(newDarkMode)
    localStorage.setItem('darkMode', newDarkMode.toString())
  }

  const handleSearch = (query: string) => {
    setSearchQuery(query)
  }

  // State to track last update time
  const [lastUpdated, setLastUpdated] = useState(new Date())

  // Update timestamp when simulationState changes
  useEffect(() => {
    if (simulationState) {
      setLastUpdated(new Date())
    }
  }, [simulationState])

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 relative">
      {/* Header */}
      <UserMapHeader
        onThemeToggle={handleThemeToggle}
        isDarkMode={isDarkMode}
        onSearch={handleSearch}
        searchQuery={searchQuery}
      />

      {/* Main Content */}
      <div className="relative z-0 h-[calc(100vh-72px)]">
        {/* Map Placeholder */}
        <div className="w-full h-full flex items-center justify-center bg-gray-100 dark:bg-gray-800">
          <div className="text-center p-8">
            <div className="text-6xl mb-4">🗺️</div>
            <h2 className="text-2xl font-bold text-gray-700 dark:text-gray-300 mb-2">
              Map Feature Removed
            </h2>
            <p className="text-gray-600 dark:text-gray-400">
              The map feature has been removed for license compliance.
            </p>
          </div>
        </div>

        {/* AQI Gauge - Fixed Position (Bottom Left) */}
        <div className="absolute bottom-6 left-4 z-[1000]">
          <AQIGauge value={50} isDarkMode={isDarkMode} />
        </div>

        {/* Traffic Status Card - Fixed Position (Bottom Right) */}
        {simulationState && (
          <div className="absolute bottom-6 right-4 z-[1000] w-80">
            <TrafficStatusCard
              avgSpeed={simulationState.avgSpeed}
              vehicleCount={simulationState.vehicleCount}
              waitingTime={simulationState.waitingTime}
              lastUpdated={lastUpdated}
              isDarkMode={isDarkMode}
            />
          </div>
        )}
      </div>
    </div>
  )
}
