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
