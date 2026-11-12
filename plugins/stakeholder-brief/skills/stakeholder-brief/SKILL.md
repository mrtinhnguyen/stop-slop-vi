---
name: stakeholder-brief
description: Use when turning dev/project material (design doc, analysis, plan, status, root-cause report, tool/skill docs) into a Vietnamese document for a specific audience such as executives, customer PMs, internal staff or other teams, or customer engineers. Leads document requests that name an audience, and stop-slop-vi runs last as the tone pass. Triggers include /stakeholder-brief, "tóm tắt cho lãnh đạo", "làm tài liệu cho khách hàng", "viết tài liệu giới thiệu để chia sẻ nội bộ", "bản brief cho PM". Outputs HTML, DOCX, or MD.
---

# stakeholder-brief

Bộ khung biến tư liệu phát triển (file `.md`, tài liệu thiết kế, phân tích, file công cụ/skill) thành **tài liệu chia sẻ theo tầm đọc của một đối tượng cụ thể** (HTML/DOCX/MD). Phần khó không phải dựng file mà là **dựng lại theo tầm đọc của đối tượng và sắp xếp lại theo loại tài liệu**.

**Thứ tự skill:** yêu cầu có đối tượng đọc cụ thể thì skill này dựng đối tượng và cấu trúc trước, `stop-slop-vi` chỉ là lượt chỉnh giọng cuối. Chỉnh câu trước rồi dựng cấu trúc sau thì câu đã chỉnh lại bị xáo trộn.

## Nguyên tắc lõi (vi phạm là hỏng tài liệu)
- **Sự thật, số liệu, quyết định chỉ lấy từ bản gốc.** **Không bịa** tiến độ, lịch, số liệu, quyết định không có trong bản gốc. Không có thì ghi "chưa xác định / cần xác nhận".
- **Trừu tượng hóa kỹ thuật nhưng không bóp méo.** Phần kỹ thuật sâu không xóa mà **đưa xuống phụ lục / thu gọn**.
- **Mỗi lần một đối tượng.** Đổi đối tượng thì chạy lại (không nhồi nhiều đối tượng vào một tài liệu).

## Quy trình
1. **Chốt đầu vào và đối tượng**: bản gốc (một file .md hoặc nhóm file liên quan) + đối tượng đọc. Chưa có đối tượng thì hỏi trước.
2. **Chọn loại tài liệu**: chia sẻ tiến độ, đồng thuận thì dùng **kiểu đồng thuận** (`references/consensus-spine.md`); giới thiệu công cụ, quy trình, tính năng thì dùng **kiểu hướng dẫn** (`references/guide-spine.md`).
3. **Lăng kính đối tượng**: áp {mối quan tâm, ngân sách thuật ngữ, độ sâu, hành động mong muốn} theo `references/audience-personas.md`
4. **Dựng lại**: xếp nội dung gốc vào khung đã chọn + dịch thuật ngữ + rút "vậy thì sao" + truy nguồn (vị trí trong bản gốc)
5. **Xuất file**: HTML → `references/render-html.md` / DOCX → `references/render-docx.md` / MD → mục "Xuất MD" bên dưới
6. **Chỉnh giọng**: dùng skill `stop-slop-vi` rồi quét bằng `slop_scan.py`
7. **Kiểm tra**: đối chiếu số liệu, quyết định với bản gốc, kiểm tra tầm đọc, **tự soát "không có tiến độ bịa"**

## Khung tài liệu đồng thuận (mặc định)
1. **Tóm tắt 1 trang** (3 dòng cho lãnh đạo: đang ở đâu, đã quyết gì, rủi ro chính)
2. Bối cảnh, mục tiêu
3. **Tiến độ** (mốc, %, trạng thái)
4. **Quyết định đã thống nhất**
5. Chưa quyết / rủi ro
6. Bước tiếp theo, lịch
7. Phụ lục (chi tiết kỹ thuật, thuật ngữ)

Kiểu hướng dẫn (giới thiệu công cụ, quy trình) theo `references/guide-spine.md`: tổng quan nhanh → vì sao cần → làm được gì → cài đặt, áp dụng → ví dụ sử dụng → lưu ý, giới hạn → xử lý sự cố → phụ lục.

## Đối tượng (mỗi lần một)
Lãnh đạo/nhà tài trợ, PM phía khách hàng/các bên liên quan, lập trình viên mới hoặc team khác, lập trình viên phía khách hàng. Hồ sơ và mức dịch thuật ngữ ở `audience-personas.md`.

## Đầu ra
- **HTML**: một file tự chứa (màu trạng thái, thanh tiến độ, phụ lục thu gọn bằng `<details>`). Chia sẻ nhanh.
- **DOCX**: python-docx. Tài liệu chính thức, bàn giao.
- **MD**: chia sẻ qua repo, wiki, chat nội bộ. Xem "Xuất MD".
- (Cần PPTX thì bổ sung sau, hiện ngoài phạm vi)

### Xuất MD
- Theo GFM: tiêu đề đánh số (`## 1.`), mục lục ở đầu (liên kết neo), `---` giữa các mục, bảng và khối code. Cùng thư mục đã có hướng dẫn khác thì theo bố cục đó.
- Trạng thái ghi bằng chữ (`Xong`, `Đang làm`, `Chậm`, `Chưa xác định`), không dùng emoji. Không emoji trang trí, không ★.
- Phụ lục đặt thành mục `## Phụ lục` cuối tài liệu thay cho `<details>` của HTML.
- Lệnh, đường dẫn, cấu hình luôn để trong khối code. Chỉ đưa lệnh đã chạy thử, chưa chạy thì ghi "chưa kiểm chứng".
- Vị trí lưu, tên file theo quy ước tài liệu của người dùng (bắt đầu bằng chủ đề, không đưa ngày, phiên bản vào tên file).

## Lỗi hay gặp
- Chỉnh câu bằng stop-slop-vi trước rồi mới dựng cấu trúc → **thứ tự: dựng lại bằng skill này trước, stop-slop-vi sau cùng**
- Nhét khung đồng thuận (tiến độ, quyết định) vào tài liệu hướng dẫn → chọn loại tài liệu trước
- Bịa tiến độ, lịch, quyết định nghe hợp lý → **cấm**, ghi "chưa xác định"
- Cắt kỹ thuật quá tay nên sai → đưa xuống phụ lục nhưng giữ sự thật
- Nhiều đối tượng trong một tài liệu → mất trọng tâm. Mỗi lần một đối tượng
- Giọng máy móc → cuối cùng chạy `stop-slop-vi`
- Khẳng định "Xong" khi bản gốc không có căn cứ → chỉ ghi xong những gì bản gốc nói là xong
