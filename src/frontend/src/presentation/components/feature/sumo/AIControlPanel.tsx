// Copyright (c) 2025 Green Wave Team
//
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import React, { useEffect, useRef, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useAppDispatch, useAppSelector } from '../../../../data/redux/hooks'
import {
  activateAIControl,
  deactivateAIControl,
  performAIStep,
} from '../../../../data/redux/sumoSlice'
import { Brain, Circle, Zap, ScrollText } from 'lucide-react'
import { AIStatusCard } from './components/AIStatusCard'
import { AIModelDetailsDialog } from './components/AIModelDetailsDialog'
import type { AIDecision } from '../../../../domain/models/SumoModels'

interface AIControlPanelProps {
  onLog?: (message: string) => void
}

interface AIDecisionLog extends AIDecision {
  timestamp: number
}

export const AIControlPanel: React.FC<AIControlPanelProps> = ({ onLog }) => {
  const { t } = useTranslation('sumo')
  const dispatch = useAppDispatch()
  const { aiControlState, isAIControlActive, isLoading, simulationState } = useAppSelector(
    (state) => state.sumo
  )

  const aiIntervalRef = useRef<number | null>(null)
  const [showDetailsDialog, setShowDetailsDialog] = useState(false)
  const [aiDecisionLogs, setAiDecisionLogs] = useState<AIDecisionLog[]>([])

  // AI Control Loop
  useEffect(() => {
    if (isAIControlActive && aiControlState) {
      aiIntervalRef.current = window.setInterval(async () => {
        try {
          const result = await dispatch(performAIStep()).unwrap()

          // Add decisions to log
          if (result.decisions && result.decisions.length > 0) {
            const newLogs: AIDecisionLog[] = result.decisions.map((decision) => ({
              ...decision,
              timestamp: result.simulationTime,
            }))
            setAiDecisionLogs((prev) => [...newLogs, ...prev].slice(0, 50)) // Keep last 50 decisions
          }

          if (result.totalSwitches > 0) {
            onLog?.(
              t('controlPanel.ai.log.decision', {
                switches: result.totalSwitches,
                holds: result.totalHolds,
                time: result.simulationTime.toFixed(0),
              })
            )
          }
        } catch (error) {
          console.error('AI step error:', error)
        }
      }, 2000)

      return () => {
        if (aiIntervalRef.current) {
          clearInterval(aiIntervalRef.current)
        }
      }
    }
  }, [isAIControlActive, dispatch, onLog, aiControlState, t])

  const handleEnableAI = async () => {
    try {
      await dispatch(activateAIControl()).unwrap()
      onLog?.(t('controlPanel.ai.log.enabled'))
    } catch (error) {
      onLog?.(t('controlPanel.ai.log.enableFailed', { error }))
    }
  }

  const handleDisableAI = async () => {
    try {
      await dispatch(deactivateAIControl()).unwrap()
      onLog?.(t('controlPanel.ai.log.disabled'))
    } catch (error) {
      onLog?.(t('controlPanel.ai.log.disableFailed', { error }))
    }
  }

  return (
    <>
      <div className="glass-card rounded-xl p-6 shadow-xl">
        <div className="flex items-center gap-3 mb-6">
          <Brain className="w-6 h-6 text-emerald-600 dark:text-emerald-400" />
          <h2 className="text-xl font-bold text-gray-900 dark:text-white">
            {t('controlPanel.ai.title')}
          </h2>
        </div>

        {/* Control Button */}
        <div className="mb-6">
          {!isAIControlActive ? (
            <button
              onClick={handleEnableAI}
              disabled={isLoading || !simulationState}
              className="w-full flex items-center justify-center gap-2 px-4 py-3 eco-gradient-primary text-white font-semibold rounded-lg
                         transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed
                         hover:shadow-lg hover:scale-105 disabled:hover:scale-100"
            >
              <Zap className="w-5 h-5" />
              {t('controlPanel.ai.enable')}
            </button>
          ) : (
            <button
              onClick={handleDisableAI}
              disabled={isLoading}
              className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-gray-600 hover:bg-gray-700 text-white font-semibold rounded-lg
                         transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed
                         hover:shadow-lg hover:scale-105 disabled:hover:scale-100"
            >
              <Circle className="w-5 h-5" />
              {t('controlPanel.ai.disable')}
            </button>
          )}
        </div>

        {/* AI Status */}
        {aiControlState && isAIControlActive && (
          <>
            <AIStatusCard
              aiControlState={aiControlState}
              onShowDetails={() => setShowDetailsDialog(true)}
            />

            {/* AI Decision Log */}
            {aiDecisionLogs.length > 0 && (
              <div className="mt-4">
                <div className="flex items-center gap-2 mb-3">
                  <ScrollText className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
                  <h3 className="text-sm font-semibold text-gray-900 dark:text-white">
                    {t('controlPanel.ai.decisionLog')}
                  </h3>
                </div>
                <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-3 max-h-64 overflow-y-auto space-y-2">
                  {aiDecisionLogs.map((log, index) => (
                    <div
                      key={`${log.tlsId}-${log.timestamp}-${index}`}
                      className="bg-white dark:bg-gray-700 rounded-md p-2 text-xs border border-gray-200 dark:border-gray-600"
                    >
                      <div className="flex items-center justify-between mb-1">
                        <span className="font-semibold text-emerald-600 dark:text-emerald-400">
                          {log.tlsId}
                        </span>
                        <span className="text-gray-500 dark:text-gray-400">
                          t={log.timestamp.toFixed(0)}s
                        </span>
                      </div>
                      <div className="flex items-center gap-2">
                        <span
                          className={`px-2 py-0.5 rounded text-xs font-medium ${
                            log.action === 'switch'
                              ? 'bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300'
                              : 'bg-gray-100 dark:bg-gray-600 text-gray-700 dark:text-gray-300'
                          }`}
                        >
                          {log.action}
                        </span>
                        <span className="text-gray-600 dark:text-gray-300">
                          Phase {log.fromPhase} → {log.toPhase}
                        </span>
                      </div>
                      {log.reason && (
                        <div className="mt-1 text-gray-500 dark:text-gray-400 italic">
                          {log.reason}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </>
        )}

        {/* Disabled State Message */}
        {!isAIControlActive && (
          <div className="text-center py-6">
            <Circle className="w-12 h-12 text-gray-400 mx-auto mb-3" />
            <p className="text-sm text-gray-500 dark:text-gray-400">
              {t('controlPanel.ai.disabledMessage')}
            </p>
            <p className="text-xs text-gray-400 dark:text-gray-500 mt-1">
              {t('controlPanel.ai.startSumoMessage')}
            </p>
          </div>
        )}
      </div>

      {showDetailsDialog && aiControlState && (
        <AIModelDetailsDialog
          isOpen={showDetailsDialog}
          onClose={() => setShowDetailsDialog(false)}
          aiControlState={aiControlState}
        />
      )}
    </>
  )
}
