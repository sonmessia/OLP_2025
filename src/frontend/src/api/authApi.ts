// src/api/authApi.ts

import type {
  LoginRequestDto,
  RegisterRequestDto,
  LoginResponseDto,
  RegisterResponseDto,
} from "../data/dtos/AuthDTOs";
import { UserRolesDto } from "../data/dtos/AuthDTOs";

// Mock data cho người dùng
const MOCK_USERS = [
  {
    id: "1",
    email: "admin@olp.vn",
    password: "admin123",
    name: "Quản lý chính",
    role: UserRolesDto.ADMIN,
    created_at: new Date("2024-01-01").toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: "2",
    email: "manager.thuduc@olp.vn",
    password: "manager123",
    name: "Nguyễn Văn A",
    role: UserRolesDto.AREA_MANAGER,
    area_name: "Ngã 4 Thủ Đức",
    created_at: new Date("2024-01-15").toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: "3",
    email: "manager.nguyenthaison@olp.vn",
    password: "manager123",
    name: "Trần Thị B",
    role: UserRolesDto.AREA_MANAGER,
    area_name: "Vòng Xoay Nguyễn Thái Sơn",
    created_at: new Date("2024-02-01").toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: "4",
    email: "manager.quangtrung@olp.vn",
    password: "manager123",
    name: "Lê Văn C",
    role: UserRolesDto.AREA_MANAGER,
    area_name: "Ngã 5 Chuồng Chó (Quang Trung)",
    created_at: new Date("2024-02-15").toISOString(),
    updated_at: new Date().toISOString(),
  },
];

/**
 * Mock API delay function
 */
const delay = (ms: number = 800): Promise<void> => {
  return new Promise((resolve) => setTimeout(resolve, ms));
};

/**
 * Authentication API Client
 */
export class AuthApiClient {
  /**
   * Đăng nhập người dùng
   */
  async login(credentials: LoginRequestDto): Promise<LoginResponseDto> {
    await delay();

    // Tìm người dùng trong mock data
    const user = MOCK_USERS.find(
      (u) =>
        u.email === credentials.email && u.password === credentials.password
    );

    if (!user) {
      throw new Error("Email hoặc mật khẩu không đúng");
    }

    // Tạo mock token
    const token = `mock-jwt-token-${user.id}-${Date.now()}`;

    // Trả về response không bao gồm password
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const { password: _password, ...userResponse } = user;

    return {
      user: userResponse,
      token,
    };
  }

  /**
   * Đăng ký người dùng mới
   */
  async register(userData: RegisterRequestDto): Promise<RegisterResponseDto> {
    await delay();

    // Kiểm tra email đã tồn tại
    const existingUser = MOCK_USERS.find((u) => u.email === userData.email);
    if (existingUser) {
      throw new Error("Email đã được sử dụng");
    }

    // Kiểm tra logic cho area manager
    if (userData.role === UserRolesDto.AREA_MANAGER && !userData.area_name) {
      throw new Error("Tên khu vực là bắt buộc đối với Quản lý khu vực");
    }

    // Tạo user mới
    const newUser = {
      id: (MOCK_USERS.length + 1).toString(),
      email: userData.email,
      password: userData.password,
      name: userData.name,
      role: userData.role,
      area_name: userData.area_name,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };

    // Thêm vào mock data (trong thực tế sẽ lưu vào database)
    MOCK_USERS.push(newUser);

    // Tạo mock token
    const token = `mock-jwt-token-${newUser.id}-${Date.now()}`;

    // Trả về response không bao gồm password
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const { password: _password, ...userResponse } = newUser;

    return {
      user: userResponse,
      token,
    };
  }

  /**
   * Xác thực token và lấy thông tin user
   */
  async verifyToken(token: string): Promise<LoginResponseDto["user"]> {
    await delay();

    // Parse token để lấy user ID
    const tokenParts = token.split("-");
    const userId = tokenParts[3];

    if (!userId) {
      throw new Error("Token không hợp lệ");
    }

    // Tìm user theo ID
    const user = MOCK_USERS.find((u) => u.id === userId);

    if (!user) {
      throw new Error("User không tồn tại");
    }

    // Trả về user không bao gồm password
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const { password: _password, ...userResponse } = user;

    return userResponse;
  }

  /**
   * Đăng xuất
   */
  async logout(): Promise<void> {
    await delay();
    // Mock logout - trong thực tế sẽ gọi API để logout
    return;
  }
}

export const authApi = new AuthApiClient();
