// Copyright (c) 2025 Green Wave Team
//
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import React from 'react'
import { useTranslation } from 'react-i18next'
import {
  Trash2,
  Activity,
  Wind,
  Car,
  Bell,
  CheckCircle2,
  XCircle,
  AlertCircle,
  Link as LinkIcon,
  Filter,
} from 'lucide-react'
import type { Subscription } from '../../../../domain/models/SubscriptionModels'

interface SubscriptionCardProps {
  subscription: Subscription
  onDelete: (id: string) => void
}

export const SubscriptionCard: React.FC<SubscriptionCardProps> = ({ subscription, onDelete }) => {
  const { t } = useTranslation(['subscription', 'common'])

  const isTrafficFlow = subscription.entities[0]?.type === 'TrafficFlowObserved'
  const isActive = subscription.status !== 'failed'
  const hasConditions = subscription.q && subscription.q.length > 0
  const attributeCount = subscription.watchedAttributes?.length || 0

  // Determine gradient colors based on entity type
  const gradientClass = isTrafficFlow
    ? 'bg-gradient-to-br from-blue-500 to-indigo-600'
    : 'bg-gradient-to-br from-emerald-500 to-teal-600'

  return (
    <div className="group bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 overflow-hidden hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
      {/* Gradient Header */}
      <div className={`${gradientClass} px-6 py-4 relative overflow-hidden`}>
        <div className="absolute inset-0 bg-black/10"></div>
        <div className="relative flex justify-between items-start">
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-white/20 backdrop-blur-sm rounded-xl">
              {isTrafficFlow ? (
                <Car className="w-6 h-6 text-white" />
              ) : (
                <Wind className="w-6 h-6 text-white" />
              )}
            </div>
            <div>
              <h3 className="text-lg font-bold text-white line-clamp-1 mb-0.5">
                {subscription.description}
              </h3>
              <div className="flex items-center gap-2">
                <span className="text-xs text-white/80 font-medium">
                  {subscription.entities[0]?.type || 'N/A'}
                </span>
                {isActive && (
                  <div className="flex items-center gap-1">
                    <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                    <span className="text-xs text-white/90 font-medium">Active</span>
                  </div>
                )}
              </div>
            </div>
          </div>
          <button
            onClick={() => onDelete(subscription.id)}
            className="p-2 bg-white/10 hover:bg-white/20 backdrop-blur-sm rounded-lg transition-all duration-200 text-white hover:scale-110"
            title={t('deleteTooltip')}
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Card Body */}
      <div className="p-6 space-y-4">
        {/* Status and Stats Row */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            {isActive ? (
              <CheckCircle2 className="w-4 h-4 text-green-500" />
            ) : (
              <XCircle className="w-4 h-4 text-red-500" />
            )}
            <span
              className={`text-sm font-semibold ${
                isActive ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'
              }`}
            >
              {subscription.status || 'active'}
            </span>
          </div>
          <div className="flex items-center gap-1.5 px-3 py-1.5 bg-gray-100 dark:bg-gray-700 rounded-lg">
            <Bell className="w-3.5 h-3.5 text-gray-600 dark:text-gray-400" />
            <span className="text-xs font-semibold text-gray-700 dark:text-gray-300">
              {subscription.timesSent || 0} {t('sentLabel').toLowerCase()}
            </span>
          </div>
        </div>

        {/* Watched Attributes Section */}
        {attributeCount > 0 && (
          <div className="space-y-2">
            <div className="flex items-center gap-2">
              <Activity className="w-4 h-4 text-gray-500 dark:text-gray-400" />
              <span className="text-xs font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wide">
                Monitored Attributes ({attributeCount})
              </span>
            </div>
            <div className="flex flex-wrap gap-2">
              {subscription.watchedAttributes?.map((attr) => (
                <span
                  key={attr}
                  className={`${
                    isTrafficFlow
                      ? 'bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300 border-blue-200 dark:border-blue-800'
                      : 'bg-emerald-50 dark:bg-emerald-900/20 text-emerald-700 dark:text-emerald-300 border-emerald-200 dark:border-emerald-800'
                  } px-3 py-1.5 rounded-lg text-xs font-medium border`}
                >
                  {attr}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Query Conditions Section */}
        {hasConditions && (
          <div className="space-y-2">
            <div className="flex items-center gap-2">
              <Filter className="w-4 h-4 text-gray-500 dark:text-gray-400" />
              <span className="text-xs font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wide">
                {t('conditionLabel')}
              </span>
            </div>
            <div className="relative">
              <code className="block bg-gradient-to-r from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 px-4 py-3 rounded-lg text-xs font-mono text-pink-600 dark:text-pink-400 break-all border border-gray-200 dark:border-gray-700">
                {subscription.q}
              </code>
              <div className="absolute top-2 right-2">
                <AlertCircle className="w-3.5 h-3.5 text-pink-500 dark:text-pink-400" />
              </div>
            </div>
          </div>
        )}

        {/* Notification URI Section */}
        <div className="pt-4 border-t border-gray-200 dark:border-gray-700">
          <div className="flex items-start gap-2">
            <LinkIcon className="w-4 h-4 text-gray-400 mt-0.5 flex-shrink-0" />
            <div className="flex-1 min-w-0">
              <span className="text-xs font-semibold text-gray-500 dark:text-gray-400 block mb-1">
                Notification Endpoint
              </span>
              <p
                className="text-xs text-gray-700 dark:text-gray-300 truncate font-mono bg-gray-50 dark:bg-gray-900 px-2 py-1 rounded"
                title={subscription.notificationUri}
              >
                {subscription.notificationUri}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Footer Accent */}
      <div className={`h-1 ${gradientClass}`}></div>
    </div>
  )
}
