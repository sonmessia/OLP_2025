// src/data/mappers/AuthMapper.ts

import { UserDto, LoginResponseDto, RegisterResponseDto, UserRolesDto } from '../dtos/AuthDTOs';
import { User, LoginResponse, RegisterResponse, UserRole } from '../../domain/models/AuthModels';

/**
 * Chuyển đổi role từ DTO sang Domain Model
 */
export const mapUserRoleDtoToDomain = (role: UserRolesDto): UserRole => {
  switch (role) {
    case UserRolesDto.ADMIN:
      return UserRole.ADMIN;
    case UserRolesDto.AREA_MANAGER:
      return UserRole.AREA_MANAGER;
    default:
      throw new Error(`Unknown user role: ${role}`);
  }
};

/**
 * Chuyển đổi role từ Domain Model sang DTO
 */
export const mapUserRoleDomainToDto = (role: UserRole): UserRolesDto => {
  switch (role) {
    case UserRole.ADMIN:
      return UserRolesDto.ADMIN;
    case UserRole.AREA_MANAGER:
      return UserRolesDto.AREA_MANAGER;
    default:
      throw new Error(`Unknown user role: ${role}`);
  }
};

/**
 * Chuyển đổi User DTO sang Domain Model
 */
export const mapUserDtoToDomain = (userDto: UserDto): User => {
  return {
    id: userDto.id,
    email: userDto.email,
    name: userDto.name,
    role: mapUserRoleDtoToDomain(userDto.role),
    areaName: userDto.area_name,
    createdAt: new Date(userDto.created_at),
    updatedAt: new Date(userDto.updated_at),
  };
};

/**
 * Chuyển đổi Login Response DTO sang Domain Model
 */
export const mapLoginResponseDtoToDomain = (loginResponseDto: LoginResponseDto): LoginResponse => {
  return {
    user: mapUserDtoToDomain(loginResponseDto.user),
    token: loginResponseDto.token,
  };
};

/**
 * Chuyển đổi Register Response DTO sang Domain Model
 */
export const mapRegisterResponseDtoToDomain = (registerResponseDto: RegisterResponseDto): RegisterResponse => {
  return {
    user: mapUserDtoToDomain(registerResponseDto.user),
    token: registerResponseDto.token,
  };
};