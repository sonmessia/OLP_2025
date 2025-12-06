// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import React, { useState, useEffect } from "react";
import { Plus, Trash2 } from "lucide-react";
import { useTranslation } from "react-i18next";
import type {
  SubscriptionCreate,
  EntityPattern,
} from "../../../../domain/models/SubscriptionModels";
import { useLocalizedSubscriptionConstants } from "./LocalizedConstants";

interface SubscriptionFormProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (subscription: SubscriptionCreate) => Promise<void>;
}

interface QueryCondition {
  attribute: string;
  operator: string;
  value: string;
}

export const SubscriptionForm: React.FC<SubscriptionFormProps> = ({
  isOpen,
  onClose,
  onSubmit,
}) => {
  const { t } = useTranslation(["subscription", "common", "forms"]);
  const { AIR_QUALITY_ATTRIBUTES, TRAFFIC_FLOW_ATTRIBUTES, OPERATORS } =
    useLocalizedSubscriptionConstants();

  const [description, setDescription] = useState("");
  const [entityType, setEntityType] = useState("AirQualityObserved");
  const [notificationUri, setNotificationUri] = useState("");
  const [selectedAttributes, setSelectedAttributes] = useState<string[]>([]);
  const [queryConditions, setQueryConditions] = useState<QueryCondition[]>([]);

  // Reset form when modal opens
  useEffect(() => {
    if (isOpen) {
      setDescription("");
      setEntityType("AirQualityObserved");
      setNotificationUri("");
      setSelectedAttributes([]);
      setQueryConditions([]);
    }
  }, [isOpen]);

  const availableAttributes =
    entityType === "AirQualityObserved"
      ? AIR_QUALITY_ATTRIBUTES
      : TRAFFIC_FLOW_ATTRIBUTES;

  const handleAttributeToggle = (value: string) => {
    setSelectedAttributes((prev) =>
      prev.includes(value)
        ? prev.filter((attr) => attr !== value)
        : [...prev, value]
    );
  };

  const addQueryCondition = () => {
    if (availableAttributes.length > 0) {
      setQueryConditions([
        ...queryConditions,
        { attribute: availableAttributes[0].value, operator: "==", value: "" },
      ]);
    }
  };

  const removeQueryCondition = (index: number) => {
    setQueryConditions(queryConditions.filter((_, i) => i !== index));
  };

  const updateQueryCondition = (
    index: number,
    field: keyof QueryCondition,
    value: string
  ) => {
    const newConditions = [...queryConditions];
    newConditions[index] = { ...newConditions[index], [field]: value };
    setQueryConditions(newConditions);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Build query string
    const queryString = queryConditions
      .filter((c) => c.value.trim() !== "")
      .map((c) => `${c.attribute}${c.operator}${c.value}`)
      .join(";");

    const entities: EntityPattern[] = [{ type: entityType }];

    const newSubscription: SubscriptionCreate = {
      description,
      entities,
      watchedAttributes:
        selectedAttributes.length > 0 ? selectedAttributes : undefined,
      q: queryString || undefined,
      notificationUri,
      notificationFormat: "normalized",
    };

    await onSubmit(newSubscription);
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4 backdrop-blur-sm">
      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl w-full max-w-2xl overflow-hidden max-h-[90vh] flex flex-col">
        <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white">
            {t("createAlert")}
          </h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 dark:hover:text-gray-300"
          >
            ✕
          </button>
        </div>

        <form
          onSubmit={handleSubmit}
          className="p-6 space-y-4 overflow-y-auto flex-1"
        >
          {/* Description */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              {t("description")}
            </label>
            <input
              type="text"
              required
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder={t("placeholder")}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-emerald-500 dark:bg-gray-700 dark:text-white"
            />
          </div>

          {/* Entity Type */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              {t("dataType")}
            </label>
            <select
              value={entityType}
              onChange={(e) => {
                setEntityType(e.target.value);
                setSelectedAttributes([]);
                setQueryConditions([]);
              }}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-emerald-500 dark:bg-gray-700 dark:text-white"
            >
              <option value="AirQualityObserved">{t("airQuality")}</option>
              <option value="TrafficFlowObserved">{t("trafficFlow")}</option>
            </select>
          </div>

          {/* Watched Attributes (Multi-select) */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              {t("watchedAttributes")}
            </label>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
              {availableAttributes.map((attr) => (
                <label
                  key={attr.value}
                  className={`flex items-center gap-2 p-2 rounded-lg border cursor-pointer transition-colors ${
                    selectedAttributes.includes(attr.value)
                      ? "bg-emerald-50 border-emerald-500 dark:bg-emerald-900/20 dark:border-emerald-500"
                      : "border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700"
                  }`}
                >
                  <input
                    type="checkbox"
                    checked={selectedAttributes.includes(attr.value)}
                    onChange={() => handleAttributeToggle(attr.value)}
                    className="w-4 h-4 text-emerald-600 rounded focus:ring-emerald-500"
                  />
                  <span className="text-sm text-gray-700 dark:text-gray-300">
                    {attr.label}
                  </span>
                </label>
              ))}
            </div>
            <p className="text-xs text-gray-500 mt-1">
              {selectedAttributes.length === 0
                ? t("monitorAll")
                : t("selectedCount", { count: selectedAttributes.length })}
            </p>
          </div>

          {/* Query Builder */}
          <div>
            <div className="flex justify-between items-center mb-2">
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                {t("queryConditions")}
              </label>
              <button
                type="button"
                onClick={addQueryCondition}
                className="text-xs flex items-center gap-1 text-emerald-600 hover:text-emerald-700 font-medium"
              >
                <Plus className="w-3 h-3" /> {t("addCondition")}
              </button>
            </div>

            <div className="space-y-2">
              {queryConditions.map((condition, index) => (
                <div key={index} className="flex gap-2 items-center">
                  <select
                    value={condition.attribute}
                    onChange={(e) =>
                      updateQueryCondition(index, "attribute", e.target.value)
                    }
                    className="flex-1 px-2 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-white"
                  >
                    {availableAttributes.map((attr) => (
                      <option key={attr.value} value={attr.value}>
                        {attr.label}
                      </option>
                    ))}
                  </select>
                  <select
                    value={condition.operator}
                    onChange={(e) =>
                      updateQueryCondition(index, "operator", e.target.value)
                    }
                    className="w-24 px-2 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-white"
                  >
                    {OPERATORS.map((op) => (
                      <option key={op.value} value={op.value}>
                        {op.label}
                      </option>
                    ))}
                  </select>
                  <input
                    type="text"
                    value={condition.value}
                    onChange={(e) =>
                      updateQueryCondition(index, "value", e.target.value)
                    }
                    placeholder={t("forms:value")}
                    className="flex-1 px-2 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-white"
                  />
                  <button
                    type="button"
                    onClick={() => removeQueryCondition(index)}
                    className="p-1.5 text-gray-400 hover:text-red-500"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              ))}
              {queryConditions.length === 0 && (
                <div className="text-sm text-gray-500 italic bg-gray-50 dark:bg-gray-800/50 p-2 rounded border border-dashed border-gray-200 dark:border-gray-700">
                  {t("noConditions")}
                </div>
              )}
            </div>
          </div>

          {/* Notification URI */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              {t("notificationUri")}
            </label>
            <input
              type="text"
              required
              value={notificationUri}
              onChange={(e) => setNotificationUri(e.target.value)}
              placeholder={t("notificationPlaceholder")}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-emerald-500 dark:bg-gray-700 dark:text-white"
            />
          </div>
        </form>

        <div className="px-6 py-4 border-t border-gray-200 dark:border-gray-700 flex justify-end gap-3 bg-gray-50 dark:bg-gray-800/50">
          <button
            type="button"
            onClick={onClose}
            className="px-4 py-2 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
          >
            {t("common:cancel")}
          </button>
          <button
            onClick={handleSubmit}
            className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg transition-colors font-medium"
          >
            {t("create")}
          </button>
        </div>
      </div>
    </div>
  );
};
