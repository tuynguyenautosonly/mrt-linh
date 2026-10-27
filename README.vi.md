# mrT × Linh

**Hai trợ lý, hai vai trò, cùng một luồng công việc xưởng.**

[**Mở trang giới thiệu và thử demo →**](https://tuynguyenautosonly.github.io/mrt-linh/) · [English](README.md)

- **mrT** hỗ trợ KTV gom dữ kiện, làm việc với ảnh/tài liệu và tra cứu kỹ thuật theo đúng ca xe.
- **Linh** giúp cố vấn đọc tiến độ đúng xe, soạn bản nháp cập nhật để người phụ trách đọc lại.
- **Luồng nguồn** giữ liên kết xe–phiếu–công việc, vai trò, phiên bản và thời điểm quan sát.

## Thử được gì?

1. Hỏi Linh “xe đã xong chưa?”, rồi đổi vai trò, xe hoặc độ mới của nguồn. Luật JavaScript cục bộ sẽ quyết định có tạo bản nháp hay giữ lại ngữ cảnh.
2. Xem các kịch bản mrT: phân biệt chữ trong ảnh với kết luận chẩn đoán; chưa có manual đúng xe thì nói thiếu; ca mới không mang kết luận từ xe cũ sang.
3. Mở bộ kiểm CSV phụ để thấy việc “báo xong” chưa phải nghiệm thu, mã trùng và cập nhật quá cũ được tách riêng thế nào.

**Đây là bản giới thiệu dùng dữ liệu giả.** Kịch bản mrT và nội dung bản nháp được soạn sẵn, không phải phản hồi AI trực tiếp. Luật kiểm vai trò/xe/độ mới và bộ kiểm CSV chạy thật trong trình duyệt. Trang không kết nối khách hàng hoặc hệ thống xưởng.

Bản triển khai nội bộ có các phần đã chạy và kiểm cục bộ, nhưng vẫn ghi nhận mrT kết luận kỹ thuật quá mức. Không coi kiểm thử native, luật đã cài hay trang demo này là bằng chứng model đã tuân thủ mọi tình huống. Xem [bảng năng lực và bằng chứng](CAPABILITIES.md).

Repo chỉ chứa mã viết mới và dữ liệu giả, không có mã triển khai nội bộ, chat riêng, hồ sơ xe hay tài liệu hãng. Mục tiêu hiện tại là **cho cộng đồng thấy cách hệ thống hoạt động và nhận phản biện**, chưa phải bán sản phẩm.

Chạy: `npm test`, rồi `python -m http.server 8097 --bind 127.0.0.1 --directory docs`. Xem hướng dẫn và giới hạn chi tiết ở [README chính](README.md).
