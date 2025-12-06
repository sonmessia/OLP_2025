// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import type { ISubscriptionRepository } from "../../domain/repositories/ISubscriptionRepository";
import type {
  Subscription,
  SubscriptionCreate,
  SubscriptionUpdate,
} from "../../domain/models/SubscriptionModels";
import { SubscriptionApiClient } from "../../api/SubscriptionApiClient";

export class SubscriptionRepositoryImpl implements ISubscriptionRepository {
  private apiClient: SubscriptionApiClient;

  constructor(apiClient: SubscriptionApiClient) {
    this.apiClient = apiClient;
  }

  async getSubscriptions(
    limit?: number,
    offset?: number
  ): Promise<Subscription[]> {
    return await this.apiClient.getSubscriptions(limit, offset);
  }

  async getSubscription(id: string): Promise<Subscription> {
    return await this.apiClient.getSubscription(id);
  }

  async createSubscription(subscription: SubscriptionCreate): Promise<string> {
    const result = await this.apiClient.createSubscription(subscription);
    return result.id;
  }

  async updateSubscription(
    id: string,
    subscription: SubscriptionUpdate
  ): Promise<void> {
    await this.apiClient.updateSubscription(id, subscription);
  }

  async deleteSubscription(id: string): Promise<void> {
    await this.apiClient.deleteSubscription(id);
  }
}
