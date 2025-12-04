import axiosInstance from "../app/config/axiosConfig";
import type {
  Subscription,
  SubscriptionCreate,
  SubscriptionUpdate,
} from "../domain/models/SubscriptionModels";

export class SubscriptionApiClient {
  async getSubscriptions(
    limit?: number,
    offset?: number
  ): Promise<Subscription[]> {
    const params = { limit, offset };
    const response = await axiosInstance.get<Subscription[]>(
      "/api/v1/subscriptions/",
      { params }
    );
    return response.data;
  }

  async getSubscription(id: string): Promise<Subscription> {
    const response = await axiosInstance.get<Subscription>(
      `/api/v1/subscriptions/${id}`
    );
    return response.data;
  }

  async createSubscription(
    subscription: SubscriptionCreate
  ): Promise<{ message: string; id: string }> {
    const response = await axiosInstance.post<{ message: string; id: string }>(
      "/api/v1/subscriptions/",
      subscription
    );
    return response.data;
  }

  async updateSubscription(
    id: string,
    subscription: SubscriptionUpdate
  ): Promise<void> {
    await axiosInstance.patch(`/api/v1/subscriptions/${id}`, subscription);
  }

  async deleteSubscription(id: string): Promise<void> {
    await axiosInstance.delete(`/api/v1/subscriptions/${id}`);
  }
}

export const subscriptionApiClient = new SubscriptionApiClient();
