// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import type { IAuthRepository } from "../../domain/repositories/IAuthRepository";
import type {
  LoginCredentials,
  LoginResponse,
  RegisterData,
  RegisterResponse,
  User,
} from "../../domain/models/AuthModels";
import { authApi } from "../../api/authApi";
import { AuthMapper } from "../mappers/AuthMapper";

export class AuthRepositoryImpl implements IAuthRepository {
  async login(credentials: LoginCredentials): Promise<LoginResponse> {
    const responseDto = await authApi.login({
      email: credentials.email,
      password: credentials.password,
    });
    return AuthMapper.mapLoginResponseDtoToDomain(responseDto);
  }

  async register(data: RegisterData): Promise<RegisterResponse> {
    const responseDto = await authApi.register({
      email: data.email,
      password: data.password,
      name: data.name,
      role: AuthMapper.mapUserRoleDomainToDto(data.role),
      area_name: data.areaName,
    });
    return AuthMapper.mapRegisterResponseDtoToDomain(responseDto);
  }

  async verifyToken(token: string): Promise<User> {
    const userDto = await authApi.verifyToken(token);
    return AuthMapper.mapUserDtoToDomain(userDto);
  }

  async logout(): Promise<void> {
    await authApi.logout();
  }
}
