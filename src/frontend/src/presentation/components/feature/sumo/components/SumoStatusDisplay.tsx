// Copyright (c) 2025 Green Wave Team
//
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import React from 'react'
import { useTranslation } from 'react-i18next'
import { Wifi, WifiOff } from 'lucide-react'

import type { SumoStatus, SumoSimulationState } from '../../../../../domain/models/SumoModels'

interface SumoStatusDisplayProps {
  status: SumoStatus
  simulationState: SumoSimulationState | null
}

export const SumoStatusDisplay: React.FC<SumoStatusDisplayProps> = ({
  status,
  simulationState,
}) => {
  const { t } = useTranslation('sumo')

  const getStatusIcon = () => {
    if (status.connected) return <Wifi className="w-5 h-5" />
    return <WifiOff className="w-5 h-5" />
  }

  const getStatusColor = () => {
    if (status.connected) return 'text-emerald-500 dark:text-emerald-400'
    return 'text-gray-500 dark:text-gray-400'
  }

  return (
    <div className="bg-gray-50 dark:bg-gray-800/50 rounded-lg p-4 mb-4">
      <div className="grid grid-cols-2 gap-4 text-sm">
        <div className="flex items-center gap-2">
          {getStatusIcon()}
          <div>
            <span className="text-gray-600 dark:text-gray-400 text-xs">{t('status.status')}</span>
            <p className={`font-bold ${getStatusColor()}`}>
              {status.connected ? t('status.connected') : t('status.disconnected')}
            </p>
          </div>
        </div>
        <div>
          <span className="text-gray-600 dark:text-gray-400 text-xs">{t('status.scenario')}</span>
          <p className="font-bold text-gray-900 dark:text-white truncate">
            {status.scenario || t('status.notRunning')}
          </p>
        </div>
        <div>
          <span className="text-gray-600 dark:text-gray-400 text-xs">{t('status.time')}</span>
          <p className="font-bold text-gray-900 dark:text-white">
            {simulationState?.simulationTime.toFixed(1) || '0.0'}s
          </p>
        </div>
        <div>
          <span className="text-gray-600 dark:text-gray-400 text-xs">{t('status.vehicles')}</span>
          <p className="font-bold text-gray-900 dark:text-white">
            {simulationState?.vehicleCount || 0}
          </p>
        </div>
      </div>
    </div>
  )
}
