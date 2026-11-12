# Kịch bản kiểm thử văn tự sự

Đưa cho subagent đường dẫn SKILL.md và references của stop-slop-vi, tạo file chuẩn bị trong một thư mục tạm trống rồi gửi câu yêu cầu. Phải đạt mọi tiêu chí mới là PASS.

## 1. Làm sạch bài blog

Chuẩn bị: `blog.md`

```markdown
# Ghi chú về Docker volume

Hôm nay chúng ta cùng tìm hiểu về Docker volume. Đây là phần thực sự khiến rất nhiều bạn bối rối.

Khi xóa container, các file ghi bên trong container cũng mất theo. Volume lưu dữ liệu này ra ngoài container.

Bạn tạo volume bằng `docker volume create mydata` rồi gắn vào bằng `-v mydata:/var/lib/mysql`. Trong thử nghiệm của mình, xóa đi tạo lại container MySQL 3 lần mà 12 bảng vẫn còn nguyên.

Hy vọng bài viết hữu ích với bạn. Đừng quên chia sẻ nếu thấy hay nhé!
```

Câu yêu cầu: "bỏ giọng AI trong blog.md"

Tiêu chí:
- Giữ nguyên xưng hô `bạn`/`mình` (không đổi thành `tôi`)
- Bỏ sáo ngữ blog: "Hôm nay chúng ta cùng tìm hiểu", "thực sự", "Hy vọng bài viết hữu ích", "Đừng quên chia sẻ"
- Giữ nguyên câu sự thật, số (3 lần, 12 bảng) và lệnh
- Chạy `slop_scan.py --prose` và báo kết quả (PASS/FAIL)

## 2. Làm sạch tiểu luận

Chuẩn bị: `report.md`

```markdown
# Ảnh hưởng của làm việc từ xa đến cộng tác trong nhóm

Làm việc từ xa không chỉ là một hình thức làm việc mà còn là sự chuyển đổi tư duy. Bài viết này sẽ tìm hiểu một năm làm việc từ xa của nhóm tôi.

Nhóm tôi bắt đầu làm việc từ xa 3 ngày mỗi tuần từ tháng 3 năm 2025. Nhóm có 8 người, 5 người sống ngoài Hà Nội. Thời gian đi lại trung bình giảm từ 2 giờ khứ hồi xuống 0. Tôi cho rằng đây là thay đổi lớn nhất.

Bên cạnh đó, cách họp cũng thay đổi. Họp trực tiếp 5 buổi mỗi tuần giảm còn 2 buổi họp trực tuyến, phần còn lại chia sẻ bằng văn bản. Tỷ lệ cuộc họp có biên bản tăng từ 30% lên 90%. Tôi nghĩ rằng nhờ có ghi chép nên quyết định ít bị đảo ngược hơn.

Ngoài ra, cũng có vấn đề. 2 nhân viên mới cho biết trong 3 tháng đầu họ khó tìm người để hỏi. Khi tin nhắn được trả lời chậm, công việc bị dừng. Tôi cho rằng nên tăng số ngày lên văn phòng cho nhân viên mới.

Tóm lại, làm việc từ xa hiệu quả về đi lại và ghi chép, nhưng yếu ở khâu hòa nhập người mới. Tôi tin rằng mô hình kết hợp là lời giải. Qua trải nghiệm này, tôi nhận ra tầm quan trọng của giao tiếp.
```

Câu yêu cầu: "sửa report.md cho gọn"

Tiêu chí:
- Giữ nguyên xưng hô `tôi`, `nhóm tôi`
- Sau khi sửa, `slop_scan.py --prose` không còn WARN PROSE_THINK, PROSE_CONNECTOR
- Giữ nguyên các số (tháng 3 năm 2025, 3 ngày, 8 người, 5 người, 2 giờ, 5 buổi, 2 buổi, 30%, 90%, 2 nhân viên, 3 tháng)
- Không thêm sự thật, số liệu, nguồn, việc làm không có trong bản gốc
- Báo kết quả quét (PASS/FAIL)

## Ghi kết quả

| Ngày | Kịch bản | Kết quả | Ghi chú |
|---|---|---|---|
| | 1 Làm sạch blog | Chưa chạy | |
| | 2 Làm sạch tiểu luận | Chưa chạy | |
