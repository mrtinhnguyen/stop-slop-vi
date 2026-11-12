# Dấu hiệu AI trong tài liệu tiếng Việt và cách sửa

Quy tắc của stop-slop (bản tiếng Anh) làm lại cho tài liệu công việc tiếng Việt. **Giữ nội dung, sự thật, số liệu, căn cứ, thuật ngữ.** Chỉ sửa dấu câu, văn dịch, sáo ngữ. Trước khi sửa, xác định văn phong sẵn có của tài liệu (gạch đầu dòng, câu hành chính, thư từ) và **tôn trọng** nó.

## A. Dấu câu và chính tả

| Dấu hiệu | Vấn đề | Sửa |
|---|---|---|
| `—` (em-dash) chen giữa câu | Thói quen tiếng Anh của model. Văn Việt dùng ` – ` có cách hoặc dấu phẩy | ` – `, dấu phẩy, ngoặc đơn, hoặc tách câu |
| ` · ` làm dấu phân cách liệt kê | Tiếng Việt không liệt kê bằng dấu chấm giữa | Dấu phẩy `,` hoặc chấm phẩy `;` |
| Cách đôi `  ·  ` | Dấu vết sinh tự động | Một dấu phân cách |
| `★`, emoji trang trí (✅ 🚀 ✨) | Nhấn mạnh kiểu AI | Xóa (nhấn mạnh bằng in đậm, màu) |
| `÷ = ×` chen trong câu | Dấu vết máy | Viết bằng lời ("chia cho", "bằng", "nhân") |
| Cách trước dấu câu (`dự án , kế hoạch`, `xong .`, `gì ?`) | Dấu vết ghép chuỗi | Viết liền dấu câu với chữ trước |
| Thiếu cách sau dấu phẩy (`dự án,kế hoạch`) | Dấu vết ghép chuỗi | Thêm một khoảng trắng. Không áp cho số thập phân `3,5` |
| Tiêu đề viết hoa mọi chữ đầu (`Kế Hoạch Triển Khai Dự Án`) | Dịch từ Title Case tiếng Anh | Viết hoa kiểu câu: `Kế hoạch triển khai dự án`. Giữ hoa tên riêng |
| Lẫn ngoặc cong `“ ”` và ngoặc thẳng `"` | Thiếu nhất quán | **Theo quy ước sẵn có của tài liệu** |
| Lẫn `…` và `...` | Thiếu nhất quán | Chọn một kiểu |
| Lẫn hai kiểu bỏ dấu (`hòa`/`hoà`, `khỏe`/`khoẻ`, `thúy`/`thuý`) | Ghép nhiều nguồn | Theo kiểu chiếm đa số trong tài liệu. Cả hai kiểu đều đúng (`hoà` theo QĐ 240/1984, `hòa` theo lối truyền thống), chỉ cần nhất quán |
| Dấu tổ hợp (NFD) | Dán từ macOS hoặc pipeline máy, làm hỏng tìm kiếm | Chuẩn hóa về NFC |
| Quá nhiều dòng `**Nhãn:** nội dung` | Định dạng kiểu chatbot | Viết thành câu, bảng, hoặc tiêu đề nhỏ |

` – ` (en-dash có cách) là dấu gạch ngang chuẩn trong văn bản tiếng Việt, **không phải** dấu hiệu AI. `→` chỉ dùng cho luồng trong sơ đồ, bảng. `*` và `-` cho chú thích là bình thường.

## B. Từ ngữ và câu (văn dịch, sáo ngữ)

### Văn dịch từ tiếng Anh

| Mẫu | Sửa |
|---|---|
| `được … bởi` (`được phát triển bởi nhóm A`) | Đưa tác nhân lên làm chủ ngữ: `nhóm A phát triển` |
| `có thể nói (rằng)`, `có thể thấy (rằng)` ở đầu câu | Khẳng định thẳng |
| `việc … việc` (`việc thực hiện việc triển khai`) | Bỏ chữ `việc` thừa: `triển khai` |
| `tiến hành + động từ` (`tiến hành kiểm tra`) | Dùng động từ luôn: `kiểm tra` |
| `một cách + tính từ` dày đặc (`một cách hiệu quả`) | `hiệu quả`, hoặc bỏ |
| `đóng (một) vai trò quan trọng/then chốt` | Nói nó làm việc gì |
| `là một trong những … nhất` | Nói thẳng, hoặc dẫn số liệu có trong nguồn |
| `thông qua` dày đặc | `qua`, `bằng`, `nhờ` (giữ khi nghĩa là "phê duyệt") |
| `đối với việc`, `trong việc` | Bỏ hoặc đổi chủ ngữ |
| `nhằm mục đích` | `để` |
| `các/những` trước mọi danh từ | Bỏ khi số nhiều đã rõ |
| `của` nối chuỗi (`kết quả của việc đánh giá của nhóm`) | Viết lại cho gọn |

Không phải mọi câu bị động đều sai. `được phê duyệt`, `được bổ nhiệm` là bình thường. Chỉ `được … bởi` có tác nhân mới là dấu vết dịch.

### Sáo ngữ và từ hô hào
- **Danh từ hóa thừa:** `thực hiện công tác`, `triển khai thực hiện`, `đẩy mạnh việc` → nói việc cụ thể.
- **Từ hô hào:** `nâng tầm`, `kiến tạo`, `hệ sinh thái`, `giải pháp toàn diện`, `tối ưu hóa trải nghiệm`, `chuyển đổi số toàn diện` → nếu nguồn không có việc làm cụ thể thì xóa, có thì nói việc đó.
- **Câu dẫn đường:** `Đáng chú ý là`, `Cần nhấn mạnh rằng`, `Không thể phủ nhận rằng` → xóa, vào thẳng nội dung.
- **Bộ ba đều nhịp** ("A thì …, B thì …, C thì …"): nhịp máy → tách câu hoặc đổi nhịp. **Nếu nội dung thật sự có ba yếu tố thì giữ** (nội dung không phải slop).
- **Quy tắc stop-slop tiếng Anh không áp cho tiếng Việt:** cấm mở câu bằng từ để hỏi, cấm liệt kê ba ý, cấm "not X but Y". Danh sách yêu cầu, thông số là nội dung.

## C. Văn phong và xưng hô

**Chế độ làm sạch không đổi xưng hô, tiểu từ cuối câu và văn phong hành chính.** Phần dưới để quan sát, không để chuyển đổi. Chỉ chế độ khớp giọng mới đổi những thứ này, theo tài liệu mẫu.

- **Gạch đầu dòng danh từ** (`- Hoàn thành kiểm thử module A`) là bình thường trong báo cáo, biên bản. Không ép thành câu đủ chủ vị.
- **Văn bản hành chính** (công văn, tờ trình, báo cáo theo Nghị định 30/2020/NĐ-CP): `Căn cứ`, `Kính gửi`, `Đề nghị`, `Nơi nhận`, `Trân trọng` là thể thức, không phải sáo ngữ. Không "làm tự nhiên" phần này.
- **Xưng hô** (`tôi`, `chúng tôi`, `em`, `anh/chị`, `quý khách`) và **tiểu từ** (`ạ`, `nhé`, `nha`) là lựa chọn của người viết. Không đổi `em` thành `tôi` hay bỏ `ạ`.
- **Thư từ, email**: giữ lời chào và lời kết của người viết. Chỉ sửa dấu câu, văn dịch.

### Dấu hiệu cảnh báo, gặp thì dừng lại
- "Câu này cứng quá, đổi `chúng tôi` thành `mình` cho thân thiện" → không đổi xưng hô.
- "Câu chủ động hay hơn" → chỉ đúng với `được … bởi`. Bị động không tác nhân thì giữ.
- "Gạch đầu dòng toàn danh từ, khô quá" → khô không phải slop.

## D. Luôn giữ nguyên
- Số và đơn vị (3.000 cuốn, 8 GB, 95%), số hiệu văn bản và yêu cầu (Số 12/QĐ-UBND, mục 3.2, tr. 20), lời trích nguyên văn.
- Thuật ngữ, tên sản phẩm (React, PostgreSQL, Docker, Redis), tên riêng, tên cơ quan.
- Ký hiệu `—` hoặc `-` trong ô bảng nghĩa là "không áp dụng", một dấu ` · ` phân cách hai thuộc tính (`Hà Nội · 11/2026`), mũi tên luồng `→`.
- Thể thức văn bản hành chính: quốc hiệu, tiêu ngữ, số ký hiệu, nơi nhận, chữ ký.
