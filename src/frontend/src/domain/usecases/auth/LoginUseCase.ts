import type { IAuthRepository } from "../../repositories/IAuthRepository";
import type { LoginCredentials, LoginResponse } from "../../models/AuthModels";

export class LoginUseCase {
  constructor(private authRepository: IAuthRepository) {}

  async execute(credentials: LoginCredentials): Promise<LoginResponse> {
    if (!credentials.email || !credentials.password) {
      throw new Error("Email and password are required");
    }
    return this.authRepository.login(credentials);
  }
}
