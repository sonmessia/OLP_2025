// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import {
  CarbonFootprintType,
  type AddressModel,
  type LocationModel,
} from "./CommonModels";

export interface CarbonFootprintModel {
  id: string;
  type: CarbonFootprintType.CarbonFootprint;

  CO2eq: number; // Carbon dioxide equivalent emissions (bắt buộc)
  emissionDate?: Date;
  emissionSource?: string;

  address?: AddressModel;
  location?: LocationModel;
  tags?: string[];
}
