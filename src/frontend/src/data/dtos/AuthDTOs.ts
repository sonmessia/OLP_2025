// Copyright (c) 2025 Green Wave Team
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

// src/data/dtos/AuthDTOs.ts

export enum UserRolesDto {
  ADMIN = 'admin',
  AREA_MANAGER = 'area_manager'
}

export interface UserDto {
  id: string;
  email: string;
  name: string;
  role: UserRolesDto;
  area_name?: string; // Chỉ có ở Area Manager
  created_at: string; // ISO string
  updated_at: string; // ISO string
}

export interface LoginRequestDto {
  email: string;
  password: string;
}

export interface RegisterRequestDto {
  email: string;
  password: string;
  name: string;
  role: UserRolesDto;
  area_name?: string; // Chỉ có khi role là AREA_MANAGER
}

export interface LoginResponseDto {
  user: UserDto;
  token: string;
}

export interface RegisterResponseDto {
  user: UserDto;
  token: string;
}