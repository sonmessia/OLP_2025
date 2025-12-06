// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import type { ISubscriptionRepository } from "../../repositories/ISubscriptionRepository";

export class DeleteSubscriptionUseCase {
  private repository: ISubscriptionRepository;

  constructor(repository: ISubscriptionRepository) {
    this.repository = repository;
  }

  async execute(id: string): Promise<void> {
    await this.repository.deleteSubscription(id);
  }
}
