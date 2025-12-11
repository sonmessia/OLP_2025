// Copyright (c) 2025 Green Wave Team
//
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import React from 'react'
import { useTranslation } from 'react-i18next'
import { ScrollText } from 'lucide-react'
import type { AIDecision } from '../../../../../domain/models/SumoModels'

interface AIDecisionLog extends AIDecision {
  timestamp: number
}

interface AIDecisionLogPanelProps {
  decisions: AIDecisionLog[]
}

export const AIDecisionLogPanel: React.FC<AIDecisionLogPanelProps> = ({ decisions }) => {
  const { t } = useTranslation('sumo')

  return (
    <div className="glass-card rounded-xl p-6 shadow-xl">
      <div className="flex items-center gap-3 mb-4">
        <ScrollText className="w-6 h-6 text-emerald-600 dark:text-emerald-400" />
        <h2 className="text-xl font-bold text-gray-900 dark:text-white">
          {t('controlPanel.ai.decisionLog')}
        </h2>
      </div>

      <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-4 max-h-96 overflow-y-auto space-y-2">
        {decisions.length === 0 ? (
          <div className="text-center py-8">
            <ScrollText className="w-12 h-12 text-gray-400 dark:text-gray-500 mx-auto mb-3 opacity-50" />
            <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">
              {t('controlPanel.ai.noDecisions')}
            </p>
            <p className="text-xs text-gray-400 dark:text-gray-500">
              {t('controlPanel.ai.enableAIToSeeDecisions')}
            </p>
          </div>
        ) : (
          decisions.map((log, index) => (
            <div
              key={`${log.tlsId}-${log.timestamp}-${index}`}
              className="bg-white dark:bg-gray-700 rounded-lg p-3 border border-gray-200 dark:border-gray-600 hover:border-emerald-300 dark:hover:border-emerald-600 transition-colors"
            >
              <div className="flex items-center justify-between mb-2">
                <span className="font-semibold text-emerald-600 dark:text-emerald-400">
                  {log.tlsId}
                </span>
                <span className="text-xs text-gray-500 dark:text-gray-400 font-mono">
                  t={log.timestamp.toFixed(0)}s
                </span>
              </div>
              <div className="flex items-center gap-2 mb-2">
                <span
                  className={`px-2 py-1 rounded text-xs font-medium ${
                    log.action === 'switch'
                      ? 'bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300'
                      : 'bg-gray-100 dark:bg-gray-600 text-gray-700 dark:text-gray-300'
                  }`}
                >
                  {log.action}
                </span>
                <span className="text-sm text-gray-600 dark:text-gray-300">
                  Phase {log.fromPhase} → {log.toPhase}
                </span>
              </div>
              {log.reason && (
                <div className="mt-2 text-xs text-gray-500 dark:text-gray-400 italic border-l-2 border-emerald-300 dark:border-emerald-600 pl-2">
                  {log.reason}
                </div>
              )}
            </div>
          ))
        )}
      </div>

      <div className="mt-3 text-xs text-gray-500 dark:text-gray-400 text-center">
        {decisions.length} {t('logs.count')} • {t('flowChart.liveUpdating')}
      </div>
    </div>
  )
}
