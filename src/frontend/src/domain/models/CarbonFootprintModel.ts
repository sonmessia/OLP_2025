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
