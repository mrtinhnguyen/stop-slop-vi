# Khung tài liệu đồng thuận (sắp xếp lại)

File .md phát triển được viết theo thứ tự *độ sâu, độ chính xác*. Tài liệu cho các bên liên quan xếp lại theo thứ tự *kết luận → hiện trạng → đồng thuận → việc còn lại*. Mỗi mục quy định **lấy từ đâu trong bản gốc** và **không có thì ghi thế nào**.

## Cách viết từng mục
| # | Mục | Nội dung | Lấy từ bản gốc | Không có thì |
|---|---|---|---|---|
| 1 | **Tóm tắt 1 trang** | 3 dòng: đang ở đâu, đã quyết gì, rủi ro chính | Rút kết luận từ toàn bộ tài liệu | Luôn viết |
| 2 | Bối cảnh, mục tiêu | Vì sao làm, mục tiêu | Phần tổng quan, bối cảnh | Trích câu mục tiêu trong bản gốc |
| 3 | **Tiến độ** | Mốc, giai đoạn, %, trạng thái | Chỗ nói về tiến độ, trạng thái, hoàn thành | **"Chưa xác định"** (cấm bịa %) |
| 4 | **Quyết định đã thống nhất** | Việc đã chốt, đã thống nhất | Các cụm quyết định, chọn, chốt | Tách riêng thành "đang trao đổi" |
| 5 | Chưa quyết / rủi ro | Vấn đề mở, rủi ro, phụ thuộc | Vấn đề, rủi ro, TODO, giả định | Chỉ ghi những gì bản gốc có |
| 6 | Bước tiếp theo, lịch | Việc sắp tới, mốc | Kế hoạch, bước tiếp, lịch | "Chưa chốt lịch" |
| 7 | Phụ lục | Chi tiết kỹ thuật, thuật ngữ, bảng, căn cứ | Phần kỹ thuật còn lại | Đối tượng là lập trình viên thì đưa vào thân bài |

## Ghi trạng thái (mục tiến độ)
- 4 mức: Xong/ổn (xanh lá), Đang làm/cần chú ý (vàng), Chậm/có vấn đề (đỏ), Chưa bắt đầu/chưa xác định (xám). Chữ ghi bằng nhãn văn bản, màu chỉ thể hiện qua badge hoặc nền ô (emoji trạng thái bị `slop_scan.py` báo WARN)
- Phần trăm tiến độ **chỉ ghi khi bản gốc nêu rõ.** Không có thì ghi tên giai đoạn ("xong thiết kế / đang triển khai"). **Cấm ước lượng %.**
- Mốc thể hiện bằng bảng: Hạng mục | Trạng thái | Ghi chú

## Quy tắc tuyệt đối: không bịa
- Không tạo **tiến độ, ngày, quyết định, số liệu** không có trong bản gốc. Độ tin của tài liệu nằm ở đây.
- Chỉ ghi "Xong" cho việc bản gốc nói là xong. Mơ hồ thì ghi "Đang làm".
- Cần suy đoán thì không đưa vào thân bài mà ghi "cần xác nhận" để người dùng điền.

## Rút "vậy thì sao"
Mỗi nội dung kỹ thuật viết thêm một dòng "điều này có nghĩa gì với bên liên quan". Ví dụ: "Lưu kép Redis cache + PostgreSQL" → "dữ liệu hay xem được để ở kho truy xuất nhanh nên màn hình hiện nhanh hơn (cải thiện tốc độ phản hồi)".

## Truy nguồn
Tự kiểm tra từng mục tiến độ, quyết định lấy từ phần nào của bản gốc (phụ lục có thể ghi tên tài liệu nguồn). Dựng lại xong thì **đối chiếu số liệu, quyết định với bản gốc**.
