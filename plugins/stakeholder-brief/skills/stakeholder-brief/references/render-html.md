# Xuất HTML

Một file HTML tự chứa (không phụ thuộc bên ngoài). Thẻ theo thứ tự khung + màu trạng thái + thanh tiến độ + phụ lục thu gọn bằng `<details>`. Dùng để chia sẻ nhanh (mở bằng trình duyệt hoặc gửi luôn file).

## Nguyên tắc
- **Chỉ CSS nội tuyến** (không CDN, không link font ngoài, để mở được cả trong mạng nội bộ, ngoại tuyến). Dùng font hệ thống.
- Tối ưu để lướt: tóm tắt 1 trang là thẻ lớn trên cùng, tiến độ dạng bảng, phụ lục thu gọn mặc định.
- Màu chỉ dùng cho trạng thái, dùng tiết chế (xong = xanh lá, đang làm = vàng, chậm = đỏ, chưa xác định = xám). Không gradient lòe loẹt, không rải emoji (dấu vết AI).
- Có ít nhất một dòng `@media print` cho bản in.

## Khung (điền vào để dùng)
```html
<!doctype html><html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{Tiêu đề}</title>
<style>
:root{--g:#1f9d55;--y:#c98a00;--r:#c0392b;--w:#8a8f98;--ink:#1a1a1a;--line:#e5e7eb;--bg:#fafafa}
*{box-sizing:border-box}body{margin:0;font-family:system-ui,'Segoe UI',Roboto,Arial,sans-serif;color:var(--ink);background:var(--bg);line-height:1.6}
.wrap{max-width:900px;margin:0 auto;padding:32px 24px}
h1{font-size:22px;margin:0 0 4px}.sub{color:var(--w);font-size:13px;margin-bottom:24px}
.card{background:#fff;border:1px solid var(--line);border-radius:10px;padding:18px 20px;margin:14px 0}
.summary{border-left:4px solid var(--g);background:#fff}
h2{font-size:15px;margin:0 0 10px;color:#111}
table{width:100%;border-collapse:collapse;font-size:13px}th,td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top}
th{color:var(--w);font-weight:600;background:#f6f7f9}
.badge{display:inline-block;padding:1px 8px;border-radius:20px;font-size:12px;color:#fff}
.b-g{background:var(--g)}.b-y{background:var(--y)}.b-r{background:var(--r)}.b-w{background:var(--w)}
.bar{height:8px;background:#eef0f2;border-radius:6px;overflow:hidden}.bar>i{display:block;height:100%;background:var(--g)}
details{margin:8px 0}summary{cursor:pointer;font-weight:600;font-size:14px}
ul{margin:6px 0 6px 18px;padding:0}li{margin:3px 0}
@media print{body{background:#fff}.card{break-inside:avoid;border-color:#ccc}}
</style></head><body><div class="wrap">
<h1>{Tiêu đề}</h1><div class="sub">{Dự án} | {Đối tượng đọc} | {Ngày}</div>

<div class="card summary"><h2>Tóm tắt</h2>
<ul><li>{Đang ở đâu}</li><li>{Đã quyết gì}</li><li>{Rủi ro chính}</li></ul></div>

<div class="card"><h2>Bối cảnh, mục tiêu</h2><p>{...}</p></div>

<div class="card"><h2>Tiến độ</h2>
<table><tr><th>Hạng mục</th><th>Trạng thái</th><th>Ghi chú</th></tr>
<tr><td>{Mốc}</td><td><span class="badge b-g">Xong</span></td><td>{...}</td></tr>
<tr><td>{...}</td><td><span class="badge b-y">Đang làm</span></td><td>{...}</td></tr>
</table></div>

<div class="card"><h2>Quyết định đã thống nhất</h2><ul><li>{...}</li></ul></div>
<div class="card"><h2>Chưa quyết, rủi ro</h2><ul><li>{...}</li></ul></div>
<div class="card"><h2>Bước tiếp theo</h2><ul><li>{...}</li></ul></div>

<div class="card"><details><summary>Phụ lục: chi tiết kỹ thuật, thuật ngữ</summary>
<p>{Đối tượng không phải lập trình viên thì đưa phần kỹ thuật xuống đây}</p></details></div>
</div></body></html>
```

## Quy tắc điền
- Badge trạng thái: Xong = `b-g`, Đang làm = `b-y`, Chậm = `b-r`, Chưa xác định = `b-w`. Theo căn cứ bản gốc.
- Cần thanh tiến độ và **bản gốc có %**: `<div class="bar"><i style="width:70%"></i></div>`. Không có thì chỉ ghi tên giai đoạn.
- Lưu `.html` vào thư mục tài liệu của người dùng. Nên mở file xem lại bằng mắt.
- Cuối cùng chỉnh giọng thân bài bằng `stop-slop-vi`.
