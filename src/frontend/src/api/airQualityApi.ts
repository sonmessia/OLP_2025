// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import axiosInstance from "../app/config/axiosConfig";
import type { AirQualityObservedDto } from "../data/dtos/AirQualityDTOs";
import type {
  BatchDeleteRequest,
  BatchOperationRequest,
  NgsiLdAttributePatch,
  QueryParams,
} from "./types";
import { generateMockAirQualityData } from "../utils/mockAirQualityData";

const BASE_PATH = "/api/v1/air-quality";

export class AirQualityApiClient {
  /**
   * Query AirQualityObserved Entities
   */
  async getAll(): Promise<AirQualityObservedDto[] | number> {
    // Mock data implementation
    await new Promise((resolve) => setTimeout(resolve, 800)); // Simulate network delay
    return generateMockAirQualityData();

    /* 
    // Real API implementation
    const response = await axiosInstance.get<
      AirQualityObservedDto[] | number
    >(BASE_PATH, { params });
    return response.data;
    */
  }

  /**
   * Get AirQualityObserved Entity by ID
   */
  async getById(
    entityId: string,
    params?: Pick<QueryParams, "pick" | "attrs" | "format" | "options">
  ): Promise<AirQualityObservedDto> {
    const response = await axiosInstance.get<AirQualityObservedDto>(
      `${BASE_PATH}/${entityId}`,
      { params }
    );
    return response.data;
  }

  /**
   * Create AirQualityObserved Entity
   */
  async create(
    data: AirQualityObservedDto
  ): Promise<{ message: string; id: string }> {
    const response = await axiosInstance.post<{ message: string; id: string }>(
      BASE_PATH,
      data
    );
    return response.data;
  }

  /**
   * Update Entity Attributes (Partial Update)
   */
  async updateAttributes(
    entityId: string,
    data: Record<string, NgsiLdAttributePatch>
  ): Promise<void> {
    await axiosInstance.patch(`${BASE_PATH}/${entityId}/attrs`, data);
  }

  /**
   * Replace Entity (Full Update)
   */
  async replace(entityId: string, data: AirQualityObservedDto): Promise<void> {
    await axiosInstance.put(`${BASE_PATH}/${entityId}`, data);
  }

  /**
   * Delete AirQualityObserved Entity
   */
  async delete(entityId: string): Promise<void> {
    await axiosInstance.delete(`${BASE_PATH}/${entityId}`);
  }

  /**
   * Delete Entity Attribute
   */
  async deleteAttribute(
    entityId: string,
    attributeName: string
  ): Promise<void> {
    await axiosInstance.delete(
      `${BASE_PATH}/${entityId}/attrs/${attributeName}`
    );
  }

  /**
   * Batch Create Entities
   */
  async batchCreate(
    entities: AirQualityObservedDto[]
  ): Promise<string[] | { success: boolean }> {
    const request: BatchOperationRequest<AirQualityObservedDto> = {
      entities,
    };
    const response = await axiosInstance.post<string[] | { success: boolean }>(
      `${BASE_PATH}/batch/create`,
      request
    );
    return response.data;
  }

  /**
   * Batch Upsert Entities
   */
  async batchUpsert(
    entities: AirQualityObservedDto[],
    options: "update" | "replace" = "update"
  ): Promise<string[] | { success: boolean }> {
    const request: BatchOperationRequest<AirQualityObservedDto> = {
      entities,
    };
    const response = await axiosInstance.post<string[] | { success: boolean }>(
      `${BASE_PATH}/batch/upsert`,
      request,
      { params: { options } }
    );
    return response.data;
  }

  /**
   * Batch Delete Entities
   */
  async batchDelete(entityIds: string[]): Promise<void> {
    const request: BatchDeleteRequest = { entity_ids: entityIds };
    await axiosInstance.post(`${BASE_PATH}/batch/delete`, request);
  }
}

export const airQualityApi = new AirQualityApiClient();
