import axiosInstance from "./axiosConfig";
import type { AirQualityObservedModel } from "../domain/models/AirQualityObservedModel";
import type {
  BatchDeleteRequest,
  BatchOperationRequest,
  NgsiLdAttributePatch,
  QueryParams,
} from "./types";

const BASE_PATH = "/api/v1/air-quality";

export const airQualityApi = {
  /**
   * Query AirQualityObserved Entities
   */
  getAll: async (
    params?: QueryParams
  ): Promise<AirQualityObservedModel[] | number> => {
    const response = await axiosInstance.get<
      AirQualityObservedModel[] | number
    >(BASE_PATH, { params });
    return response.data;
  },

  /**
   * Get AirQualityObserved Entity by ID
   */
  getById: async (
    entityId: string,
    params?: Pick<QueryParams, "pick" | "attrs" | "format" | "options">
  ): Promise<AirQualityObservedModel> => {
    const response = await axiosInstance.get<AirQualityObservedModel>(
      `${BASE_PATH}/${entityId}`,
      { params }
    );
    return response.data;
  },

  /**
   * Create AirQualityObserved Entity
   */
  create: async (
    data: AirQualityObservedModel
  ): Promise<{ message: string; id: string }> => {
    const response = await axiosInstance.post<{ message: string; id: string }>(
      BASE_PATH,
      data
    );
    return response.data;
  },

  /**
   * Update Entity Attributes (Partial Update)
   */
  updateAttributes: async (
    entityId: string,
    data: Record<string, NgsiLdAttributePatch>
  ): Promise<void> => {
    await axiosInstance.patch(`${BASE_PATH}/${entityId}/attrs`, data);
  },

  /**
   * Replace Entity (Full Update)
   */
  replace: async (
    entityId: string,
    data: AirQualityObservedModel
  ): Promise<void> => {
    await axiosInstance.put(`${BASE_PATH}/${entityId}`, data);
  },

  /**
   * Delete AirQualityObserved Entity
   */
  delete: async (entityId: string): Promise<void> => {
    await axiosInstance.delete(`${BASE_PATH}/${entityId}`);
  },

  /**
   * Delete Entity Attribute
   */
  deleteAttribute: async (
    entityId: string,
    attributeName: string
  ): Promise<void> => {
    await axiosInstance.delete(
      `${BASE_PATH}/${entityId}/attrs/${attributeName}`
    );
  },

  /**
   * Batch Create Entities
   */
  batchCreate: async (
    entities: AirQualityObservedModel[]
  ): Promise<string[] | { success: boolean }> => {
    const request: BatchOperationRequest<AirQualityObservedModel> = {
      entities,
    };
    const response = await axiosInstance.post<string[] | { success: boolean }>(
      `${BASE_PATH}/batch/create`,
      request
    );
    return response.data;
  },

  /**
   * Batch Upsert Entities
   */
  batchUpsert: async (
    entities: AirQualityObservedModel[],
    options: "update" | "replace" = "update"
  ): Promise<string[] | { success: boolean }> => {
    const request: BatchOperationRequest<AirQualityObservedModel> = {
      entities,
    };
    const response = await axiosInstance.post<string[] | { success: boolean }>(
      `${BASE_PATH}/batch/upsert`,
      request,
      { params: { options } }
    );
    return response.data;
  },

  /**
   * Batch Delete Entities
   */
  batchDelete: async (entityIds: string[]): Promise<void> => {
    const request: BatchDeleteRequest = { entity_ids: entityIds };
    await axiosInstance.post(`${BASE_PATH}/batch/delete`, request);
  },
};
