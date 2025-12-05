// src/domain/models/AuthModels.ts

export enum UserRole {
  ADMIN = 'admin',
  AREA_MANAGER = 'area_manager'
}

export interface User {
  id: string;
  email: string;
  name: string;
  role: UserRole;
  areaName?: string; // Chỉ có ở Area Manager
  createdAt: Date;
  updatedAt: Date;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  name: string;
  role: UserRole;
  areaName?: string; // Chỉ có khi role là AREA_MANAGER
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

export interface LoginResponse {
  user: User;
  token: string;
}

export interface RegisterResponse {
  user: User;
  token: string;
}