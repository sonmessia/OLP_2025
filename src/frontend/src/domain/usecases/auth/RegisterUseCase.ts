// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import type { IAuthRepository } from "../../repositories/IAuthRepository";
import type { RegisterData, RegisterResponse } from "../../models/AuthModels";

export class RegisterUseCase {
  constructor(private authRepository: IAuthRepository) {}

  async execute(data: RegisterData): Promise<RegisterResponse> {
    // Basic validation logic can be added here
    if (!data.email || !data.password || !data.name) {
      throw new Error("Missing required fields");
    }
    return this.authRepository.register(data);
  }
}
