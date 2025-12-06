// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import type { ISubscriptionRepository } from "../../repositories/ISubscriptionRepository";
import type { Subscription } from "../../models/SubscriptionModels";

export class GetSubscriptionsUseCase {
  private repository: ISubscriptionRepository;

  constructor(repository: ISubscriptionRepository) {
    this.repository = repository;
  }

  async execute(limit?: number, offset?: number): Promise<Subscription[]> {
    return await this.repository.getSubscriptions(limit, offset);
  }
}
