# -*- coding: utf-8 -*-
import json
import subprocess
import sys
import unicodedata
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOOK = ROOT / "plugins" / "stop-slop-vi" / "hooks" / "stop-slop-doc-reminder.py"
sys.path.insert(0, str(HOOK.parent))
H = __import__("stop-slop-doc-reminder")


def kind(prompt):
    r = H.route(prompt)
    return r[0] if r else None


class Fold(unittest.TestCase):
    def test_strips_marks_keeps_length(self):
        for s in ["Soạn biên bản họp", "ĐỀ XUẤT", "Thư xin việc", "dự án ổn"]:
            f = H.fold(s)
            self.assertEqual(len(f), len(s), s)
            self.assertTrue(f.isascii(), f)
        self.assertEqual(H.fold("Đề Xuất"), "de xuat")

    def test_nfd_input(self):
        self.assertEqual(H.fold(unicodedata.normalize("NFD", "báo cáo")), H.fold("báo cáo"))


class Route(unittest.TestCase):
    def test_docs(self):
        for p in ["Soạn biên bản họp tuần này dạng docx", "Viết báo cáo tháng 10", "Làm slide pptx cho buổi họp",
                  "Soạn công văn gửi Sở Tài chính", "Viết email trả lời khách", "Sửa tờ trình mục 3",
                  "Viết tài liệu API cho module thanh toán"]:
            self.assertEqual(kind(p), "slop", p)

    def test_no_diacritics(self):
        for p in ["soan bien ban hop", "viet bao cao thang", "lam slide gioi thieu san pham pptx", "sua cong van nay"]:
            self.assertEqual(kind(p), "slop", p)

    def test_audience_goes_to_brief(self):
        for p in ["Tóm tắt tài liệu thiết kế này cho lãnh đạo", "Làm bản brief cho khách hàng dạng HTML",
                  "Viết tài liệu giới thiệu skill để chia sẻ nội bộ", "lam ban tom tat cho ban giam doc"]:
            self.assertEqual(kind(p), "brief", p)
        self.assertEqual(kind("/stakeholder-brief thiet-ke.md cho khách hàng"), "brief_explicit")

    def test_tone(self):
        for p in ["Bỏ giọng AI trong slide 14 đến 17", "Chương 3 viết theo văn phong chương 1",
                  "bo giong AI giup minh", "Đoạn này đọc như văn dịch máy, sửa giúp"]:
            self.assertEqual(kind(p), "slop", p)

    def test_prose(self):
        for p in ["Viết tiểu luận về làm việc từ xa", "Sửa bài blog này", "Viết bài bình luận cho báo",
                  "Viết thư xin việc vị trí backend", "viet bai thu hoach mon triet", "Bỏ giọng AI trong bài blog",
                  "Dựa vào báo cáo này viết bài blog"]:
            self.assertEqual(kind(p), "prose", p)

    def test_report_is_not_article(self):
        self.assertEqual(kind("Viết bài báo cáo tổng kết năm"), "slop")
        self.assertEqual(kind("Viết bài báo về chuyển đổi số"), "prose")

    def test_code_prompts_ignored(self):
        for p in ["Sửa bug build gradle", "Tạo function gửi email trong code", "Thêm bình luận vào code hàm này",
                  "Sửa thông báo lỗi khi đăng nhập", "Hướng dẫn tôi sửa lỗi test", "Tạo bảng database cho đơn hàng",
                  "Làm API thêm cột vào bảng", "Đọc tài liệu rồi sửa code cho đúng", "Viết unit test cho module",
                  "Lập kế hoạch refactor module thanh toán"]:
            self.assertIsNone(kind(p), p)

    def test_read_only_ignored(self):
        for p in ["Đọc file excel này rồi phân tích", "Báo cáo này nói gì?", "Tóm tắt giúp tôi bài blog này nói gì"]:
            self.assertNotEqual(kind(p), "slop", p)

    def test_word_collisions(self):
        self.assertIsNone(kind("Thử chạy lại lệnh build"))
        self.assertIsNone(kind("Sửa lỗi hiển thị bảo hành"))

    def test_opt_out(self):
        for p in ["Làm pptx nhưng không dùng stop-slop", "Soạn báo cáo, giữ nguyên câu chữ của tôi",
                  "/stop-slop-vi bao-cao.md", "viet bao cao, tat stop-slop"]:
            self.assertIsNone(kind(p), p)

    def test_task_notification_ignored(self):
        n = "<task-notification>\n<summary>Đã soạn xong tài liệu chia sẻ</summary>\n</task-notification>"
        self.assertIsNone(kind(n))
        self.assertIsNone(kind('<agent-message from="a1">\nĐã sửa xong bài blog\n</agent-message>'))
        self.assertEqual(kind("Viết lại kết quả sau thành báo cáo:\n" + n), "slop")
        self.assertIsNone(kind('<agent-message from="a1">\nĐã sửa xong bài blog'))
        self.assertIsNone(kind("Cái này là gì?\n" + n))

    def test_keyword_keeps_diacritics(self):
        self.assertEqual(H.route("Soạn biên bản họp")[1], "biên bản")


class ReviewFalsePositives(unittest.TestCase):
    def test_folded_verb_collisions(self):
        for p in ["Đọc file docx này và trả lời bằng tiếng Việt", "Giải thích bằng tiếng Việt vì sao hàm đọc xlsx chậm",
                  "Báo cáo này nói gì về thị trường Việt Nam?", "Đọc báo cáo này và cho biết điểm chính",
                  "Kế hoạch chính là gì?", "Lặp qua danh sách tài liệu và in ra"]:
            self.assertIsNone(kind(p), p)

    def test_code_with_doc_words(self):
        for p in ["Viết script chuyển docx sang pdf", "Viết code đọc file xlsx bằng pandas",
                  "Sửa bug trong module báo cáo doanh thu", "Viết API xuất báo cáo doanh thu",
                  "Sửa lỗi parse file .md trong script", "Viết unit test cho hàm tạo slide",
                  "Đoạn code này ai viết?", "Ai viết hàm này vậy?", "Tích hợp API dịch máy vào app"]:
            self.assertIsNone(kind(p), p)

    def test_code_with_prose_words(self):
        for p in ["Sửa bug ở trang blog", "Viết API lấy danh sách bài viết", "Làm chức năng bình luận cho bài viết",
                  "Viết hàm tính sản lượng thu hoạch", "Sửa giao diện để người dùng cảm nhận mượt hơn"]:
            self.assertIsNone(kind(p), p)

    def test_vietnamese_code_terms(self):
        for p in ["Viết hàm gửi thông báo cho người dùng", "Viết hàm gửi email xác nhận", "Lập trình chức năng xuất excel",
                  "Viết vòng lặp đọc từng dòng file word", "Sửa lỗi hiển thị văn bản trên màn hình",
                  "Tạo nút để chia sẻ link", "Làm trang web cho khách hàng", "Tạo tài khoản cho nhân viên mới"]:
            self.assertIsNone(kind(p), p)

    def test_everyday_word_collisions(self):
        for p in ["Tôi quyết định dùng Redis, viết lại cache", "Viết app đặt món để ăn trưa",
                  "Sửa lại rồi thử gửi lại xem sao"]:
            self.assertIsNone(kind(p), p)

    def test_misrouted(self):
        self.assertEqual(kind("Soạn thông báo lợi nhuận quý 3"), "slop")
        self.assertEqual(kind("Sửa đoạn văn bản này cho gọn"), "slop")
        self.assertEqual(kind("Viết README cho repo này"), "slop")
        self.assertEqual(kind("Soạn quyết định bổ nhiệm trưởng phòng"), "slop")

    def test_non_string_prompt(self):
        for raw in [b'{"prompt": 5}', b'{"prompt": ["a"]}']:
            r = subprocess.run([sys.executable, str(HOOK)], input=raw, capture_output=True)
            self.assertEqual(r.returncode, 0, raw)


class Cli(unittest.TestCase):
    def run_hook(self, raw):
        return subprocess.run([sys.executable, str(HOOK)], input=raw, capture_output=True)

    def test_non_dict_stdin_does_not_crash(self):
        for raw in [b"[1,2]", b'"x"', b"{broken"]:
            self.assertEqual(self.run_hook(raw).returncode, 0, raw)

    def test_outputs_context(self):
        r = self.run_hook(json.dumps({"prompt": "Soạn biên bản họp"}).encode("utf-8"))
        out = json.loads(r.stdout)["hookSpecificOutput"]
        self.assertEqual(out["hookEventName"], "UserPromptSubmit")
        self.assertIn("stop-slop-vi", out["additionalContext"])

    def test_selftest_passes(self):
        r = subprocess.run([sys.executable, str(HOOK), "--selftest"], capture_output=True)
        self.assertEqual(r.returncode, 0, r.stdout.decode("utf-8", "replace"))


if __name__ == "__main__":
    unittest.main()
