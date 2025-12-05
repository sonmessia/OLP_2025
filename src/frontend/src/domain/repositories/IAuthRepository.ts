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
