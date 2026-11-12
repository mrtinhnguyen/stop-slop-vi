# Xuất DOCX (python-docx)

Dùng cho tài liệu chính thức, bàn giao. Tiêu đề, bảng, gạch đầu dòng theo thứ tự khung. (`pip install python-docx`)

## Nguyên tắc
- Tổ chức có mẫu riêng thì ưu tiên **mở file DOCX mẫu có sẵn rồi điền** (giữ style). Không có thì tạo mới như dưới.
- Font: tài liệu gửi cơ quan nhà nước theo Nghị định 30/2020/NĐ-CP dùng Times New Roman cỡ 13–14. Tài liệu kỹ thuật, nội bộ có thể dùng Arial hoặc Calibri cỡ 11. Theo mẫu của tổ chức nếu có.
- Trạng thái ghi bằng nhãn chữ (Xong/Đang làm/Chậm/Chưa xác định) kèm nền ô hoặc màu chữ. Không dùng emoji trạng thái. Không định dạng thừa.
- Kết hợp bảng (tiến độ, mốc) với gạch đầu dòng (quyết định, rủi ro, bước tiếp). Phụ lục là mục cuối (phân biệt bằng style tiêu đề).
- Số liệu, quyết định theo căn cứ bản gốc. Cấm bịa (quy tắc ở consensus-spine.md).

## Mẫu tạo mới
```python
# -*- coding: utf-8 -*-
from docx import Document
from docx.shared import Pt, RGBColor

doc = Document()
# Font mặc định (tài liệu nội bộ; văn bản hành chính đổi sang 'Times New Roman', Pt(13))
doc.styles['Normal'].font.name = 'Arial'
doc.styles['Normal'].font.size = Pt(11)

def h(text, level=1):
    return doc.add_heading(text, level=level)

doc.add_heading('{Tiêu đề}', 0)
sub = doc.add_paragraph('{Dự án} | {Đối tượng đọc} | {Ngày}')
sub.runs[0].font.color.rgb = RGBColor(0x8a, 0x8f, 0x98)

h('Tóm tắt', 1)
for line in ['{Đang ở đâu}', '{Đã quyết gì}', '{Rủi ro chính}']:
    doc.add_paragraph(line, style='List Bullet')

h('Bối cảnh, mục tiêu', 1); doc.add_paragraph('{...}')

h('Tiến độ', 1)
rows = [('Hạng mục', 'Trạng thái', 'Ghi chú'),
        ('{Mốc}', 'Xong', '{...}'),
        ('{...}', 'Đang làm', '{...}')]
t = doc.add_table(rows=0, cols=3); t.style = 'Light Grid Accent 1'
for r in rows:
    cells = t.add_row().cells
    for i, v in enumerate(r):
        cells[i].text = v

for title, items in [('Quyết định đã thống nhất', ['{...}']),
                     ('Chưa quyết, rủi ro', ['{...}']),
                     ('Bước tiếp theo', ['{...}'])]:
    h(title, 1)
    for it in items:
        doc.add_paragraph(it, style='List Bullet')

h('Phụ lục: chi tiết kỹ thuật, thuật ngữ', 1)
doc.add_paragraph('{Đối tượng không phải lập trình viên thì đưa phần kỹ thuật xuống đây}')

doc.save(r'{đường dẫn đầu ra}.docx')
```

## Điền mẫu có sẵn
- Mở bằng `Document(template_path)`, tìm đoạn/bảng giữ chỗ rồi chỉ thay chữ (giữ style).
- Mẫu phức tạp, python-docx làm vỡ style thì mở và điền bằng Word COM (Windows).

## Hoàn tất
- Lưu xong nên mở bằng Word một lần để xem bảng, định dạng.
- Giọng văn thân bài chỉnh bằng `stop-slop-vi`.
