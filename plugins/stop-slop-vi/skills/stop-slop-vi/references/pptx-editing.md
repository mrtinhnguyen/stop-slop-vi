# Công thức sửa pptx an toàn (python-pptx)

Thay chữ trong PowerPoint mà **giữ nguyên định dạng**. Xử lý được bảng, nhóm hình và đoạn nhiều run. (Cần python-pptx: `pip install python-pptx`)

## Nguyên tắc
1. **Sao lưu bản gốc trước**: `shutil.copyfile(src, bak)`.
2. **Tìm đoạn bằng needle (chuỗi con duy nhất)**: số slide khác nhau giữa các file (bản gộp slide 14–17, bản lẻ slide 4–7) vẫn dùng lại được cùng quy tắc.
3. **Giữ định dạng `run[0]`**: đặt chữ mới vào run đầu của đoạn, các run còn lại gán `""`. Đoạn bị chia thành nhiều run vẫn giữ định dạng.
4. **Danh sách slide được phép sửa**: chặn hẳn các slide ngoài phạm vi (tránh làm hỏng slide khác).
5. Needle khớp **từ 2 chỗ trở lên hoặc 0 chỗ** thì bỏ qua và cảnh báo. Khi trùng, thêm cụm riêng vào needle (ví dụ có cả em-dash: `chức năng đặt trước — yêu cầu số 12`).
6. **Kiểm tra**: so với bản sao lưu để chắc chỉ slide cần sửa bị đổi, rồi quét lại dấu hiệu còn sót theo đoạn.

## Mẫu dùng lại
```python
# -*- coding: utf-8 -*-
import re, shutil
from pptx import Presentation

SRC = r"...deck.pptx"; BAK = SRC.replace(".pptx","_ORIG-backup.pptx")
ALLOWED = {14,15,16,17}          # slide được sửa, đánh số từ 1
EDITS = [                         # (needle chuỗi con duy nhất, toàn bộ đoạn mới)
    ("Đảm bảo tính nhất quán", "Thống nhất trước câu hướng dẫn, vị trí nút, cách viết thuật ngữ cho từng màn hình"),
    # ...
]

def norm(s): return re.sub(r"\s+"," ",s).strip()
def iter_paras(shapes):
    for sh in shapes:
        if sh.shape_type == 6:                     # GROUP: đệ quy
            yield from iter_paras(sh.shapes); continue
        if sh.has_text_frame:
            for p in sh.text_frame.paragraphs: yield p
        if sh.has_table:
            for row in sh.table.rows:
                for cell in row.cells:
                    for p in cell.text_frame.paragraphs: yield p
def set_para(p, new):                              # giữ định dạng run[0]
    if not p.runs: return False
    p.runs[0].text = new
    for r in p.runs[1:]: r.text = ""
    return True

shutil.copyfile(SRC, BAK)                          # 1. sao lưu
prs = Presentation(BAK); slides = list(prs.slides) # đọc từ bản sao lưu (bản gốc), lưu vào file đang dùng
issues=[]; ok=0
for needle, new in EDITS:
    m=[p for i,sl in enumerate(slides,1) if i in ALLOWED
         for p in iter_paras(sl.shapes) if norm(needle) in norm(p.text)]
    if len(m)==1: set_para(m[0], new); ok+=1
    else: issues.append((needle, len(m)))          # 0 = gõ sai, >1 = trùng
prs.save(SRC)
print(f"applied={ok}/{len(EDITS)} issues={issues}")
```

## Đoạn mã kiểm tra
```python
# Cô lập phạm vi thay đổi: slide nào khác bản sao lưu
def stext(sl):
    t=[]
    def w(shs):
        for sh in shs:
            if sh.shape_type==6: w(sh.shapes); continue
            if sh.has_text_frame and sh.text_frame.text.strip(): t.append(sh.text_frame.text)
            if sh.has_table:
                for r in sh.table.rows: t.append(" | ".join(c.text for c in r.cells))
    w(sl.shapes); return "\n".join(t)
L=list(Presentation(SRC).slides); B=list(Presentation(BAK).slides)
print("changed:", [i+1 for i in range(len(L)) if stext(L[i])!=stext(B[i])])  # phải trùng với ALLOWED
```

## Cạm bẫy
- **Console Windows không phải UTF-8**: in chữ có dấu, ký tự đặc biệt bị lỗi. Ghi ra file UTF-8 rồi đọc bằng công cụ Read.
- Đoạn **nhiều run**: kiểm tra định dạng đồng nhất rồi mới gộp (khác in đậm, màu thì xử lý từng run). Chữ mới nhận màu, cỡ, font của `run[0]`.
- Ghép ô bảng bằng `" | "` rồi quét sẽ **báo nhầm** ` · ` và ` — `: quét lại theo từng đoạn.
- **Lưu lại bằng python-pptx là tuần tự hóa lại XML**: mỗi part lệch ±1 byte, **không mất part nào**. File nhỏ đi chỉ do khác tỷ lệ nén. Bố cục và vị trí hình nên **mở PowerPoint xem bằng mắt** (chương trình chỉ kiểm được chữ).
- `—` trong ô bảng (nghĩa là không áp dụng) không phải slop: đừng để needle khớp vào.
