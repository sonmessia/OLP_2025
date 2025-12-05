import axiosInstance from "../app/config/axiosConfig";
import type {
  RegistrationCreate,
  RegistrationUpdate,
  QueryParams,
  ContextSourceRegistration,
} from "./types";

const BASE_PATH = "/api/v1/csourceRegistrations";

export class ContextSourceRegistrationsApiClient {
  /**
   * Create a new context source registration
   */
  async create(
    data: RegistrationCreate,
    tenant?: string
  ): Promise<{ message: string; id: string; mode: string }> {
    const response = await axiosInstance.post<{
      message: string;
      id: string;
      mode: string;
    }>(BASE_PATH, data, {
      params: { tenant },
    });
    return response.data;
  }

  /**
   * Get all context source registrations
   */
  async getAll(
    params?: Pick<QueryParams, "entity_type" | "limit" | "offset" | "tenant">
  ): Promise<ContextSourceRegistration[]> {
    const response = await axiosInstance.get<ContextSourceRegistration[]>(
      BASE_PATH,
      {
        params,
      }
    );
    return response.data;
  }

  /**
   * Get details of a registration
   */
  async getById(
    registrationId: string,
    tenant?: string
  ): Promise<ContextSourceRegistration> {
    const response = await axiosInstance.get<ContextSourceRegistration>(
      `${BASE_PATH}/${registrationId}`,
      {
        params: { tenant },
      }
    );
    return response.data;
  }

  /**
   * Update a registration
   */
  async update(
    registrationId: string,
    data: RegistrationUpdate,
    tenant?: string
  ): Promise<void> {
    await axiosInstance.patch(`${BASE_PATH}/${registrationId}`, data, {
      params: { tenant },
    });
  }

  /**
   * Delete a registration
   */
  async delete(registrationId: string, tenant?: string): Promise<void> {
    await axiosInstance.delete(`${BASE_PATH}/${registrationId}`, {
      params: { tenant },
    });
  }

  /**
   * Quick redirect registration
   */
  async quickRedirect(
    entityType: string,
    endpoint: string,
    description?: string,
    tenant?: string
  ): Promise<{ message: string; id: string }> {
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
  }

  /**
   * Quick federation registration
   */
  async quickFederation(
    entityType: string,
    endpoint: string,
    description?: string,
    tenant?: string
  ): Promise<{ message: string; id: string }> {
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
  }

  /**
   * Quick device registration
   */
  async quickDevice(
    entityId: string,
    entityType: string,
    properties: string,
    iotAgent: string,
    description?: string,
    tenant?: string
  ): Promise<{ message: string; id: string }> {
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
  }
}

export const contextSourceRegistrationsApi =
  new ContextSourceRegistrationsApiClient();
