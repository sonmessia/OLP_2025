# Tính năng Tìm kiếm Địa điểm trên Bản đồ

## Tổng quan

Tính năng tìm kiếm địa điểm đã được tích hợp vào component `PollutionMap.tsx`, cho phép người dùng tìm kiếm và điều hướng đến các địa điểm cụ thể trên bản đồ ô nhiễm.

## Quy trình hoạt động (Workflow)

### 1. **Nhập liệu từ người dùng**

- Người dùng gõ tên địa điểm vào ô tìm kiếm (ví dụ: "Đường Cầu Giấy")
- Hệ thống sử dụng **debouncing** (500ms) để tránh gọi API quá nhiều lần
- Tìm kiếm chỉ được kích hoạt khi người dùng nhập ít nhất 3 ký tự

### 2. **Gọi API Nominatim**

- **Endpoint**: `https://nominatim.openstreetmap.org/search`
- **Tham số**:
  - `q`: Từ khóa tìm kiếm
  - `format`: `json`
  - `limit`: `5` (giới hạn 5 kết quả)
  - `countrycodes`: `vn` (chỉ tìm kiếm trong Việt Nam)
  - `addressdetails`: `1` (bao gồm chi tiết địa chỉ)

### 3. **Nhận và hiển thị kết quả**

Nominatim trả về danh sách JSON chứa:

- `display_name`: Tên đầy đủ của địa điểm
- `lat`, `lon`: Tọa độ vĩ độ và kinh độ
- `boundingbox`: Khung bao để zoom bản đồ
- `place_id`: ID duy nhất của địa điểm

### 4. **Điều hướng bản đồ**

- Khi người dùng chọn một kết quả, bản đồ sẽ "bay" (fly) đến vị trí đó
- Zoom level tự động tăng lên 15 để xem chi tiết
- Animation mượt mà với thời gian 1.5 giây

## Các tính năng chính

### ✅ Debouncing

- Tránh gọi API liên tục khi người dùng đang gõ
- Chỉ gọi API sau 500ms người dùng ngừng gõ

### ✅ Loading State

- Hiển thị spinner khi đang tìm kiếm
- Thông báo rõ ràng cho người dùng

### ✅ Dropdown kết quả

- Hiển thị tối đa 5 kết quả
- Mỗi kết quả có icon địa điểm
- Hover effect để tăng trải nghiệm người dùng
- Hỗ trợ dark mode

### ✅ Clear Button

- Nút xóa để reset tìm kiếm nhanh chóng
- Chỉ hiển thị khi có nội dung trong ô tìm kiếm

### ✅ No Results Message

- Thông báo khi không tìm thấy kết quả
- Hiển thị từ khóa tìm kiếm để người dùng biết

### ✅ Map Navigation

- Sử dụng `useMap` hook từ react-leaflet
- Component `MapController` để điều khiển bản đồ
- Animation mượt mà với `flyTo` method

## Cấu trúc Code

### State Management

```typescript
const [searchQuery, setSearchQuery] = useState("");
const [searchResults, setSearchResults] = useState<NominatimResult[]>([]);
const [isSearching, setIsSearching] = useState(false);
const [showResults, setShowResults] = useState(false);
const [mapCenter, setMapCenter] = useState<[number, number] | null>(null);
const [mapZoom, setMapZoom] = useState(13);
const searchTimeoutRef = useRef<number | null>(null);
```

### Interface

```typescript
interface NominatimResult {
  place_id: number;
  display_name: string;
  lat: string;
  lon: string;
  boundingbox: [string, string, string, string];
}
```

### Key Functions

#### `performSearch(query: string)`

- Gọi Nominatim API
- Xử lý response và cập nhật state
- Error handling

#### `handleLocationSelect(result: NominatimResult)`

- Parse tọa độ từ kết quả
- Cập nhật center và zoom của bản đồ
- Đóng dropdown và cập nhật search query

#### `MapController`

- Component con để điều khiển bản đồ
- Sử dụng `useMap` hook
- Trigger `flyTo` khi có thay đổi center/zoom

## UI Components

### Search Input

- Icon tìm kiếm bên trái
- Loading spinner hoặc nút xóa bên phải
- Placeholder hướng dẫn người dùng
- Focus state với ring màu xanh lá

### Results Dropdown

- Position absolute để overlay
- Max height với scroll
- Border và shadow để nổi bật
- Transition mượt mà

### Result Item

- Icon địa điểm màu xanh lá
- Tên địa điểm đầy đủ
- Hover effect
- Truncate text nếu quá dài

## Responsive Design

- Hỗ trợ dark mode đầy đủ
- Responsive với các kích thước màn hình
- Touch-friendly cho mobile

## Best Practices

### 1. **Performance**

- Debouncing để giảm số lượng API calls
- Cleanup timeout trong useEffect
- Limit kết quả API về 5 items

### 2. **User Experience**

- Loading indicator rõ ràng
- Error handling graceful
- No results message
- Clear button để reset nhanh

### 3. **Accessibility**

- Semantic HTML
- Proper button elements
- Focus states
- Keyboard navigation support

### 4. **Code Quality**

- TypeScript types đầy đủ
- Clean component structure
- Separation of concerns
- Reusable MapController component

## Cách sử dụng

1. Mở trang Dashboard
2. Tìm component "Bản đồ Nhiệt độ Ô nhiễm"
3. Nhập tên địa điểm vào ô tìm kiếm (ví dụ: "Đường Cầu Giấy")
4. Chờ kết quả hiển thị (tối đa 500ms)
5. Click vào kết quả mong muốn
6. Bản đồ sẽ tự động bay đến vị trí đó

## Lưu ý

- Nominatim API có rate limiting, nên sử dụng debouncing
- Chỉ tìm kiếm trong phạm vi Việt Nam (`countrycodes: 'vn'`)
- Cần kết nối internet để sử dụng tính năng này
- API là public và miễn phí từ OpenStreetMap

## Future Improvements

- [ ] Cache kết quả tìm kiếm
- [ ] Lưu lịch sử tìm kiếm
- [ ] Gợi ý địa điểm phổ biến
- [ ] Tìm kiếm theo vị trí hiện tại
- [ ] Tích hợp với backend để tìm kiếm dữ liệu ô nhiễm
- [ ] Thêm marker cho địa điểm được tìm kiếm
- [ ] Export/share vị trí
