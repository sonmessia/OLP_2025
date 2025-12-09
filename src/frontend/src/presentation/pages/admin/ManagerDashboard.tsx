// Copyright (c) 2025 Green Wave Team
//
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import React, { useState, useEffect } from 'react'
import { useTranslation } from 'react-i18next'
import { DashboardHeader } from '../../components/feature/dashboard/DashboardHeader'
import { KPICard } from '../../components/feature/dashboard/KPICard'
import { MonitoringChart } from '../../components/feature/dashboard/MonitoringChart'
import { DeviceHealthPanel } from '../../components/feature/dashboard/DeviceHealthPanel'
import { PollutionMap } from '../../components/feature/dashboard/PollutionMap'
import { AlertPanel } from '../../components/feature/dashboard/AlertPanel'
import { ManualControlPanel } from '../../components/feature/dashboard/ManualControlPanel'
import type {
  DashboardStateModel,
  KPICardModel,
  MonitoringDataPoint,
  RewardDataPoint,
  PollutionHotspot,
  AlertLog,
  InterventionAction,
} from '../../../domain/models/DashboardModel'
import { sumoApi } from '../../../api/sumoApi'
import { airQualityApi } from '../../../api/airQualityApi'
import type { AirQualityObservedDto } from '../../../data/dtos/AirQualityDTOs'
import { TRAFFIC_LOCATIONS } from '../../../utils/trafficLocations'
import type { TFunction } from 'i18next'

export const ManagerDashboard: React.FC = () => {
  const { t } = useTranslation([
    'dashboard',
    'monitoring',
    'traffic',
    'devices',
    'common',
    'locations',
    'alerts',
  ])

  // Initialize dark mode from localStorage or system preference
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

  const [isDarkMode, setIsDarkMode] = useState(getInitialDarkMode)

  // Mock data generator (moved inside component to access t)
  const generateMockData = (
    translate: TFunction<['dashboard', 'devices', 'common', 'locations', 'alerts']>
  ): DashboardStateModel => {
    const now = new Date()
    const timePoints = Array.from({ length: 20 }, (_, i) => {
      const time = new Date(now.getTime() - (19 - i) * 5 * 60 * 1000)
      return time.toISOString()
    })

    const kpis: KPICardModel[] = [
      {
        id: '1',
        title: translate('dashboard:kpi.waitingTime'),
        value: 45,
        unit: translate('dashboard:kpi.unit.seconds'),
        trend: 'down',
        trendValue: -12,
        icon: 'Clock',
        color: 'blue',
      },
      {
        id: '2',
        title: 'PM2.5',
        value: 35,
        unit: 'μg/m³',
        trend: 'down',
        trendValue: -8,
        icon: 'Leaf',
        color: 'green',
      },
      {
        id: '3',
        title: translate('dashboard:kpi.vehicleCount'),
        value: 1248,
        unit: translate('dashboard:kpi.unit.vehiclePerHour'),
        trend: 'up',
        trendValue: 5,
        icon: 'Car',
        color: 'yellow',
      },
      {
        id: '4',
        title: translate('dashboard:kpi.aiScore'),
        value: 87,
        unit: '%',
        trend: 'up',
        trendValue: 3,
        icon: 'Brain',
        color: 'blue',
      },
    ]

    const monitoringData: MonitoringDataPoint[] = timePoints.map((time, index) => ({
      timestamp: time,
      avgWaitingTime: 40 + Math.sin(index / 3) * 15 + Math.random() * 5,
      pm25Level: 30 + Math.cos(index / 4) * 20 + Math.random() * 8,
    }))

    const rewardData: RewardDataPoint[] = timePoints.map((time) => ({
      timestamp: time,
      trafficReward: 40 + Math.random() * 20,
      environmentReward: 30 + Math.random() * 25,
    }))

    const pollutionHotspots: PollutionHotspot[] = TRAFFIC_LOCATIONS.map((loc) => ({
      id: loc.id,
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      name: translate(loc.nameKey as any),
      latitude: loc.coordinates[0],
      longitude: loc.coordinates[1],
      pm25: 30 + Math.random() * 30, // Random initial value
      aqi: 50 + Math.random() * 50, // Random initial value
      severity: 'medium',
    }))

    const alerts: AlertLog[] = [
      {
        id: 'alert_1',
        timestamp: new Date(now.getTime() - 15 * 60000).toISOString(),
        type: 'critical',
        message: translate('alerts:pm25Critical', {
          location: 'Ngã 4 Thủ Đức',
          value: 180,
        } as any) as unknown as string,
        resolved: false,
      },
      {
        id: 'alert_2',
        timestamp: new Date(now.getTime() - 45 * 60000).toISOString(),
        type: 'warning',
        message: translate('alerts:trafficCongestion', {
          location: 'Hàng Xanh',
        } as any) as unknown as string,
        resolved: false,
      },
    ]

    const interventions: InterventionAction[] = [
      {
        id: 'int_1',
        timestamp: new Date(now.getTime() - 10 * 60000).toISOString(),
        action: String(
          translate('alerts:interventions.signalAdjustment', {
            direction: 'North-South',
          } as any)
        ),
        target: 'Ngã 4 Thủ Đức',
        status: 'completed',
        aiTriggered: true,
      },
      {
        id: 'int_2',
        timestamp: new Date(now.getTime() - 120 * 60000).toISOString(),
        action: String(
          translate('alerts:interventions.routeRebalancing', {
            route: 'Pham Van Dong',
          } as any)
        ),
        target: 'Hàng Xanh',
        status: 'pending',
        aiTriggered: false,
      },
    ]

    return {
      kpis,
      monitoringData,
      rewardData,
      pollutionHotspots,
      alerts,
      interventions,
      lastUpdated: now.toISOString(),
    }
  }

  const [dashboardData, setDashboardData] = useState<DashboardStateModel>(() => generateMockData(t))

  const [selectedSensor, setSelectedSensor] = useState<PollutionHotspot | null>(null)

  // Apply dark mode class on mount
  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }, [isDarkMode])

  // Update titles when language changes
  useEffect(() => {
    setDashboardData((prev) => ({
      ...prev,
      kpis: prev.kpis.map((kpi, index) => {
        let title = kpi.title
        let unit = kpi.unit
        if (index === 0) {
          title = t('dashboard:kpi.waitingTime')
          unit = t('dashboard:kpi.unit.seconds')
        } else if (index === 2) {
          title = t('dashboard:kpi.vehicleCount')
          unit = t('dashboard:kpi.unit.vehiclePerHour')
        } else if (index === 3) {
          title = t('dashboard:kpi.aiScore')
        }
        return { ...kpi, title, unit }
      }),
      pollutionHotspots: prev.pollutionHotspots.map((spot) => ({
        ...spot,
        name: spot.name === 'Unknown Location' ? t('devices:unknownLocation') : spot.name,
      })),
    }))
  }, [t])

  // Real-time data fetching
  useEffect(() => {
    const fetchData = async () => {
      try {
        const now = new Date().toISOString()

        // 1. Fetch Sumo State
        let sumoState = null
        try {
          sumoState = await sumoApi.getSumoState()
        } catch {
          console.warn('Could not fetch Sumo state, using previous/mock data')
        }

        // 2. Fetch Air Quality Data
        let airQualityData: AirQualityObservedDto[] = []
        try {
          const aqResponse = await airQualityApi.getAll()
          if (Array.isArray(aqResponse)) {
            airQualityData = aqResponse
          }
        } catch {
          console.warn('Could not fetch Air Quality data')
        }

        // 3. Process Data
        setDashboardData((prev) => {
          // Update KPIs
          const newKpis = [...prev.kpis]

          // Update Waiting Time (Sumo)
          if (sumoState) {
            newKpis[0] = {
              ...newKpis[0],
              value: Math.round(sumoState.waiting_time || 0),
              trend: 'stable',
            }

            // Update Vehicle Count (Sumo)
            newKpis[2] = {
              ...newKpis[2],
              value: sumoState.vehicle_count || 0,
            }
          }

          // Update PM2.5 (Air Quality)
          let avgPm25 = 0
          if (airQualityData.length > 0) {
            const totalPm25 = airQualityData.reduce((sum, item) => sum + (item.pm25 || 0), 0)
            avgPm25 = totalPm25 / airQualityData.length

            newKpis[1] = {
              ...newKpis[1],
              value: Math.round(avgPm25),
            }
          } else {
            // Fallback to previous value or mock if no data
            avgPm25 = prev.kpis[1].value
          }

          // Update Monitoring Chart (Hybrid: Keep history, add new point)
          const newPoint: MonitoringDataPoint = {
            timestamp: now,
            avgWaitingTime:
              sumoState?.waiting_time ||
              prev.monitoringData[prev.monitoringData.length - 1].avgWaitingTime,
            pm25Level:
              airQualityData.length > 0
                ? avgPm25
                : prev.monitoringData[prev.monitoringData.length - 1].pm25Level,
          }

          // Keep last 20 points
          const newMonitoringData = [...prev.monitoringData.slice(1), newPoint]

          // Update Pollution Hotspots
          const newHotspots: PollutionHotspot[] =
            airQualityData.length > 0
              ? airQualityData.map((aq) => ({
                  id: aq.id,
                  name:
                    aq.areaServed && aq.areaServed.includes('locations.')
                      ? aq.areaServed
                          .split(', ')
                          .map((k) =>
                            // eslint-disable-next-line @typescript-eslint/no-explicit-any
                            t(k.trim().replace('locations.', 'locations:') as any)
                          )
                          .join(', ')
                      : aq.areaServed || t('devices:unknownLocation'),
                  latitude: aq.location?.coordinates[1] || 0,
                  longitude: aq.location?.coordinates[0] || 0,
                  pm25: aq.pm25 || 0,
                  aqi: aq.airQualityIndex || 0,
                  severity:
                    (aq.airQualityIndex || 0) > 150
                      ? 'high'
                      : (aq.airQualityIndex || 0) > 100
                        ? 'medium'
                        : 'low',
                }))
              : prev.pollutionHotspots

          // Update Interventions (Mocking AI detection for now as API doesn't return history)
          const newInterventions = prev.interventions

          return {
            ...prev,
            kpis: newKpis,
            monitoringData: newMonitoringData,
            pollutionHotspots: newHotspots,
            interventions: newInterventions,
            lastUpdated: now,
          }
        })
      } catch (error) {
        console.error('Error updating dashboard:', error)
      }
    }

    // Initial fetch
    fetchData()

    // Poll every 5 seconds
    const interval = setInterval(fetchData, 5000)

    return () => clearInterval(interval)
  }, [t])

  const handleThemeToggle = () => {
    const newDarkMode = !isDarkMode
    setIsDarkMode(newDarkMode)
    localStorage.setItem('darkMode', newDarkMode.toString())
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <DashboardHeader onThemeToggle={handleThemeToggle} isDarkMode={isDarkMode} />

      <main className="p-4">
        {/* Top Section: Map & Controls */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
          <div className="lg:col-span-2">
            {/* KPI Cards */}
            <div className="grid grid-cols-2 lg:grid-cols-4 md:gap-6 gap-2 mb-2">
              {dashboardData.kpis.map((kpi) => (
                <KPICard key={kpi.id} kpi={kpi} />
              ))}
            </div>
            {/* Pollution Map */}
            <div className="h-[600px]">
              <PollutionMap
                hotspots={dashboardData.pollutionHotspots}
                onHotspotSelect={setSelectedSensor}
              />
            </div>
          </div>

          {/* Right Column: Alerts & Manual Control */}
          <div className="flex flex-col gap-6 h-full">
            {/* Alert Panel */}
            <div className="h-[350px]">
              <AlertPanel
                alerts={dashboardData.alerts}
                interventions={dashboardData.interventions}
              />
            </div>
            {/* Manual Control Panel */}
            <div className="flex-1 min-h-[300px]">
              <ManualControlPanel selectedSensor={selectedSensor} />
            </div>
          </div>
        </div>

        {/* Middle Row (40% Height) */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
          {/* Main Monitoring Chart - 65% */}
          <div className="lg:col-span-2 h-96">
            <MonitoringChart data={dashboardData.monitoringData} isDarkMode={isDarkMode} />
          </div>

          {/* Device Health Panel - 35% */}
          <div className="h-96">
            <DeviceHealthPanel />
          </div>
        </div>

        {/* Last Updated */}
        <div className="mt-6 text-center">
          <p className="text-sm text-gray-500 dark:text-gray-400">
            {t('dashboard:updatedAt', {
              time: new Date(dashboardData.lastUpdated).toLocaleString('vi-VN'),
            })}
          </p>
        </div>
      </main>
    </div>
  )
}
