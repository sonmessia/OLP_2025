// Copyright (c) 2025 Green Wave Team
//
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import React from 'react'
import { useTranslation } from 'react-i18next'
import type { TFunction } from 'i18next'
import {
  Leaf,
  AlertTriangle,
  AlertOctagon,
  Check,
  Wind,
  Compass,
  MapPin,
  Lightbulb,
} from 'lucide-react'
import type { AirQualityObservedModel } from '../../../../domain/models/AirQualityObservedModel'

interface HealthInsightPanelProps {
  airQuality: AirQualityObservedModel
  isDarkMode: boolean
}

const getAQIState = (aqi: number | undefined, isDarkMode: boolean, t: TFunction<'aqi'>) => {
  const value = aqi || 0

  if (value <= 50) {
    return {
      level: t('healthInsight.levels.safe'),
      icon: <Leaf className="w-8 h-8 text-green-600" />,
      color: 'green',
      bgColor: isDarkMode ? 'bg-green-900/50 border-green-700' : 'bg-green-50 border-green-200',
      textColor: isDarkMode ? 'text-green-300' : 'text-green-800',
      iconColor: 'text-green-600',
      recommendations: t('healthInsight.advice.safe', {
        returnObjects: true,
      }) as string[],
    }
  } else if (value <= 150) {
    return {
      level: t('healthInsight.levels.poor'),
      icon: <AlertTriangle className="w-8 h-8 text-yellow-600" />,
      color: 'yellow',
      bgColor: isDarkMode ? 'bg-yellow-900/50 border-yellow-700' : 'bg-yellow-50 border-yellow-200',
      textColor: isDarkMode ? 'text-yellow-300' : 'text-yellow-800',
      iconColor: 'text-yellow-600',
      recommendations: t('healthInsight.advice.poor', {
        returnObjects: true,
      }) as string[],
    }
  } else {
    return {
      level: t('healthInsight.levels.hazardous'),
      icon: <AlertOctagon className="w-8 h-8 text-red-600" />,
      color: 'red',
      bgColor: isDarkMode ? 'bg-red-900/50 border-red-700' : 'bg-red-50 border-red-200',
      textColor: isDarkMode ? 'text-red-300' : 'text-red-800',
      iconColor: 'text-red-600',
      recommendations: t('healthInsight.advice.hazardous', {
        returnObjects: true,
      }) as string[],
    }
  }
}

export const HealthInsightPanel: React.FC<HealthInsightPanelProps> = ({
  airQuality,
  isDarkMode,
}) => {
  const { t } = useTranslation(['aqi', 'subscription', 'locations'])
  const aqiState = getAQIState(airQuality.airQualityIndex, isDarkMode, t)

  return (
    <div
      className={`
      glass-card rounded-xl p-3 md:p-4 shadow-xl
      transition-all duration-300 transform h-full overflow-y-auto
      ${aqiState.textColor}
    `}
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-3 md:mb-4">
        <div className="flex items-center space-x-2 md:space-x-3">
          <div className="text-2xl md:text-3xl drop-shadow-md">{aqiState.icon}</div>
          <div>
            <h3 className={`font-bold text-base md:text-lg ${aqiState.textColor}`}>
              {t('healthInsight.status')}: {aqiState.level}
            </h3>
            <p className={`text-xs md:text-sm opacity-80`}>
              {t('healthInsight.index')}: {airQuality.airQualityIndex || 'N/A'}
            </p>
          </div>
        </div>
      </div>

      {/* Location Info */}
      {airQuality.areaServed && (
        <div className="mb-3 md:mb-4 pb-3 md:pb-4 border-b border-gray-200 dark:border-gray-600">
          <p
            className={`flex items-center text-xs md:text-sm font-medium ${
              isDarkMode ? 'text-gray-300' : 'text-gray-700'
            }`}
          >
            <MapPin className="w-3 h-3 md:w-4 md:h-4 mr-1" />{' '}
            {airQuality.areaServed && airQuality.areaServed.includes('locations.')
              ? airQuality.areaServed
                  .split(', ')
                  .map((k) =>
                    // eslint-disable-next-line @typescript-eslint/no-explicit-any
                    t(k.trim().replace('locations.', ''), { ns: 'locations' } as any)
                  )
                  .join(', ')
              : airQuality.areaServed}
          </p>
        </div>
      )}

      {/* Air Quality Details */}
      <div className="grid grid-cols-2 gap-2 md:gap-3 mb-3 md:mb-4">
        <div className="bg-white/50 dark:bg-black/20 rounded-lg p-2">
          <p className={`text-[10px] md:text-xs ${isDarkMode ? 'text-gray-400' : 'text-gray-600'}`}>
            PM2.5
          </p>
          <p
            className={`font-semibold text-sm md:text-base ${
              isDarkMode ? 'text-white' : 'text-gray-900'
            }`}
          >
            {airQuality.pm25 || 'N/A'} μg/m³
          </p>
        </div>
        <div className="bg-white/50 dark:bg-black/20 rounded-lg p-2">
          <p className={`text-[10px] md:text-xs ${isDarkMode ? 'text-gray-400' : 'text-gray-600'}`}>
            PM10
          </p>
          <p
            className={`font-semibold text-sm md:text-base ${
              isDarkMode ? 'text-white' : 'text-gray-900'
            }`}
          >
            {airQuality.pm10 || 'N/A'} μg/m³
          </p>
        </div>
        <div className="bg-white/50 dark:bg-black/20 rounded-lg p-2">
          <p className={`text-[10px] md:text-xs ${isDarkMode ? 'text-gray-400' : 'text-gray-600'}`}>
            {t('attributes.temperature', { ns: 'subscription' })}
          </p>
          <p
            className={`font-semibold text-sm md:text-base ${
              isDarkMode ? 'text-white' : 'text-gray-900'
            }`}
          >
            {airQuality.temperature || 'N/A'}°C
          </p>
        </div>
        <div className="bg-white/50 dark:bg-black/20 rounded-lg p-2">
          <p className={`text-[10px] md:text-xs ${isDarkMode ? 'text-gray-400' : 'text-gray-600'}`}>
            {t('attributes.humidity', { ns: 'subscription' })}
          </p>
          <p
            className={`font-semibold text-sm md:text-base ${
              isDarkMode ? 'text-white' : 'text-gray-900'
            }`}
          >
            {airQuality.relativeHumidity ? Math.round(airQuality.relativeHumidity * 100) : 'N/A'}%
          </p>
        </div>
      </div>

      {/* Health Recommendations */}
      <div>
        <h4
          className={`flex items-center font-semibold text-xs md:text-sm mb-2 md:mb-3 ${aqiState.textColor}`}
        >
          <Lightbulb className="w-3 h-3 md:w-4 md:h-4 mr-2" /> {t('healthInsight.recommendations')}:
        </h4>
        <ul className="space-y-1 md:space-y-2">
          {Array.isArray(aqiState.recommendations) &&
            aqiState.recommendations.map((recommendation, index) => (
              <li key={index} className="flex items-start space-x-2">
                <Check className={`w-3 h-3 md:w-4 md:h-4 mt-0.5 ${aqiState.iconColor}`} />
                <span
                  className={`text-xs md:text-sm ${isDarkMode ? 'text-gray-300' : 'text-gray-700'}`}
                >
                  {recommendation}
                </span>
              </li>
            ))}
        </ul>
      </div>

      {/* Additional Info */}
      {(airQuality.windSpeed || airQuality.windDirection) && (
        <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-600">
          <div className="flex items-center justify-between text-xs">
            {airQuality.windSpeed && (
              <span
                className={`flex items-center ${isDarkMode ? 'text-gray-400' : 'text-gray-600'}`}
              >
                <Wind className="w-3 h-3 mr-1" /> {t('healthInsight.windSpeed')}:{' '}
                {airQuality.windSpeed} m/s
              </span>
            )}
            {airQuality.windDirection && (
              <span
                className={`flex items-center ${isDarkMode ? 'text-gray-400' : 'text-gray-600'}`}
              >
                <Compass className="w-3 h-3 mr-1" /> {t('healthInsight.windDirection')}:{' '}
                {airQuality.windDirection}°
              </span>
            )}
          </div>
        </div>
      )}

      {/* Timestamp */}
      {airQuality.dateObserved && (
        <div className="mt-3 text-xs text-center">
          <span className={isDarkMode ? 'text-gray-500' : 'text-gray-400'}>
            {t('healthInsight.updated')}: {new Date(airQuality.dateObserved).toLocaleString()}
          </span>
        </div>
      )}
    </div>
  )
}
