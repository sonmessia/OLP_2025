export interface EntityPattern {
  id?: string;
  type?: string;
}

export interface NotifierInfo {
  key: string;
  value: string;
}

export interface SubscriptionCreate {
  description: string;
  entities: EntityPattern[];
  watchedAttributes?: string[];
  q?: string;
  notificationFormat?: string;
  notificationUri: string;
  notificationAccept?: string;
  notifierInfo?: NotifierInfo[];
  expiresAt?: string;
  throttling?: number;
}

export interface SubscriptionUpdate {
  description?: string;
  watchedAttributes?: string[];
  q?: string;
  notification?: any;
  expiresAt?: string;
  throttling?: number;
}

export interface Subscription extends SubscriptionCreate {
  id: string;
  status?: string;
  lastNotification?: string;
  lastFailure?: string;
  lastSuccess?: string;
  timesSent?: number;
}
