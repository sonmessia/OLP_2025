// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import { useTranslation } from "react-i18next";
import {
  AIR_QUALITY_ATTRIBUTES,
  TRAFFIC_FLOW_ATTRIBUTES,
  OPERATORS,
} from "./constants";

export const useLocalizedSubscriptionConstants = () => {
  const { t } = useTranslation();

  const localizedAirQualityAttributes = AIR_QUALITY_ATTRIBUTES.map((attr) => ({
    value: attr.value,
    // @ts-expect-error - dynamic key from constants
    label: t(attr.labelKey as string) as string,
  }));

  const localizedTrafficFlowAttributes = TRAFFIC_FLOW_ATTRIBUTES.map(
    (attr) => ({
      value: attr.value,
      // @ts-expect-error - dynamic key from constants
      label: t(attr.labelKey as string) as string,
    })
  );

  const localizedOperators = OPERATORS.map((op) => ({
    value: op.value,
    // @ts-expect-error - dynamic key from constants
    label: t(op.labelKey as string) as string,
  }));

  return {
    AIR_QUALITY_ATTRIBUTES: localizedAirQualityAttributes,
    TRAFFIC_FLOW_ATTRIBUTES: localizedTrafficFlowAttributes,
    OPERATORS: localizedOperators,
  };
};
