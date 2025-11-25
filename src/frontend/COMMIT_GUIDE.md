Hướng dẫn Viết Commit Message Chuẩn (Git Commit Guide)

Chào mừng bạn đến với hướng dẫn quản lý lịch sử code của dự án GreenWave.
Tại sao chúng ta cần chuẩn này? Vì Lịch sử Git (Git History) chính là Tài liệu. Một lịch sử commit sạch đẹp giúp người review code hiểu bạn đang làm gì, giúp việc tìm lỗi (debug) nhanh hơn, và tự động tạo được ChangeLog.
Chúng ta tuân thủ chặt chẽ chuẩn Conventional Commits.

1. Cấu trúc Commit (The Format)

Mỗi commit message bao gồm 3 phần: Header, Body (tùy chọn), và Footer (tùy chọn).

Plaintext

<type>(<scope>): <subject>

[optional body]

[optional footer(s)]

Ví dụ hoàn chỉnh:

Plaintext

feat(ai): implement new reward function based on CO2 levels

The old function only considered traffic flow. This new logic adds
a 50% weight for environmental impact using PM2.5 sensor data.

Closes #123

2. Header (Bắt buộc)

Dòng đầu tiên không được quá 72 ký tự.

type (Loại thay đổi)

Bạn chỉ được sử dụng các loại sau:
Type
Ý nghĩa
Ví dụ
feat
Thêm tính năng mới (tương ứng MINOR version)
feat(iot): add traci connection
fix
Sửa lỗi bug (tương ứng PATCH version)
fix(backend): resolve timeout error
docs
Chỉ thay đổi tài liệu
docs: update setup guide
style
Sửa format, thiếu dấu chấm phẩy, space (không đổi logic)
style(ai): format code with black
refactor
Sửa code nhưng không sửa lỗi hay thêm tính năng
refactor(infra): optimize docker build
perf
Cải thiện hiệu năng
perf(db): add index to query
test
Thêm hoặc sửa test
test(ai): add unit test for agent
chore
Thay đổi tool build, thư viện, việc lặt vặt
chore(deps): upgrade numpy
ci
Thay đổi cấu hình CI/CD (GitHub Actions)
ci: fix commitlint workflow

scope (Phạm vi)

Dành riêng cho dự án GreenWave, hãy chỉ rõ commit này tác động vào đâu:
infra: Docker, MongoDB, Orion-LD, Server.
backend: API, Python scripts, Data ingestion.
ai: RL Agents, Model training, TensorFlow/PyTorch.
iot: SUMO, TraCI scripts, Sensors.
frontend: Dashboard, UI.
docs: README, Wiki.
deps: Các file requirements.txt hoặc package.json.

subject (Tiêu đề ngắn)

Mô tả ngắn gọn thay đổi.
✅ ĐÚNG: Sử dụng thể mệnh lệnh (Imperative mood): "add", "change", "fix", "remove".
❌ SAI: Quá khứ: "added", "changed", "fixed".
❌ SAI: Viết hoa chữ đầu: "Add feature". (Hãy viết thường toàn bộ: "add feature").
❌ SAI: Có dấu chấm câu ở cuối.

3. Body (Tùy chọn)

Dùng khi tiêu đề không đủ để giải thích.
Sử dụng thể mệnh lệnh.
Giải thích tại sao cần thay đổi này, thay vì như thế nào (code đã tự giải thích "như thế nào" rồi).
