// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import type { ISubscriptionRepository } from "../../repositories/ISubscriptionRepository";
import type { SubscriptionCreate } from "../../models/SubscriptionModels";

export class CreateSubscriptionUseCase {
  private repository: ISubscriptionRepository;

  constructor(repository: ISubscriptionRepository) {
    this.repository = repository;
  }

  async execute(subscription: SubscriptionCreate): Promise<string> {
    return await this.repository.createSubscription(subscription);
  }
}
