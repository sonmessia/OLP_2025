// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import type {
  Subscription,
  SubscriptionCreate,
  SubscriptionUpdate,
} from "../models/SubscriptionModels";

export interface ISubscriptionRepository {
  getSubscriptions(limit?: number, offset?: number): Promise<Subscription[]>;
  getSubscription(id: string): Promise<Subscription>;
  createSubscription(subscription: SubscriptionCreate): Promise<string>;
  updateSubscription(
    id: string,
    subscription: SubscriptionUpdate
  ): Promise<void>;
  deleteSubscription(id: string): Promise<void>;
}
