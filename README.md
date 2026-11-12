# stop-slop-vi

Skill cho Claude Code gỡ "giọng AI" khỏi tài liệu công việc tiếng Việt.

Giao biên bản họp, báo cáo, đề xuất, email, file pptx/docx/xlsx cho Claude, bạn sẽ hay gặp em-dash (`—`), liệt kê bằng dấu chấm giữa (` · `), `★` và emoji, tiêu đề viết hoa mọi chữ đầu, cùng văn dịch kiểu `được thực hiện bởi`, `có thể nói rằng`. Skill này giúp không viết những câu như vậy ngay từ đầu. Với tài liệu đã có, nó chỉ sửa dấu câu và văn dịch, không động vào nội dung.

Làm lại cho tiếng Việt từ [leeandev/stop-slop-ko](https://github.com/leeandev/stop-slop-ko) (bản tiếng Hàn), vốn dựa trên ý tưởng của [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop) (bản tiếng Anh). Quy tắc không dịch thẳng mà viết lại cho cách viết tài liệu tiếng Việt.

## Trước / sau

```diff
- # Báo Cáo Cải Tiến Ứng Dụng Mượn Sách
+ # Báo cáo cải tiến ứng dụng mượn sách

- Dự án nhằm mục đích cải tiến cấu trúc tìm kiếm của ứng dụng mượn sách nội bộ — đơn giản hóa quy trình mượn sách cho nhân viên.
+ Dự án cải tiến cấu trúc tìm kiếm của ứng dụng mượn sách nội bộ để nhân viên mượn sách nhanh hơn, ít bước hơn.

- - ★ Tăng tốc độ tìm kiếm · thêm chức năng đặt trước · nhắc hạn trả sách
+ - Tăng tốc độ tìm kiếm, thêm chức năng đặt trước, nhắc hạn trả sách

- - Việc thực hiện việc chuyển đổi dữ liệu được tiến hành bởi nhóm hạ tầng
+ - Nhóm hạ tầng chuyển đổi dữ liệu

- - Công cụ tìm kiếm mới cho phép tra cứu 3.000 đầu sách trong 1 giây ✅
+ - Công cụ tìm kiếm mới tra cứu 3.000 đầu sách trong 1 giây

- - Bổ sung bước xác nhận khi ghi nhận lịch sử mượn , trả
+ - Bổ sung bước xác nhận khi ghi nhận lịch sử mượn, trả

- Có thể nói, đây là bước đi đóng vai trò then chốt trong việc xây dựng văn hóa đọc của công ty.
+ Sau cải tiến, nhân viên tìm và mượn sách nội bộ dễ hơn.
```

Kết quả quét hai file bằng scanner đi kèm `slop_scan.py`. File gốc nằm trong [`examples/`](examples/); dòng gợi ý cách sửa của từng mục được lược bớt.

```
== before.md: WARN 9, INFO 0
  [WARN] TITLE_CASE @ L1: # Báo Cáo Cải Tiến Ứng Dụng Mượn Sách
  [WARN] EMDASH @ L5: …ứng dụng mượn sách nội bộ — đơn giản hóa quy trình m…
  [WARN] STAR @ L9: - ★ Tăng tốc độ tìm kiếm · t…
  [WARN] MIDDOT_SPACED2 @ L9: - ★ Tăng tốc độ tìm kiếm · thêm chức năng đặt trước · nhắc hạn trả sách
  [WARN] TL_BOI @ L10: … việc chuyển đổi dữ liệu được tiến hành bởi nhóm hạ tầng
  [WARN] TL_VIEC_CHAIN @ L10: - Việc thực hiện việc chuyển đổi dữ liệu được …
  [WARN] EMOJI @ L11: …00 đầu sách trong 1 giây ✅
  [WARN] SPACE_BEFORE_PUNCT @ L12: … khi ghi nhận lịch sử mượn , trả
  [WARN] TL_COTHENOI @ L17: Có thể nói, đây là bước đi đóng vai…
== after.md: WARN 0, INFO 0
RESULT: FAIL (WARN 9)
```

## Vì sao không dùng thẳng quy tắc bản tiếng Anh

stop-slop tiếng Anh khuyên "viết chủ động, ngắn, thẳng". Áp nguyên vào báo cáo tiếng Việt thì gạch đầu dòng `- Hoàn thành kiểm thử` bị ép thành câu đủ chủ vị, `Kính gửi` bị "làm mềm", và văn bản càng gượng.

- **Gạch đầu dòng không chủ ngữ không phải slop.** Đó là kiểu viết bình thường của báo cáo, biên bản. Chế độ làm sạch không đổi kiểu câu.
- **Không đổi xưng hô và thể thức.** `tôi/chúng tôi/em/mình`, `ạ/nhé`, `Kính gửi/Căn cứ/Nơi nhận` là lựa chọn của người viết.
- **Dấu hiệu AI thật của tiếng Việt là dấu câu, văn dịch và sáo ngữ:** em-dash, ` · ` liệt kê, `★`, cách trước dấu câu (`dự án , kế hoạch`), tiêu đề Title Case, `được … bởi`, `việc … việc`, `có thể nói rằng`.
- **` – ` (en-dash có cách) là dấu gạch ngang chuẩn của tiếng Việt,** không bị báo.
- **Quy tắc "cấm liệt kê ba ý", "cấm not X but Y" của bản tiếng Anh không áp cho danh sách yêu cầu, thông số.** Đó là nội dung, không phải văn phong.

## Có gì trong repo

Repo này là một marketplace plugin cho Claude Code với hai plugin. Cài cái nào cần.

| Plugin | Việc làm |
|---|---|
| **stop-slop-vi** | Áp quy tắc văn phong khi viết mới (tạo mới), sửa lại (làm sạch) hoặc theo văn phong tài liệu khác (khớp giọng) cho tài liệu tiếng Việt. Xử lý cả văn tự sự như tiểu luận, blog, bình luận. Có scanner và hook tự áp dụng |
| **stakeholder-brief** | Dựng lại tài liệu thiết kế, phân tích, tiến độ theo tầm đọc của một đối tượng (lãnh đạo, PM phía khách hàng, lập trình viên team khác) rồi xuất HTML/DOCX/MD. Lượt chỉnh văn phong cuối giao cho stop-slop-vi |

### stop-slop-vi

Ba chế độ:

- **Tạo mới**: viết biên bản, báo cáo, email mới đúng quy tắc ngay từ đầu. Tạo file xong thì quét bằng scanner và báo `PASS`/`FAIL`.
- **Làm sạch**: chỉ sửa dấu câu, văn dịch, sáo ngữ trong tài liệu có sẵn. Giữ nguyên số liệu, mã yêu cầu, thuật ngữ, xưng hô và thể thức hành chính.
- **Khớp giọng**: rút văn phong (kiểu câu, xưng hô, dấu câu, ký hiệu danh sách… theo 6 trục) từ chương đồng nghiệp viết hoặc tài liệu đã duyệt, rồi viết phần của bạn theo đó.

**Scanner** `slop_scan.py`: quét theo đoạn các file docx (thân, bảng, header, chú thích), pptx (theo thứ tự slide, bảng), xlsx (ô, hình), md, txt, html. Chỉ dùng thư viện chuẩn của Python.

```bash
python plugins/stop-slop-vi/skills/stop-slop-vi/scripts/slop_scan.py bao-cao.docx --info
```

- exit 0 = PASS, 1 = FAIL (có WARN), 2 = lỗi đầu vào
- Chuẩn hóa NFC trước khi quét và báo WARN nếu văn bản dùng dấu tổ hợp (NFD), thường gặp khi dán từ macOS
- Chỉ quét đoạn có chữ tiếng Việt có dấu. Văn bản gõ hoàn toàn không dấu không được quét
- Sáo ngữ, danh từ hóa thừa, bộ ba đều nhịp scanner không bắt được. Phần đó skill đọc và quyết

**Sửa bài của chính mình**: tiểu luận, bài thu hoạch, blog, bình luận, thư xin việc cũng dùng ba chế độ trên. Văn vẫn viết thành đoạn, không bị đổi sang gạch đầu dòng, và khi sửa không đổi xưng hô `tôi/mình/em`. Skill gỡ các sáo ngữ hay chen vào văn tự sự.

| Trước | Sau |
|---|---|
| Hôm nay chúng ta cùng tìm hiểu về Docker volume. Đây là phần thực sự khiến rất nhiều bạn bối rối. | (xóa) Vào thẳng nội dung từ "Khi xóa container, các file ghi bên trong container cũng mất theo." |
| Nhờ có ghi chép nên quyết định ít bị đảo ngược hơn. … Qua trải nghiệm này, tôi nhận ra tầm quan trọng của giao tiếp. | Nhờ có ghi chép nên quyết định ít bị đảo ngược hơn. |

Thêm `--prose` để scanner kiểm cả dấu hiệu văn tự sự.

```bash
python plugins/stop-slop-vi/skills/stop-slop-vi/scripts/slop_scan.py tieu-luan.md --prose --info
```

- INFO (chỉ báo vị trí): kết bằng bài học ("tôi nhận ra tầm quan trọng của…"), "không chỉ là … mà còn", đoạn đầu mở bằng danh ngôn, từ nhấn rỗng ("thực sự", "vô cùng"), sáo ngữ tiểu luận và blog
- WARN (tính trên toàn bài): "tôi cho rằng" (nghĩ rằng, tin rằng, theo tôi) từ 3 lần và ít nhất 1 lần mỗi 2.500 ký tự; từ 3 đoạn mở bằng liên từ ("Bên cạnh đó", "Ngoài ra") và chiếm từ 25% số đoạn. Ngưỡng tăng theo độ dài bài nên tần suất bình thường không bị bắt
- Không bịa sự thật, số liệu, nguồn. Câu cần sửa mà không có căn cứ thì xóa hoặc hỏi lại

**Hook tự áp dụng**: nhận ra các yêu cầu như "soạn biên bản họp", "làm báo cáo pptx", "bỏ giọng AI" (gõ có dấu hay không dấu đều được) và nhắc Claude dùng skill. Yêu cầu có đối tượng đọc ("cho lãnh đạo", "cho khách hàng", "bản brief") thì nhắc dùng stakeholder-brief trước. Yêu cầu văn tự sự ("viết tiểu luận", "sửa bài blog") thì nhắc văn phong tự sự. Yêu cầu viết code ("viết hàm gửi email", "sửa bug module báo cáo") thì không can thiệp. Thêm "không dùng stop-slop" hoặc "giữ nguyên câu chữ" vào yêu cầu để hook im lặng.

### stakeholder-brief

- Với mỗi đối tượng trong 4 loại (lãnh đạo/nhà tài trợ, PM phía khách hàng, lập trình viên mới hoặc team khác, lập trình viên phía khách hàng), skill quyết định dịch thuật ngữ đến đâu và đưa gì xuống phụ lục.
- Hai loại tài liệu: **kiểu đồng thuận** để báo tiến độ, đồng thuận (tóm tắt → hiện trạng → quyết định đã thống nhất → chưa quyết → bước tiếp theo), và **kiểu hướng dẫn** để giới thiệu công cụ, quy trình (tổng quan nhanh → vì sao cần → cài đặt → ví dụ → giới hạn).
- **Không bịa tiến độ, lịch, quyết định không có trong bản gốc.** Không có thì ghi "chưa xác định" hoặc "cần xác nhận".

## Cài đặt

Gõ từng dòng vào ô nhập của Claude Code.

**Bước 1. Đăng ký marketplace (bắt buộc, làm một lần)**

Đăng ký repo này làm danh sách plugin. Bước này chưa cài gì.

```
/plugin marketplace add mrtinhnguyen/stop-slop-vi
```

**Bước 2. Cài plugin cần dùng**

| Muốn dùng để | Cài |
|---|---|
| Chỉ gỡ giọng AI khỏi tài liệu tiếng Việt (phần lớn trường hợp) | Chỉ stop-slop-vi |
| Làm thêm tài liệu chia sẻ cho lãnh đạo, PM phía khách hàng | Cả hai |

Cài stop-slop-vi (cơ bản):

```
/plugin install stop-slop-vi@stop-slop-vi
```

Cài stakeholder-brief (chỉ khi cần làm tài liệu chia sẻ):

```
/plugin install stakeholder-brief@stop-slop-vi
```

stakeholder-brief cài riêng vẫn chạy, nhưng được thiết kế để giao lượt chỉnh văn phong cuối cho stop-slop-vi, nên nên cài cả hai.

Cài xong thì khởi động lại Claude Code. Mở `/plugin` để xem các plugin đã cài.

### Cài không cần dòng lệnh

**App desktop Claude Code (tab Code):** bấm **+** cạnh ô nhập, chọn **Add plugins**, thêm marketplace `mrtinhnguyen/stop-slop-vi`, rồi chọn plugin cần cài.

**VS Code:** mở **Manage plugins**, thêm marketplace ở tab **Marketplaces**, rồi bấm **Install** ở tab **Plugins**.

**Khai báo trong file cấu hình:** thêm đoạn sau vào `~/.claude/settings.json` (cho riêng bạn) hoặc `.claude/settings.json` của repo (cho cả nhóm). Khai báo trong repo chỉ bật plugin; mỗi người vẫn cài một lần bằng giao diện ở trên.

```json
{
  "extraKnownMarketplaces": {
    "stop-slop-vi": {
      "source": { "source": "github", "repo": "mrtinhnguyen/stop-slop-vi" },
      "autoUpdate": true
    }
  },
  "enabledPlugins": {
    "stop-slop-vi@stop-slop-vi": true,
    "stakeholder-brief@stop-slop-vi": true
  }
}
```

### Dùng trên claude.ai (bản web)

claude.ai không cài plugin Claude Code mà có hệ thống plugin và skill riêng. Có ba cách:

- **Thêm marketplace:** **Customize > Plugins > Add > Add marketplace**, nhập `mrtinhnguyen/stop-slop-vi`.
- **Tải lên file zip** (lấy ở trang [Releases](https://github.com/mrtinhnguyen/stop-slop-vi/releases) hoặc tự đóng gói như bên dưới):
  - `stop-slop-vi-skill.zip`, `stakeholder-brief-skill.zip`: **Customize > Skills > + > Upload a skill**
  - `stop-slop-vi-plugin.zip`, `stakeholder-brief-plugin.zip`: **Customize > Plugins > Add > Upload plugin**
- **Cho cả tổ chức (Team/Enterprise):** Owner vào **Organization settings > Plugins & skills > Add**, chọn **Add marketplace** hoặc **Sync from GitHub**, rồi đặt mức **Installed by default** hoặc **Required**.

Trên claude.ai, skill hoạt động khi tổ chức bật **Cloud code execution and file creation** và **Skills**. Quy tắc và tài liệu tham chiếu dùng được đầy đủ. Hook tự áp dụng chỉ chạy trong Claude Code. Scanner `slop_scan.py` có chạy được trên claude.ai hay không thì tài liệu của Anthropic chưa nói rõ.

Tự đóng gói zip (ra thư mục `dist/`):

```bash
python scripts/build_zips.py
```

**Yêu cầu**
- Scanner và hook: Python 3.8 trở lên (macOS/Linux dùng `python3`, Windows dùng `python`)
- Hook tự áp dụng chạy bằng `sh`. Windows cần Git Bash (có sẵn trong Git for Windows). Không có Git Bash thì chỉ hook không chạy, skill và scanner vẫn dùng được
- Công thức sửa pptx: `pip install python-pptx`
- Xuất DOCX: `pip install python-docx`

## Ví dụ sử dụng

```
Soạn biên bản họp tuần dạng docx, ghi âm ở meeting.txt
Bỏ giọng AI trong chương 3 của đề xuất này
Sửa bài blog này, file là post.md
Viết slide 14 đến 17 theo văn phong slide 1 đến 13
Tóm tắt tài liệu thiết kế này thành brief 1 trang cho lãnh đạo
/stop-slop-vi:stop-slop-vi bao-cao.md
```

Gọi trực tiếp skill của plugin bằng tên `plugin:skill` (`/stop-slop-vi:stop-slop-vi`, `/stakeholder-brief:stakeholder-brief`). Phần lớn trường hợp chỉ cần yêu cầu bằng lời như trên là skill tự được dùng.

## Phát triển

```bash
python -m unittest discover -s tests
python plugins/stop-slop-vi/hooks/stop-slop-doc-reminder.py --selftest
```

Kịch bản kiểm thử skill với subagent nằm ở [`tests/scenarios/`](tests/scenarios/). Nghiên cứu và kế hoạch chuyển đổi ở [`docs/superpowers/specs/`](docs/superpowers/specs/).

## Giấy phép

MIT. Xem [LICENSE](LICENSE). Bản này dựa trên [leeandev/stop-slop-ko](https://github.com/leeandev/stop-slop-ko) (MIT, © 2026 leeandev), vốn lấy ý tưởng từ [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop) (MIT).
