// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import axiosInstance from "../app/config/axiosConfig";
import type {
  DeviceResponseDTO,
  DeviceListResponseDTO,
  DeviceFilterDTO,
} from "../data/dtos/DeviceDTOs";

export class DeviceApiClient {
  private readonly BASE_URL = "/api/v1/devices";

  async getAll(params?: DeviceFilterDTO): Promise<DeviceListResponseDTO> {
    try {
      const response = await axiosInstance.get<DeviceListResponseDTO>(
        this.BASE_URL,
        {
          params,
        }
      );
      return response.data;
    } catch (error) {
      console.error("Error fetching devices:", error);
      // Return empty list on error to prevent UI crash
      return { devices: [], total: 0, page: 1, limit: 10 };
    }
  }

  async getById(id: string): Promise<DeviceResponseDTO | null> {
    try {
      const response = await axiosInstance.get<DeviceResponseDTO>(
        `${this.BASE_URL}/${id}`
      );
      return response.data;
    } catch (error) {
      console.error(`Error fetching device ${id}:`, error);
      return null;
    }
  }

  async getLowBattery(threshold: number = 20): Promise<DeviceResponseDTO[]> {
    try {
      const response = await axiosInstance.get<DeviceResponseDTO[]>(
        `${this.BASE_URL}/low-battery`,
        {
          params: { threshold },
        }
      );
      return response.data;
    } catch (error) {
      console.error("Error fetching low battery devices:", error);
      return [];
    }
  }

  async getInactive(days: number = 1): Promise<DeviceResponseDTO[]> {
    try {
      const response = await axiosInstance.get<DeviceResponseDTO[]>(
        `${this.BASE_URL}/inactive`,
        {
          params: { days },
        }
      );
      return response.data;
    } catch (error) {
      console.error("Error fetching inactive devices:", error);
      return [];
    }
  }
}

export const deviceApi = new DeviceApiClient();
export default deviceApi;
