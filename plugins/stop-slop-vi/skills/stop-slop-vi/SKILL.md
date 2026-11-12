---
name: stop-slop-vi
description: Use when writing, generating, or editing Vietnamese documents meant for people (biên bản họp, báo cáo, tờ trình, công văn, đề xuất, kế hoạch, email, thông báo, hướng dẫn, pptx/xlsx/docx) or Vietnamese prose (tiểu luận, bài luận, bài thu hoạch, blog, bình luận, bài báo, thư xin việc) together with the docx/pptx/xlsx skills (for documents aimed at a named audience, stakeholder-brief leads and this skill runs last as the tone pass), when asked to remove "giọng AI"/văn dịch máy from Vietnamese text, or to match an existing document/author's tone (khớp giọng, thống nhất văn phong). Also matches requests typed without diacritics ("soan bao cao", "bo giong AI"). Triggers include /stop-slop-vi, "soạn biên bản họp", "làm báo cáo pptx", "bỏ giọng AI", "viết theo văn phong này", "viết tiểu luận", "sửa bài blog".
---

# stop-slop-vi

Bộ khung để viết tài liệu công việc và văn tự sự tiếng Việt như người viết ngay từ đầu (tạo mới), gỡ "giọng AI" khỏi bản đã có (làm sạch), hoặc khớp với văn phong tài liệu, tác giả khác (khớp giọng). Làm lại từ stop-slop bản tiếng Anh cho tiếng Việt.

**Nguyên tắc lõi:** giữ 100% nội dung, căn cứ, số liệu, thuật ngữ. **Chỉ sửa giọng, dấu câu, sáo ngữ.** Sửa xong luôn đối chiếu phạm vi thay đổi với bản gốc.

**Tự động áp dụng:** hook UserPromptSubmit trong plugin (`hooks/stop-slop-doc-reminder.py`) nhận ra yêu cầu viết, sửa tài liệu (từ khóa tài liệu + động từ viết, kể cả gõ không dấu) và nhắc dùng skill này. Có từ khóa đối tượng đọc (cho lãnh đạo, cho khách hàng, bản tóm tắt, tài liệu giới thiệu…) thì nhắc dùng stakeholder-brief trước (khi plugin đó đã cài). Yêu cầu văn tự sự (tiểu luận, blog, bình luận) thì nhắc văn phong tự sự và quét `--prose`. Người dùng nói "không dùng stop-slop", "giữ nguyên văn" thì hook im lặng.

**Thứ tự:** tài liệu chia sẻ có đối tượng đọc cụ thể (cho …, để chia sẻ, bản tóm tắt, tài liệu giới thiệu) thì `stakeholder-brief` dựng đối tượng và cấu trúc trước, skill này chỉ là **lượt chỉnh giọng cuối**. Tài liệu không cần dựng lại cho đối tượng (biên bản từ ghi âm, trả lời email, điền mẫu) thì chế độ tạo mới của skill này tự làm.

## Khi nào dùng
- **Tạo mới** biên bản, báo cáo, email, pptx/xlsx/docx → **chế độ tạo mới**
- Bản nháp đọc như "máy viết, máy dịch" cần sửa → **chế độ làm sạch**
- Cần khớp giọng với chương đồng nghiệp viết, tài liệu đã có → **chế độ khớp giọng**
- **Văn tự sự** (tiểu luận, bài luận, blog, bình luận, thư xin việc) cũng dùng ba chế độ trên → `references/prose-patterns.md`
- Đối tượng: tài liệu kỹ thuật tiếng Việt (MD, README, thiết kế, chú thích code), tài liệu gửi khách hàng (đề xuất, email, pptx), văn bản hành chính
- **Không dùng khi:** văn tiếng Anh (dùng stop-slop gốc), sửa logic code, viết lại sự thật, nội dung

## Cạm bẫy tiếng Việt (khác với stop-slop gốc)
**Gạch đầu dòng cụm danh từ, cụm động từ không chủ ngữ là văn phong bình thường** của báo cáo, biên bản. Văn bản hành chính có thể thức riêng (Nghị định 30/2020/NĐ-CP). Đổi những thứ này thành "câu chủ động, thẳng, ngắn" như stop-slop tiếng Anh thì **càng gượng**. Dấu hiệu AI thật của tiếng Việt là **dấu câu, văn dịch, sáo ngữ**, không phải kiểu câu. Quy tắc "cấm mở bằng từ để hỏi / cấm liệt kê ba ý / cấm not X but Y" của stop-slop gốc là cho tiểu luận tiếng Anh → **không áp cho danh sách yêu cầu, thông số tiếng Việt** (đó là nội dung).

**Chế độ làm sạch không bao giờ đổi xưng hô, tiểu từ cuối câu và thể thức hành chính.** `tôi / chúng tôi / em / mình`, `ạ / nhé`, `Kính gửi / Căn cứ / Đề nghị / Nơi nhận` là lựa chọn của người viết, không phải slop. Gạch đầu dòng không chủ ngữ cũng không ép thành câu đủ. Chỉ **chế độ khớp giọng** mới đổi những thứ này, theo chữ ký của tài liệu mẫu. Chế độ làm sạch sửa dấu câu, văn dịch, sáo ngữ, chữ thừa, không sửa cách xưng hô và kiểu câu.

| Tự bào chữa | Thực tế |
|---|---|
| "Gạch đầu dòng không chủ ngữ thì cụt" | Không. Đó là kiểu báo cáo chuẩn. Làm sạch thì **không đổi kiểu câu**. |
| "Đổi sang chủ động cho tự nhiên" | Chỉ đúng với `được … bởi`. Còn lại là áp sai stop-slop tiếng Anh. Tôn trọng văn phong người viết. |
| "Văn hành chính cứng quá, viết mềm lại" | Thể thức hành chính không phải slop. Chỉ sửa dấu câu, văn dịch trong phần nội dung. |
| "`em` nghe không chuyên nghiệp, đổi thành `tôi`" | Xưng hô do người viết chọn. Không đổi. |

## Chế độ tạo mới (write-time)
Mặc định khi viết tài liệu mới. Định dạng file do skill docx/pptx/xlsx (hoặc mẫu sẵn có + Excel COM) lo, câu chữ do skill này lo. Không viết sai từ đầu rẻ hơn sửa sau.
1. **Chọn văn phong trước.** Có mẫu sẵn hoặc tài liệu kỳ trước (biên bản tuần trước, tài liệu cùng loạt) thì theo văn phong đó (áp nhẹ `references/tone-extraction.md`). Không có thì mặc định: biên bản, báo cáo, bảng, slide = gạch đầu dòng ngắn; email, thông báo = câu đầy đủ, xưng `tôi/chúng tôi`; văn bản hành chính = theo thể thức Nghị định 30/2020. Viết thêm vào tài liệu có sẵn thì theo kiểu câu của tài liệu đó.
   - **Văn tự sự** (tiểu luận, bài luận, bài thu hoạch, blog, bình luận, bài báo, thư xin việc) viết thành đoạn. Đọc `references/prose-patterns.md` để chọn xưng hô.
   - "Báo cáo" vẫn là gạch đầu dòng. Chỉ viết thành đoạn khi người dùng nói rõ.
   - Văn tự sự cũng không bịa sự thật, số liệu, trích dẫn, nguồn. Thiếu thì ghi `[cần xác nhận: ...]`.
2. **Viết đúng quy tắc ngay từ bản nháp.** Không dùng dấu hiệu nhóm A, B trong `references/vi-slop-patterns.md` (em-dash, liệt kê bằng ` · `, ★ và emoji, ký hiệu toán, văn dịch, cách trước dấu câu, tiêu đề Title Case). Chuỗi ký tự trong script sinh file cũng theo chuẩn này. Ghi file UTF-8, dạng NFC.
3. **Giữ nguyên tư liệu gốc.** Số, tên, quyết định, mã yêu cầu trong ghi âm, tài liệu thiết kế, chuỗi email phải chuyển nguyên. Biên bản không bịa quyết định, thời hạn, người phụ trách không có trong lời nói (không có thì ghi "chưa xác định").
4. **Tạo file xong thì quét.** `python3 "${CLAUDE_SKILL_DIR}/scripts/slop_scan.py" <file>` (Windows dùng `python`). WARN thì sửa chuỗi gốc trong script sinh file rồi sinh lại (chỉ vá file nhị phân khi không có script). Thêm `--info` để xem mục INFO (cần người quyết). Văn tự sự thì chạy `--prose --info`.
5. **Báo cáo.** Ghi kết quả quét `PASS`/`FAIL` (số WARN). Không chạy thì ghi `NOT_RUN`.

## Chế độ làm sạch (de-slop)
1. Xác định tính chất tài liệu (kỹ thuật/khách hàng/hành chính, gạch đầu dòng/văn xuôi) → **tôn trọng văn phong sẵn có**. Văn tự sự thì đọc `references/prose-patterns.md` và quét `--prose`. Xưng hô không đổi kể cả với văn tự sự
2. Tìm và thay dấu hiệu theo `references/vi-slop-patterns.md`
3. Kiểm tra quy tắc giữ nguyên (số, căn cứ, quy ước bảng, thể thức hành chính)
4. File pptx thì sửa an toàn theo công thức `references/pptx-editing.md`

## Chế độ khớp giọng (tone-match)
1. Lấy mẫu chuẩn (tài liệu, chương cần khớp) từ bản gốc chưa sửa
2. Rút chữ ký văn phong theo `references/tone-extraction.md` (6 trục, thêm trục tự sự nếu mẫu là văn tự sự)
3. Viết lại theo từng thành phần (áp luôn quy tắc làm sạch), giữ nội dung

## Tra nhanh (dấu hiệu chính → cách sửa)
| Dấu hiệu | Sửa |
|---|---|
| em-dash `—` trong câu | ` – `, dấu phẩy, ngoặc, tách câu |
| Liệt kê bằng ` · ` | Dấu phẩy hoặc chấm phẩy |
| `★` trang trí, emoji, `÷ =` | Xóa, viết bằng lời |
| Cách trước dấu câu (`dự án , kế hoạch`) | Viết liền |
| Tiêu đề `Kế Hoạch Triển Khai Dự Án` | Viết hoa kiểu câu |
| Văn dịch (`được … bởi`, `có thể nói rằng`, `việc … việc`, `tiến hành + động từ`, `một cách + tính từ`) | Tiếng Việt tự nhiên |
| Danh từ hóa thừa, bộ ba đều nhịp, từ hô hào | Tách câu, đổi nhịp (nội dung thật có ba ý thì giữ) |
| Xưng hô, tiểu từ, thể thức hành chính, số liệu, căn cứ, trích dẫn | **Giữ nguyên** |

## Kiểm tra (bắt buộc)
Sau khi sửa, đối chiếu bản sao lưu để chắc **chỉ phạm vi cần sửa bị đổi**, rồi quét dấu hiệu còn sót. Chỉ báo "xong" khi có căn cứ (diff file, slide đã đổi).

Quét dấu hiệu còn sót bằng `scripts/slop_scan.py`.
```
python3 "${CLAUDE_SKILL_DIR}/scripts/slop_scan.py" FILE... [--info] [--prose] [--out report.txt]
```
- Windows không có `python3` hoặc chỉ hiện gợi ý Microsoft Store thì chạy `python`
- Hỗ trợ: docx (thân, bảng, header, chú thích), pptx (theo thứ tự slide, bảng), xlsx (ô, hình), md, txt, html
- exit 0 = PASS (không có WARN), 1 = FAIL, 2 = lỗi đầu vào. Bỏ qua đoạn không có chữ tiếng Việt có dấu, ô bảng chỉ có `—`, khối code md. Văn bản gõ hoàn toàn không dấu sẽ không được quét
- WARN: em-dash, ★, emoji trang trí, ÷, liệt kê ` · ` từ hai lần, cách đôi quanh dấu phân cách, cách trước dấu câu, tiêu đề Title Case (md), dấu tổ hợp NFD, văn dịch `được … bởi`, `có thể nói/thấy (rằng)`, `việc … việc`
- INFO: một dấu ` · `, thiếu cách sau dấu phẩy, `tiến hành + động từ`, `đóng vai trò`, `là một trong những … nhất`, `đối với/trong việc`, `nhằm mục đích`, `một cách + tính từ` và `thông qua` dày đặc, lẫn ngoặc cong/thẳng, lẫn `…`/`...`, lẫn kiểu bỏ dấu `hòa`/`hoà`, nhiều dòng `**Nhãn:**`
- `--prose` (văn tự sự): INFO cho kết bằng bài học, "không chỉ là … mà còn", mở bằng danh ngôn/định nghĩa, từ nhấn rỗng, sáo ngữ tiểu luận/blog. WARN toàn văn bản khi "tôi cho rằng" (nghĩ rằng, tin rằng, theo tôi) từ 3 lần và ít nhất 1 lần mỗi 2.500 ký tự, hoặc từ 3 đoạn mở bằng liên từ và chiếm từ 25% số đoạn. Không có `--prose` thì tắt các quy tắc này
- Console Windows in lỗi chữ có dấu thì dùng `--out` rồi đọc file
- Sáo ngữ, danh từ hóa, bộ ba đều nhịp scanner không bắt được. PASS rồi vẫn đọc lại một lượt

## Lỗi hay gặp
- Báo "đã làm sạch" ở chế độ tạo mới mà không quét → kèm kết quả `slop_scan.py` làm căn cứ
- Đổi gạch đầu dòng thành câu chủ động đầy đủ nên càng gượng → xem "Cạm bẫy tiếng Việt"
- Làm sạch văn tự sự mà đổi `mình` thành `tôi`, hoặc bịa việc làm, sự thật để sửa câu kết bài học → không đổi xưng hô, không có thì xóa hoặc hỏi
- "Làm mềm" thể thức hành chính (`Kính gửi`, `Căn cứ`, `Nơi nhận`) → giữ nguyên
- Làm hỏng số, mã yêu cầu, trích dẫn khi "dọn dẹp" → chốt danh sách cần giữ trước
- Thay cả đoạn pptx nên mất định dạng → dùng công thức giữ `run[0]`
- Không sao lưu bản gốc → không hoàn tác được. Luôn sao lưu trước
