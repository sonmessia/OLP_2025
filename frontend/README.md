# GreenWave Digital Twin - Frontend

Frontend application cho hệ thống giám sát và điều khiển giao thông thông minh.

## Tính Năng

- ✅ **Digital Twin Visualization**: Hiển thị bản đồ giao thông real-time với Leaflet
- ✅ **Area Selection**: Chọn và khóa góc nhìn vào khu vực cụ thể
- ✅ **Real-time Updates**: WebSocket connection để nhận dữ liệu real-time
- ✅ **Traffic Control**: Điều khiển pha đèn giao thông
- ✅ **Statistics Dashboard**: Hiển thị thống kê giao thông và chất lượng không khí

## Tech Stack

- **React 19** + **TypeScript**
- **Redux Toolkit** - State management
- **Leaflet** - Interactive maps
- **TailwindCSS** - Styling
- **Vite** - Build tool
- **WebSocket** - Real-time communication

## Cài Đặt

```bash
npm install
```

## Cấu Hình

Tạo file `.env`:

```env
VITE_API_URL=http://localhost:3001
VITE_WS_URL=ws://localhost:8765
VITE_ORION_URL=http://localhost:1026/ngsi-ld/v1
```

## Chạy Development

```bash
npm run dev
```

Mở http://localhost:5173

## Build Production

```bash
npm run build
npm run preview
```

## Cấu Trúc Theo Clean Architecture

```
src/
├── presentation/        # UI Layer
│   ├── pages/
│   │   └── DigitalTwinPage.tsx
│   ├── components/
│   │   └── feature/
│   │       ├── TrafficMap.tsx
│   │       ├── AreaSelector.tsx
│   │       ├── TrafficStats.tsx
│   │       └── TrafficControl.tsx
│   ├── hooks/
│   │   └── useWebSocket.ts
│   └── App.tsx
│
├── domain/              # Business Logic
│   ├── models/
│   │   └── simulation.types.ts
│   └── use-cases/
│
├── data/                # Data Layer
│   ├── redux/
│   ├── dtos/
│   └── mappers/
│
└── services/            # External Services
    └── repositories/
```

## Components

### TrafficMap

Bản đồ Leaflet hiển thị:

- Vehicles với rotation theo góc
- Traffic lights với màu sắc theo trạng thái
- Locked view vào khu vực được chọn

### AreaSelector

Chọn khu vực giám sát:

- Ngã Tư Thủ Đức
- Ngã Tư Hàng Xanh
- (Có thể thêm nhiều khu vực)

### TrafficStats

Hiển thị thống kê:

- Hàng đợi xe (queues)
- Pha đèn hiện tại
- PM2.5 (chất lượng không khí)
- AI Reward Score

### TrafficControl

Điều khiển đèn giao thông:

- Pha 0: Đông-Tây
- Pha 1: Bắc-Nam
- Pha 2: Chuyển tiếp

## WebSocket Integration

```typescript
const { isConnected, lastMessage, sendCommand } = useWebSocket({
  url: "ws://localhost:8765",
  onMessage: (data) => {
    // Handle simulation update
  },
});

// Send command
sendCommand({ type: "setPhase", phase: 1 });
```

## License

MIT
