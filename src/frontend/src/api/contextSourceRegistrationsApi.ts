import axiosInstance from "./axiosConfig";
import type {
  RegistrationCreate,
  RegistrationUpdate,
  QueryParams,
} from "./types";

const BASE_PATH = "/api/v1/csourceRegistrations";

export const contextSourceRegistrationsApi = {
  /**
   * Create a new context source registration
   */
  create: async (
    data: RegistrationCreate,
    tenant?: string
  ): Promise<{ message: string; id: string; mode: string }> => {
    const response = await axiosInstance.post<{
      message: string;
      id: string;
      mode: string;
    }>(BASE_PATH, data, {
      params: { tenant },
    });
    return response.data;
  },

  /**
   * Get all context source registrations
   */
  getAll: async (
    params?: Pick<QueryParams, "entity_type" | "limit" | "offset" | "tenant">
  ): Promise<Record<string, any>[]> => {
    const response = await axiosInstance.get<Record<string, any>[]>(BASE_PATH, {
      params,
    });
    return response.data;
  },

  /**
   * Get details of a registration
   */
  getById: async (
    registrationId: string,
    tenant?: string
  ): Promise<Record<string, any>> => {
    const response = await axiosInstance.get<Record<string, any>>(
      `${BASE_PATH}/${registrationId}`,
      {
        params: { tenant },
      }
    );
    return response.data;
  },

  /**
   * Update a registration
   */
  update: async (
    registrationId: string,
    data: RegistrationUpdate,
    tenant?: string
  ): Promise<void> => {
    await axiosInstance.patch(`${BASE_PATH}/${registrationId}`, data, {
      params: { tenant },
    });
  },

  /**
   * Delete a registration
   */
  delete: async (registrationId: string, tenant?: string): Promise<void> => {
    await axiosInstance.delete(`${BASE_PATH}/${registrationId}`, {
      params: { tenant },
    });
  },

  /**
   * Quick redirect registration
   */
  quickRedirect: async (
    entityType: string,
    endpoint: string,
    description?: string,
    tenant?: string
  ): Promise<{ message: string; id: string }> => {
    const response = await axiosInstance.post<{ message: string; id: string }>(
      `${BASE_PATH}/quick/redirect`,
      null,
      {
        params: {
          entity_type: entityType,
          endpoint,
          description,
          tenant,
        },
      }
    );
    return response.data;
  },

  /**
   * Quick federation registration
   */
  quickFederation: async (
    entityType: string,
    endpoint: string,
    description?: string,
    tenant?: string
  ): Promise<{ message: string; id: string }> => {
    const response = await axiosInstance.post<{ message: string; id: string }>(
      `${BASE_PATH}/quick/federation`,
      null,
      {
        params: {
          entity_type: entityType,
          endpoint,
          description,
          tenant,
        },
      }
    );
    return response.data;
  },

  /**
   * Quick device registration
   */
  quickDevice: async (
    entityId: string,
    entityType: string,
    properties: string,
    iotAgent: string,
    description?: string,
    tenant?: string
  ): Promise<{ message: string; id: string }> => {
    const response = await axiosInstance.post<{ message: string; id: string }>(
      `${BASE_PATH}/quick/device`,
      null,
      {
        params: {
          entity_id: entityId,
          entity_type: entityType,
          properties,
          iot_agent: iotAgent,
          description,
          tenant,
        },
      }
    );
    return response.data;
  },
};
