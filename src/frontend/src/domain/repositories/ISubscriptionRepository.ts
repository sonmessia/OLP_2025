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
