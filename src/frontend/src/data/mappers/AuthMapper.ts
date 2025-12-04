// src/data/mappers/AuthMapper.ts

import type {
  UserDto,
  LoginResponseDto,
  RegisterResponseDto,
  RegisterRequestDto,
} from "../dtos/AuthDTOs";
import { UserRolesDto } from "../dtos/AuthDTOs";
import type {
  User,
  LoginResponse,
  RegisterResponse,
  RegisterData,
} from "../../domain/models/AuthModels";
import { UserRole } from "../../domain/models/AuthModels";

/**
 * Auth Mapper Class
 */
export class AuthMapper {
  /**
   * Chuyển đổi role từ DTO sang Domain Model
   */
  static mapUserRoleDtoToDomain(role: UserRolesDto): UserRole {
    switch (role) {
      case UserRolesDto.ADMIN:
        return UserRole.ADMIN;
      case UserRolesDto.AREA_MANAGER:
        return UserRole.AREA_MANAGER;
      default:
        throw new Error(`Unknown user role: ${role}`);
    }
  }

  /**
   * Chuyển đổi role từ Domain Model sang DTO
   */
  static mapUserRoleDomainToDto(role: UserRole): UserRolesDto {
    switch (role) {
      case UserRole.ADMIN:
        return UserRolesDto.ADMIN;
      case UserRole.AREA_MANAGER:
        return UserRolesDto.AREA_MANAGER;
      default:
        throw new Error(`Unknown user role: ${role}`);
    }
  }

  /**
   * Chuyển đổi User DTO sang Domain Model
   */
  static mapUserDtoToDomain(userDto: UserDto): User {
    return {
      id: userDto.id,
      email: userDto.email,
      name: userDto.name,
      role: this.mapUserRoleDtoToDomain(userDto.role),
      areaName: userDto.area_name,
      createdAt: new Date(userDto.created_at),
      updatedAt: new Date(userDto.updated_at),
    };
  }

  /**
   * Chuyển đổi Login Response DTO sang Domain Model
   */
  static mapLoginResponseDtoToDomain(
    loginResponseDto: LoginResponseDto
  ): LoginResponse {
    return {
      user: this.mapUserDtoToDomain(loginResponseDto.user),
      token: loginResponseDto.token,
    };
  }

  /**
   * Chuyển đổi Register Response DTO sang Domain Model
   */
  static mapRegisterResponseDtoToDomain(
    registerResponseDto: RegisterResponseDto
  ): RegisterResponse {
    return {
      user: this.mapUserDtoToDomain(registerResponseDto.user),
      token: registerResponseDto.token,
    };
  }

  /**
   * Chuyển đổi Register Data từ Domain Model sang DTO
   */
  static mapRegisterDataToDto(registerData: RegisterData): RegisterRequestDto {
    return {
      email: registerData.email,
      password: registerData.password,
      name: registerData.name,
      role: this.mapUserRoleDomainToDto(registerData.role),
      area_name: registerData.areaName,
    };
  }
}
