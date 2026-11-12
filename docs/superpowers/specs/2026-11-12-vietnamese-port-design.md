# Chuyển stop-slop-ko sang tiếng Việt (stop-slop-vi): nghiên cứu và kế hoạch

Ngày: 2026-11-12. Phạm vi: toàn bộ repo (3 plugin, scanner, hook, test, README). Mục tiêu: chỉ hỗ trợ tiếng Việt, bỏ hẳn tiếng Hàn.

## 1. Repo hiện có gì

| Thành phần | File | Mức gắn với tiếng Hàn |
|---|---|---|
| Skill chính | `plugins/stop-slop-ko/skills/stop-slop-ko/SKILL.md` | Cao: toàn bộ quy tắc xoay quanh lối viết gạch đầu dòng kết thúc bằng danh từ của tiếng Hàn và đuôi câu |
| Bảng dấu hiệu | `references/ko-slop-patterns.md` | Cao: trợ từ, văn dịch Hàn, gạch giữa ghép từ |
| Văn tự sự | `references/prose-patterns.md` | Trung bình: khung 7 dấu hiệu dùng lại được, ví dụ và regex phải viết mới |
| Khớp giọng | `references/tone-extraction.md` | Thấp: 6 trục dùng lại được, trục "đuôi câu" và "mật độ trợ từ" phải thay |
| Sửa pptx | `references/pptx-editing.md` | Rất thấp: code python-pptx trung lập, chỉ dịch chú thích và ví dụ |
| Scanner | `scripts/slop_scan.py` (347 dòng) | Phần đọc docx/pptx/xlsx/md/html trung lập (~60%); phần `RULES`, `PROSE_RULES`, `HANGUL`, `PARTICLE`, `THINK`, `CONNECTOR` phải viết lại |
| Hook điều hướng | `hooks/stop-slop-doc-reminder.py` (227 dòng) | Logic `route()` trung lập; mọi regex từ khóa và `MESSAGES`, `SELFTEST` phải viết lại |
| stakeholder-brief | 6 file | Thấp: phương pháp trung lập, chỉ dịch và đổi font, đổi tên đối tượng đọc |
| jasoseo | 6 file + `count.py` | Rất cao: thư tự giới thiệu kiểu Hàn là thể loại riêng (đếm ký tự, byte EUC-KR, 5 câu hỏi chuẩn) |
| Test | `tests/*.py`, `tests/scenarios/*.md` | Cao: mọi fixture là tiếng Hàn |

Gần như toàn bộ phần khó (trích xuất văn bản từ Office, gom đoạn md, ngưỡng theo độ dài, kiểm tra plugin cài hay chưa, bỏ qua thông báo task) dùng lại được. Việc chính là thay **tri thức ngôn ngữ**, không phải hạ tầng.

## 2. Cái gì mang sang được, cái gì phải bỏ

### Giữ nguyên ý tưởng
- Ba chế độ: **tạo mới / làm sạch / khớp giọng**.
- Nguyên tắc lõi: giữ 100% nội dung, số liệu, căn cứ, thuật ngữ; chỉ sửa dấu câu, văn dịch, sáo ngữ.
- Không bịa sự thật; thiếu thì ghi `[cần xác nhận: ...]`.
- Scanner chỉ bắt dấu hiệu máy đo được; sáo ngữ và nhịp câu để mô hình đọc.
- Báo cáo `PASS/FAIL/NOT_RUN`, exit code 0/1/2.

### Bỏ vì là đặc thù tiếng Hàn
- `PARTICLE_SPACE` (cách trước trợ từ tiếng Hàn): tiếng Việt không có trợ từ dính liền.
- `TL_ISSEO`, `TL_TONGHAYEO`, `TL_DOEEOJI`, `TL_HALSUITDA`, `TL_DAEBI_SANGI`: văn dịch Hàn.
- Ngoại lệ "dấu chấm giữa dùng để ghép từ" của tiếng Hàn: tiếng Việt không dùng `·` để ghép từ, nên mọi `·` trong văn xuôi đều đáng ngờ.
- `ENDASH` INFO: trong tiếng Việt, ` – ` có cách hai bên là dấu gạch ngang chuẩn của văn bản, không phải dấu hiệu AI (xem 3.1).
- Toàn bộ quy tắc về đuôi câu tiếng Hàn.
- `count.py`: byte EUC-KR, cp949.

## 3. Dấu hiệu AI riêng của tiếng Việt

### 3.1 Dấu câu và chính tả (scanner bắt được)

| Mã đề xuất | Mức | Dấu hiệu | Lý do |
|---|---|---|---|
| `EMDASH` | WARN | `—` (em-dash) trong văn xuôi | Văn Việt dùng ` – ` (en-dash có cách) hoặc dấu phẩy, ngoặc. `—` dính liền là thói quen tiếng Anh của model |
| `STAR`, `EMOJI`, `DIVIDE` | WARN | `★`, emoji trang trí, `÷` | Giữ như bản Hàn |
| `MIDDOT_LIST` | WARN | ` · ` dùng phân cách liệt kê | Tiếng Việt liệt kê bằng dấu phẩy hoặc chấm phẩy |
| `SPACE_BEFORE_PUNCT` | WARN | Cách trước `, . : ; ! ?` (`dự án , kế hoạch`) | Lỗi máy/ghép chuỗi, tương tự `PARTICLE_SPACE` của bản Hàn |
| `NO_SPACE_AFTER_PUNCT` | INFO | Thiếu cách sau dấu phẩy giữa chữ (`a,b`) | Trừ số `3,5` và chữ viết tắt |
| `TITLE_CASE` | WARN | Tiêu đề viết hoa mọi chữ đầu (`Kế Hoạch Triển Khai Dự Án`) | Tiếng Việt viết hoa kiểu câu; Title Case là dấu vết dịch từ tiếng Anh. Chỉ xét dòng tiêu đề md, không xét tên riêng ngắn |
| `NFD_MIX` | WARN | Văn bản có ký tự tổ hợp (NFD) hoặc lẫn NFC/NFD | Dán từ macOS hoặc pipeline máy; gây lỗi tìm kiếm. Scanner chuẩn hóa NFC trước khi so regex |
| `TONE_MARK_MIX` | INFO | Một tài liệu lẫn hai kiểu bỏ dấu (`hòa`/`hoà`, `thúy`/`thuý`) | Không sai, nhưng không nhất quán là dấu vết ghép nhiều nguồn. Chỉ báo khi cả hai kiểu cùng xuất hiện |
| `QUOTE_MIX` | INFO | Lẫn ngoặc cong `“ ”` và ngoặc thẳng `"` | Giữ như bản Hàn |
| `BOLD_LABEL` | INFO | Quá nhiều dòng mở bằng `**Nhãn:**` | Chữ ký định dạng của chatbot. Ngưỡng theo tỷ lệ dòng |
| `ELLIPSIS_MIX` | INFO | Lẫn `...` và `…` | Nhất quán |

Lọc đoạn: thay bộ lọc chữ Hangul bằng phát hiện tiếng Việt, ví dụ có ít nhất một ký tự trong `[ăâđêôơưàáảãạ...ỹ]` sau khi chuẩn hóa NFC. Đoạn không dấu (thuần tiếng Anh, code) bỏ qua như bản Hàn bỏ đoạn không có Hangul.

### 3.2 Văn dịch và sáo ngữ (một phần bắt bằng regex, còn lại mô hình đọc)

Tương đương với nhóm `TL_*` của bản Hàn:

| Mã đề xuất | Mức | Mẫu | Sửa |
|---|---|---|---|
| `TL_BOI` | WARN | Bị động có tác nhân `được ... bởi` (`được phát triển bởi nhóm A`) | `nhóm A phát triển` |
| `TL_MOTCACH` | INFO | `một cách + tính từ` dày đặc (`một cách hiệu quả`) | `hiệu quả`, hoặc bỏ |
| `TL_VIEC_CHAIN` | WARN | `việc` chồng việc (`việc thực hiện việc triển khai`) | Bỏ danh từ hóa thừa |
| `TL_TIENHANH` | INFO | `tiến hành + động từ` (`tiến hành kiểm tra`) | `kiểm tra` |
| `TL_COTHENOI` | WARN | `có thể nói (rằng)`, `có thể thấy (rằng)` | Khẳng định thẳng |
| `TL_DONGVAITRO` | INFO | `đóng (một) vai trò (quan trọng|then chốt)` | Nói việc nó làm |
| `TL_LAMOTTRONG` | INFO | `là một trong những ... nhất` | Nói thẳng, hoặc dẫn số liệu |
| `TL_THONGQUA` | INFO | `thông qua` dày đặc | `bằng`, `qua`, `nhờ` |
| `TL_DOIVOIVIEC` | INFO | `đối với việc`, `trong việc` mở câu | Bỏ hoặc đổi chủ ngữ |
| `TL_NHAM` | INFO | `nhằm mục đích` | `để` |

Ngưỡng: các mục INFO kiểu "dày đặc" nên dùng mật độ theo 1.000 ký tự như `PROSE_THINK` hiện có, vì một lần `thông qua` là bình thường.

### 3.3 Văn tự sự (`--prose`)
Map 7 dấu hiệu của `prose-patterns.md` sang tiếng Việt:

| Bản Hàn | Bản Việt |
|---|---|
| Kết bài bằng bài học | `tôi nhận ra tầm quan trọng của`, `bài học rút ra là`, `đã giúp tôi hiểu được` |
| "Không đơn thuần là A mà là B" | `không chỉ là ... mà còn`, `không đơn thuần là`, `không chỉ dừng lại ở` |
| Mở bằng danh ngôn, định nghĩa từ điển | `Có câu nói`, `Theo từ điển`, `Như ... đã từng nói` |
| Từ nhấn rỗng | `thực sự`, `vô cùng`, `cực kỳ`, `hết sức`, `đặc biệt là` |
| "Tôi nghĩ rằng" lặp lại | `tôi cho rằng`, `tôi nghĩ rằng`, `theo tôi`, `có lẽ` (WARN theo mật độ) |
| Đoạn mở bằng liên từ | `Bên cạnh đó`, `Ngoài ra`, `Hơn nữa`, `Đồng thời`, `Tóm lại`, `Nhìn chung` (WARN theo tỷ lệ) |
| Sáo ngữ báo cáo / blog | `Trong bối cảnh ...`, `Trong kỷ nguyên số`, `Hôm nay chúng ta cùng tìm hiểu`, `Hy vọng bài viết hữu ích`, `Đừng quên like và share` |

Nguồn đối chiếu sẵn có: skill `congchucso-tone` trên máy (`~/.claude/skills/congchucso-tone/references/patterns.md`, `deep-tells.md`) đã có kho dấu hiệu AI tiếng Việt chia lớp. Nên lấy danh sách từ đó làm điểm xuất phát rồi chọn mục regex đo được, tránh hai bộ quy tắc mâu thuẫn. Phân vai đề xuất: `congchucso-tone` lo biên tập sâu văn xuôi; `stop-slop-vi` lo tài liệu công việc, scanner Office và hook tự động.

### 3.4 "Cái bẫy" tương đương mục cạm bẫy ngôn ngữ của bản Hàn

Bản Hàn có luật cứng: không đổi đuôi câu của người viết. Bản Việt cần luật tương tự:

1. **Văn phong hành chính không phải slop.** Công văn, tờ trình, báo cáo theo Nghị định 30/2020/NĐ-CP có câu chữ trang trọng (`Căn cứ`, `Đề nghị`, `Kính gửi`, `Nơi nhận`). Chế độ làm sạch không được "làm cho tự nhiên" phần thể thức này.
2. **Không đổi xưng hô và tiểu từ cuối câu.** `tôi/chúng tôi/em/anh/chị`, `ạ/nhé/nha` là lựa chọn của tác giả, giống đuôi câu tiếng Hàn. Chỉ đổi trong chế độ khớp giọng.
3. **Gạch đầu dòng danh từ là bình thường.** Báo cáo dạng `- Hoàn thành kiểm thử module A` không cần thành câu đủ chủ vị.
4. **Bị động `được` không mặc định là sai.** Chỉ `được ... bởi` có tác nhân mới là văn dịch; `được phê duyệt` là bình thường.
5. Quy tắc tiếng Anh "cấm liệt kê 3 ý" không áp cho danh sách yêu cầu, thông số.

### 3.5 Hook: khó nhất là gõ không dấu

Người Việt hay gõ không dấu (`viet bao cao`, `soan cong van`). Hook nên so khớp trên chuỗi đã **bỏ dấu và hạ chữ thường** (`unicodedata` NFD rồi lọc `Mn`, đổi `đ→d`), đồng thời giữ regex có ranh giới từ để tránh khớp nhầm (`bao` trong `bảo`, `bào` cũng thành `bao`). Cần thêm test cho các ca này.

Từ khóa đề xuất:
- Tài liệu: `biên bản (họp)`, `báo cáo`, `tờ trình`, `công văn`, `kế hoạch`, `đề xuất`, `đề án`, `thông báo`, `hướng dẫn`, `tài liệu`, `email/mail/thư`, `slide`, `pptx`, `docx`, `xlsx`, `excel`, `word`, `README`, `.md`.
- Đối tượng đọc (định tuyến sang stakeholder-brief): `cho lãnh đạo`, `cho ban giám đốc`, `cho khách hàng`, `cho đối tác`, `cho nhân viên mới`, `để chia sẻ`, `bản tóm tắt`, `brief`, `tài liệu giới thiệu`.
- Động từ: `viết`, `soạn`, `tạo`, `làm`, `lập`, `chỉnh`, `sửa`, `biên tập`, `trau chuốt`, `rà soát`, `cập nhật`, `tóm tắt lại`.
- Giọng: `bớt giọng AI`, `bỏ văn máy`, `cho tự nhiên`, `khớp giọng`, `theo văn phong`.
- Văn tự sự: `bài luận`, `tiểu luận`, `bài blog`, `bài viết`, `bình luận`, `bài báo`, `cảm nhận`, `thư xin việc`.
- Thoát: `không dùng stop-slop`, `giữ nguyên văn`.

Cạm bẫy đã thấy ở bản Hàn (v1.2.2 sửa hai lần báo nhầm) sẽ lặp lại theo kiểu khác: `làm` và `tạo` rất phổ biến trong yêu cầu code (`tạo function`, `làm API`). Phải đòi đồng thời từ khóa tài liệu + động từ, và thêm danh sách loại trừ ngữ cảnh code.

## 4. Hai plugin phụ

**stakeholder-brief**: dịch thẳng, đổi đối tượng sang bối cảnh Việt (Lãnh đạo/Ban giám đốc, Khách hàng/PM phía khách, Lập trình viên mới hoặc team khác, Lập trình viên phía khách). Đổi font tiếng Hàn sang `Times New Roman` cho DOCX hành chính hoặc `Segoe UI`/`Arial` cho tài liệu kỹ thuật; HTML dùng `system-ui`. Công sức nhỏ.

**jasoseo**: thể loại thư tự giới thiệu kiểu Hàn không có bản sao ở Việt Nam. Ba lựa chọn:
- (a) Bỏ hẳn.
- (b) Đổi thành coach **CV + thư xin việc** tiếng Việt: giữ phần phỏng vấn, ngân hàng trải nghiệm, cấm bịa; đổi `count.py` sang đếm **số từ** (âm tiết cách nhau bởi khoảng trắng) và ký tự, bỏ byte EUC-KR; đổi bộ câu hỏi sang mẫu tuyển dụng Việt (giới thiệu bản thân, lý do ứng tuyển, kinh nghiệm theo STAR, định hướng).
- (c) Tạm giữ ngoài marketplace, làm sau.

Đề xuất (c) cho đợt đầu, (b) ở đợt sau: lõi stop-slop-vi đứng được một mình, còn jasoseo cần nghiên cứu thể loại riêng.

## 5. Kế hoạch thực hiện

Theo thứ tự, mỗi bước một commit, viết test trước (TDD).

1. **Đổi tên và khung**: `plugins/stop-slop-ko` → `plugins/stop-slop-vi`, skill `stop-slop-vi`, `marketplace.json`, `plugin.json`, version `2.0.0` (đổi ngôn ngữ là thay đổi phá vỡ). Giữ ghi nguồn MIT cho leeandev/stop-slop-ko và hardikpandya/stop-slop.
2. **Scanner**: viết `tests/test_slop_scan.py` với fixture tiếng Việt cho từng mã ở mục 3.1 và 3.2 (ca đúng và ca không được báo nhầm), rồi sửa `slop_scan.py`: chuẩn hóa NFC, `VIET` thay `HANGUL`, bộ `RULES` mới, `PROSE_RULES`/`THINK`/`CONNECTOR` mới. Phần trích xuất Office giữ nguyên.
3. **References**: viết `vi-slop-patterns.md` (thay `ko-slop-patterns.md`), viết lại `prose-patterns.md`, sửa `tone-extraction.md` (trục "đuôi câu" → "xưng hô và tiểu từ cuối câu", "mật độ trợ từ" → "mật độ hư từ `thì/là/mà/của`"), dịch `pptx-editing.md`.
4. **SKILL.md**: viết lại bằng tiếng Việt, mô tả trigger tiếng Việt cả có dấu và không dấu.
5. **Hook**: test `--selftest` trước (khoảng 40 ca: có dấu, không dấu, ngữ cảnh code, opt-out, thông báo task), rồi thay regex và `MESSAGES`. Thêm hàm bỏ dấu.
6. **stakeholder-brief**: dịch 6 file, đổi font, đổi tên tham chiếu `stop-slop-ko` → `stop-slop-vi`.
7. **jasoseo**: theo quyết định ở mục 4.
8. **README, examples, scenarios**: `examples/before.md`/`after.md` tiếng Việt, chạy scanner thật để lấy output đưa vào README.
9. **Dọn lịch sử**: các file `docs/superpowers/plans|specs` tiếng Hàn giữ trong git history, xóa khỏi cây (hoặc chuyển vào `docs/archive-ko/`).

Ước lượng: bước 2 và 5 chiếm phần lớn công sức (regex + test). Các bước còn lại chủ yếu là viết tài liệu.

## 6. Rủi ro

- **Báo nhầm `TITLE_CASE`** với tên riêng, tên tổ chức (`Bộ Tài Chính` vẫn hay bị viết vậy, `Công ty Cổ phần ...`). Chỉ áp cho tiêu đề md/docx, cần ngưỡng số từ và danh sách ngoại lệ.
- **`SPACE_BEFORE_PUNCT`** với chuỗi kỹ thuật (`a ? b : c`, `x : int`). Bỏ qua code inline như bản Hàn đang làm.
- **Hook không dấu** dễ khớp rộng. Cần test âm (prompt code, prompt hỏi đáp) nhiều hơn test dương.
- **Chồng chéo với `congchucso-tone`**: phải phân vai rõ trong description để Claude không tải cả hai cho cùng một yêu cầu.

## 7. Quyết định đã chốt

1. jasoseo: bỏ hẳn khỏi repo (thể loại thư tự giới thiệu kiểu Hàn không có bản tương đương ở Việt Nam). Có thể làm lại thành coach CV và thư xin việc tiếng Việt trong một plugin mới.
2. Marketplace `stop-slop-vi`, chủ sở hữu `mrtinhnguyen` (github.com/mrtinhnguyen/stop-slop-vi).
3. README chỉ viết tiếng Việt, không giữ phần tóm tắt tiếng Anh.
4. `stop-slop-vi` độc lập, không gọi sang `congchucso-tone`.
5. Lịch sử commit tiếng Hàn bị xóa; repo bắt đầu từ một commit duy nhất. Ghi nguồn và bản quyền MIT của leeandev/stop-slop-ko và hardikpandya/stop-slop được giữ trong LICENSE và README.
