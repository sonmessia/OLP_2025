# Authentication System

Hệ thống authentication được xây dựng theo kiến trúc Clean Architecture với các thành phần sau:

## 📁 Cấu trúc thư mục

```
src/frontend/src/
├── domain/
│   └── models/
│       └── AuthModels.ts          # Domain models (User, AuthState, etc.)
├── data/
│   ├── dtos/
│   │   └── AuthDTOs.ts           # API Data Transfer Objects
│   ├── mappers/
│   │   └── AuthMapper.ts         # DTO ↔ Domain Model transformation
│   └── redux/
│       ├── authSlice.ts          # Redux authentication state management
│       └── store.ts              # Redux store configuration
├── api/
│   └── authApi.ts                # Authentication API client with mock data
└── presentation/
    ├── pages/
    │   ├── LoginPage.tsx         # Login page
    │   ├── RegisterPage.tsx      # Registration page
    │   └── AreaManagerPage.tsx   # Area manager dashboard
    ├── components/
    │   └── common/
    │       ├── ProtectedRoute.tsx    # Route protection wrapper
    │       ├── AuthHeader.tsx        # Header with user info & logout
    │       └── UnauthorizedPage.tsx  # Access denied page
    └── App.tsx                     # Routing configuration
```

## 🔐 Tài khoản demo

### Quản lý chính (Admin)
- **Email:** `admin@olp.vn`
- **Mật khẩu:** `admin123`
- **Quyền:** Truy cập tất cả các trang, bao gồm ControlTrafficPage

### Quản lý khu vực (Area Manager)
- **Email:** `manager.nguyenkieuan@olp.vn`
- **Mật khẩu:** `manager123`
- **Khu vực:** `Ngã 4 Thủ Đức`
- **Email:** `manager.huynhminhquy@olp.vn`
- **Mật khẩu:** `manager123`
- **Khu vực:** `Khu công nghệ cao`
- **Quyền:** Chỉ truy cập AreaManagerPage

## 🚀 Routing & Access Control

### Public Routes
- `/` - UserMap (bản đồ người dùng)
- `/login` - Trang đăng nhập
- `/register` - Trang đăng ký
- `/introduce` - Landing page
- `/unauthorized` - Trang truy cập bị từ chối

### Protected Routes
- `/control` - ControlTrafficPage (chỉ Admin)
- `/admin` - ManagerDashboard (chỉ Admin)
- `/area-manager` - AreaManagerPage (chỉ Area Manager)
- `/devices` - DeviceManagementPage (cả Admin và Area Manager)

## 🔄 Luồng xử lý authentication

1. **Login:**
   ```
   UI (LoginPage) → Redux Action → authApi.login() → Mock API → Map DTO → Update Redux State
   ```

2. **Route Protection:**
   ```
   ProtectedRoute → Check isAuthenticated → Check role → Render children or Redirect
   ```

3. **Auto-authentication:**
   ```
   App mount → Check localStorage → Verify token → Update Redux state
   ```

## 🛠️ Công nghệ sử dụng

- **State Management:** Redux Toolkit với Async Thunks
- **API:** Mock API với delay simulation
- **Type Safety:** TypeScript interfaces & enums
- **Routing:** React Router DOM v7 với Protected Routes
- **Styling:** Tailwind CSS utilities

## 🔧 Data Flow

1. **Domain Models:** Pure TypeScript interfaces, không dependencies
2. **DTOs:** API response shape (snake_case)
3. **Mappers:** Transform DTO ↔ Domain Model với validation
4. **API:** Mock data với async operations
5. **Redux:** Centralized state management với persistence
6. **UI:** React components với TypeScript

## 📝 Các tính năng

- ✅ Đăng nhập/Đăng ký với form validation
- ✅ Role-based access control (Admin vs Area Manager)
- ✅ Protected routes với redirects
- ✅ Persistent authentication (localStorage)
- ✅ Auto token verification
- ✅ Logout functionality
- ✅ Error handling & user feedback
- ✅ Responsive UI design
- ✅ TypeScript type safety

## 🔍 Sử dụng trong development

1. Khởi động ứng dụng: `npm run dev`
2. Truy cập `http://localhost:5173/login`
3. Sử dụng tài khoản demo để đăng nhập
4. Test các routes với vai trò khác nhau

## 🚀 Production deployment

Trong môi trường production, thay thế mock API trong `authApi.ts` với API calls thực tế:

```typescript
// Thay thế mock functions với axios calls
export const authApi = {
  async login(credentials: LoginRequestDto): Promise<LoginResponseDto> {
    const response = await axios.post('/api/auth/login', credentials);
    return response.data;
  },
  // ... other methods
};
```

## 🔐 Security considerations

1. Sử dụng HTTPS trong production
2. Implement JWT token refresh logic
3. Add rate limiting cho login attempts
4. Sanitize user inputs
5. Implement proper session management
6. Add CORS configuration
7. Use environment variables cho sensitive data