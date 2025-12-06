// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import type {
  LoginCredentials,
  LoginResponse,
  RegisterData,
  RegisterResponse,
  User,
} from "../models/AuthModels";

export interface IAuthRepository {
  login(credentials: LoginCredentials): Promise<LoginResponse>;
  register(data: RegisterData): Promise<RegisterResponse>;
  verifyToken(token: string): Promise<User>;
  logout(): Promise<void>;
}
