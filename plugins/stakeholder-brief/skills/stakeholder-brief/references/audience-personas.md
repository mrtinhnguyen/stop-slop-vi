# Hồ sơ đối tượng đọc (mỗi lần một)

Mỗi đối tượng khác nhau ở {mối quan tâm, ngân sách thuật ngữ, độ sâu, hành động mong muốn}. Theo đối tượng mà quyết **giữ gì, trừu tượng hóa gì, đưa gì xuống phụ lục**. Chưa rõ đối tượng thì hỏi trước.

| Đối tượng | Mối quan tâm | Ngân sách thuật ngữ | Độ sâu | Cần gì |
|---|---|---|---|---|
| **Lãnh đạo/nhà tài trợ** | Kết quả, rủi ro, lịch, chi phí | Gần như 0 (viết đầy đủ từ viết tắt) | 1 trang | Đang ở đâu, đã quyết gì, rủi ro gì. Đề nghị ra quyết định |
| **PM phía khách hàng/các bên liên quan** | Tiến độ, đồng thuận, việc tiếp theo | Thấp (chỉ thuật ngữ chính, kèm giải thích trong ngoặc) | Tóm tắt + tiến độ | Mốc, quyết định đã thống nhất, việc chưa quyết, bước tiếp theo |
| **Lập trình viên mới/team khác** | Bối cảnh, cấu trúc, vì sao làm vậy | Trung bình | Tổng quan + bảng thuật ngữ | Tổng quan kiến trúc, lý do các quyết định chính, thuật ngữ |
| **Lập trình viên phía khách hàng** | Giao diện, ràng buộc, hợp đồng dữ liệu | Cao (thuật ngữ kỹ thuật được) | Một phần chi tiết | Đặc tả tích hợp, ràng buộc, hợp đồng dữ liệu. Căn cứ để tin về mặt kỹ thuật |

## Mức dịch (giảm dần từ lãnh đạo đến lập trình viên phía khách hàng)
- **Lãnh đạo**: "API p95 latency" → "độ trễ phản hồi màn hình". Số liệu thể hiện bằng % và màu trạng thái. Bảng kỹ thuật, code đưa hết xuống phụ lục.
- **PM phía khách hàng**: giữ thuật ngữ chính kèm giải thích ("SSO (đăng nhập một lần dùng nhiều dịch vụ)"). Trọng tâm là mốc và trạng thái.
- **Lập trình viên mới**: giữ thuật ngữ + bảng thuật ngữ. Có sơ đồ cấu trúc, bối cảnh quyết định.
- **Lập trình viên phía khách hàng**: giữ nguyên thuật ngữ, giao diện, ràng buộc. Phụ lục tối thiểu, đặc tả nằm trong thân bài.

## Quy tắc chung
- **Không tạo ra hiện trạng, số liệu, quyết định không có trong bản gốc.** Kể cả với lãnh đạo, bịa "tiến độ 70%" là sai. Chỉ ghi khi bản gốc có căn cứ.
- Thuật ngữ đối tượng không hiểu thì **không xóa mà dịch, giải thích trong ngoặc, hoặc đưa xuống phụ lục**. Giữ thông tin, chỉ đổi cách diễn đạt.
- Tài liệu cần hành động thì ghi rõ **"đọc xong tài liệu này cần làm gì"** (đề nghị quyết định, đề nghị xem xét, chỉ để thông tin).
- Xưng hô theo quan hệ với người đọc: gửi lãnh đạo, khách hàng dùng `chúng tôi` và `anh/chị` hoặc `Quý công ty`; nội bộ có thể dùng `team mình`. Theo quy ước sẵn có của tổ chức nếu có.
