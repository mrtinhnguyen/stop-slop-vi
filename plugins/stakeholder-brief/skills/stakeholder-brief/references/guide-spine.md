# Khung tài liệu hướng dẫn (giới thiệu công cụ, quy trình, tính năng)

Kiểu đồng thuận nói "đã đi đến đâu, đã quyết gì", còn kiểu hướng dẫn nói "đây là gì, dùng thế nào". Thuộc loại này: giới thiệu công cụ nội bộ, hướng dẫn cài đặt, áp dụng, quy trình vận hành. Lăng kính đối tượng (`audience-personas.md`) áp dụng như cũ.

## Cách viết từng mục
| # | Mục | Nội dung | Lấy từ bản gốc | Không có thì |
|---|---|---|---|---|
| 1 | **Tổng quan nhanh** | Định nghĩa một dòng, người đọc, luồng chính | Phần tổng quan, description | Luôn viết |
| 2 | Vì sao cần | Vấn đề cần giải quyết, trước và sau khi dùng | Bối cảnh, lý do, ví dụ thực tế | Trích câu mục tiêu trong bản gốc |
| 3 | **Làm được gì** | Tính năng, chế độ, quy tắc dạng bảng | Thân skill/công cụ | Chỉ ghi những gì bản gốc có |
| 4 | **Cài đặt, áp dụng** | Yêu cầu trước, các bước cài, kiểm tra cài xong | File cấu hình, script | Ghi "chưa kiểm chứng" |
| 5 | Ví dụ sử dụng | Đầu vào theo tình huống và kết quả | Ghi chép dùng thực tế | Nói rõ là ví dụ, giữ tối thiểu |
| 6 | Lưu ý, giới hạn | Việc không làm được, khả năng đánh giá sai | Ràng buộc, lỗi hay gặp | Không viết "không có giới hạn đã biết" |
| 7 | Xử lý sự cố | Triệu chứng → nguyên nhân → cách xử lý | Ghi chép cạm bẫy, sự cố | Có thể bỏ |
| 8 | Phụ lục | Cấu trúc file, thuật ngữ, quy tắc chi tiết | Phần còn lại | Đối tượng là lập trình viên thì đưa vào thân bài |

## Quy tắc
- Lệnh cài đặt **chỉ đưa lệnh đã chạy thử lúc viết**. Chưa chạy thì ghi "chưa kiểm chứng" cạnh lệnh.
- Số liệu hiệu quả (ví dụ "30 WARN → 0 WARN") chỉ ghi khi có số đo thật. Không bịa hiệu quả triển khai, tỷ lệ sử dụng.
- Prompt ví dụ ngắn gọn. Không phóng đại kết quả.
- Khi lẫn loại tài liệu (giới thiệu công cụ + đề nghị đồng thuận triển khai) thì thân bài theo kiểu hướng dẫn, đề nghị đồng thuận đặt một dòng ở "Tổng quan nhanh".
