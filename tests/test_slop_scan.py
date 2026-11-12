# -*- coding: utf-8 -*-
import subprocess
import sys
import tempfile
import unicodedata
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "plugins" / "stop-slop-vi" / "skills" / "stop-slop-vi" / "scripts" / "slop_scan.py"
sys.path.insert(0, str(SCRIPT.parent))

import slop_scan as S  # noqa: E402

FILLER = "Công ty thử làm việc từ xa từ năm ngoái và năm nay mở rộng ra mọi phòng ban."  # 77 ký tự


def body(n_chars):
    """Các đoạn bình thường, tổng khoảng n_chars ký tự."""
    paras, total = [], 0
    while total < n_chars:
        paras.append(FILLER)
        total += len(FILLER)
    return paras


class Base(unittest.TestCase):
    def write(self, name, text):
        p = Path(tempfile.mkdtemp()) / name
        p.write_text(text, encoding="utf-8")
        return p

    def md(self, lines):
        return self.write("t.md", "\n\n".join(lines))

    def codes(self, lines, prose=True, info=True):
        return [h[1] for h in S.scan(self.md(lines), info, prose)]

    def levels(self, lines, prose=False):
        return {h[1]: h[0] for h in S.scan(self.md(lines), True, prose)}


class Punctuation(Base):
    def test_emdash(self):
        self.assertEqual(self.levels(["Làm việc từ xa — nhiều lợi ích."])["EMDASH"], "WARN")

    def test_spaced_endash_is_normal(self):
        self.assertFalse(self.codes(["Làm việc từ xa – nhiều lợi ích.", "Giai đoạn 2024–2026."]))

    def test_star_emoji_divide(self):
        codes = self.codes(["★ Tốc độ tìm kiếm tăng ✅", "Chia đều ÷ ba phòng."])
        for c in ["STAR", "EMOJI", "DIVIDE"]:
            self.assertIn(c, codes)

    def test_middot_list(self):
        self.assertEqual(self.levels(["Tăng tốc · thêm đặt chỗ · nhắc trả sách"])["MIDDOT_SPACED2"], "WARN")
        self.assertEqual(self.levels(["Hà Nội · tháng 11"])["MIDDOT_SPACED1"], "INFO")

    def test_space_before_punct(self):
        self.assertEqual(self.levels(["Dự án , kế hoạch và ngân sách đã duyệt ."])["SPACE_BEFORE_PUNCT"], "WARN")
        self.assertEqual(self.levels(["Cần làm gì ?"])["SPACE_BEFORE_PUNCT"], "WARN")

    def test_space_before_punct_not_ellipsis_or_code(self):
        self.assertNotIn("SPACE_BEFORE_PUNCT", self.codes(["Còn nữa ...", "Biểu thức `a ? b : c` dùng được."]))

    def test_no_space_after_comma(self):
        self.assertEqual(self.levels(["Dự án,kế hoạch đã xong."])["NO_SPACE_AFTER_PUNCT"], "INFO")
        self.assertNotIn("NO_SPACE_AFTER_PUNCT", self.codes(["Tăng 3,5% so với năm trước."]))

    def test_title_case_heading(self):
        self.assertEqual(self.levels(["# Kế Hoạch Triển Khai Dự Án", FILLER])["TITLE_CASE"], "WARN")
        self.assertEqual(self.levels(["## 1. Giới Thiệu Về Hệ Thống", FILLER])["TITLE_CASE"], "WARN")

    def test_title_case_not_sentence_case_or_caps_or_body(self):
        lines = ["# Kế hoạch triển khai dự án", "# KẾ HOẠCH TRIỂN KHAI", "# Giới thiệu Hà Nội",
                 "Báo Cáo Kết Quả Năm Nay ở trong thân bài."]
        self.assertNotIn("TITLE_CASE", self.codes(lines))

    def test_title_case_acronyms_ignored(self):
        self.assertNotIn("TITLE_CASE", self.codes(["# Tích hợp API và SSO cho cổng nội bộ"]))

    def test_quote_mix(self):
        self.assertIn("QUOTE_MIX", self.codes(["Anh ấy nói “được”.", 'Chị ấy nói "không".']))

    def test_ellipsis_mix(self):
        self.assertIn("ELLIPSIS_MIX", self.codes(["Còn nữa…", "Và còn nữa..."]))

    def test_bold_labels(self):
        lines = ["- **Mục tiêu:** tăng tốc độ", "- **Phạm vi:** toàn công ty", "- **Rủi ro:** nhân sự",
                 "- **Thời hạn:** quý một"]
        self.assertEqual(self.levels(lines)["BOLD_LABEL"], "INFO")
        self.assertNotIn("BOLD_LABEL", self.codes(lines[:2]))


class Encoding(Base):
    def test_nfd_text_warned_and_still_scanned(self):
        text = unicodedata.normalize("NFD", "Dự án — kế hoạch đã duyệt.")
        lv = self.levels([text])
        self.assertEqual(lv["NFD"], "WARN")
        self.assertIn("EMDASH", lv)

    def test_nfc_text_clean(self):
        self.assertNotIn("NFD", self.codes(["Dự án đã duyệt."]))

    def test_tone_mark_mix(self):
        self.assertEqual(self.levels(["Văn bản hòa giải.", "Bảo đảm sức khoẻ."])["TONE_MARK_MIX"], "INFO")

    def test_tone_mark_consistent(self):
        self.assertNotIn("TONE_MARK_MIX", self.codes(["Văn bản hòa giải.", "Bảo đảm sức khỏe.", "Giá quý này."]))
        self.assertNotIn("TONE_MARK_MIX", self.codes(["Văn bản hoà giải.", "Bảo đảm sức khoẻ.", "Thuỷ lợi."]))

    def test_qu_is_not_old_style(self):
        self.assertNotIn("TONE_MARK_MIX", self.codes(["Văn bản hòa giải.", "Tài sản quý."]))


class Translationese(Base):
    def test_duoc_boi(self):
        self.assertEqual(self.levels(["Hệ thống được phát triển bởi nhóm A."])["TL_BOI"], "WARN")

    def test_boi_vi_not_hit(self):
        self.assertNotIn("TL_BOI", self.codes(["Anh ấy được khen bởi vì làm nhanh.", "Đề án được duyệt."]))

    def test_co_the_noi(self):
        self.assertEqual(self.levels(["Có thể nói, đây là bước ngoặt."])["TL_COTHENOI"], "WARN")
        self.assertIn("TL_COTHENOI", self.codes(["Kết quả tốt. Có thể thấy doanh thu tăng."]))
        self.assertIn("TL_COTHENOI", self.codes(["Chúng ta có thể khẳng định rằng dự án thành công."]))

    def test_co_the_legit(self):
        self.assertNotIn("TL_COTHENOI", self.codes(["Người dùng có thể thấy nút gửi ở góc phải.",
                                                     "Trợ lý có thể nói chuyện bằng tiếng Việt."]))

    def test_viec_chain(self):
        self.assertEqual(self.levels(["Việc thực hiện việc triển khai cần một tháng."])["TL_VIEC_CHAIN"], "WARN")

    def test_viec_compound_not_chain(self):
        self.assertNotIn("TL_VIEC_CHAIN", self.codes(["Công việc của tôi là làm việc với khách."]))

    def test_info_rules(self):
        codes = self.codes(["Nhóm tiến hành kiểm tra hệ thống.", "Dữ liệu đóng vai trò quan trọng.",
                            "Đây là một trong những sản phẩm tốt nhất.", "Khó khăn trong việc tuyển dụng.",
                            "Chương trình nhằm mục đích hỗ trợ."], prose=False)
        for c in ["TL_TIENHANH", "TL_DONGVAITRO", "TL_LAMOTTRONG", "TL_DOIVOIVIEC", "TL_NHAM"]:
            self.assertIn(c, codes)

    def test_density_rules(self):
        dense = ["Nhóm xử lý một cách nhanh chóng.", "Báo cáo trình bày một cách rõ ràng.",
                 "Mọi việc diễn ra một cách suôn sẻ."]
        self.assertIn("TL_MOTCACH", self.codes(dense, prose=False))
        self.assertNotIn("TL_MOTCACH", self.codes(body(4000) + dense, prose=False))
        self.assertNotIn("TL_MOTCACH", self.codes(["Có một cách khác để làm.", "Tìm một cách để giảm chi phí.",
                                                   "Thêm một cách nữa."], prose=False))
        qua = ["Liên hệ thông qua email.", "Gửi thông qua cổng nội bộ.", "Thanh toán thông qua ví."]
        self.assertIn("TL_THONGQUA", self.codes(qua, prose=False))

    def test_info_hidden_without_flag(self):
        self.assertFalse(self.codes(["Nhóm tiến hành kiểm tra hệ thống."], info=False, prose=False))


class Filtering(Base):
    def test_english_and_code_skipped(self):
        p = self.write("t.md", "Plain English — no Vietnamese.\n\n```\nx = a — b\n```\n")
        self.assertFalse([h for h in S.scan(p, True, True)])

    def test_marker_cells_skipped(self):
        p = self.write("t.md", "| Mục | Ghi chú |\n|---|---|\n| Bảo trì | — |\n")
        self.assertNotIn("EMDASH", [h[1] for h in S.scan(p, True, False)])


class NoProseUnchanged(Base):
    def test_prose_rules_off_by_default(self):
        lines = ["Bài viết này sẽ tìm hiểu làm việc từ xa.", "Tôi nhận ra tầm quan trọng của hợp tác."]
        self.assertFalse([c for c in self.codes(lines, prose=False) if c.startswith("PROSE")])

    def test_existing_rules_still_fire_with_prose(self):
        self.assertIn("EMDASH", self.codes(["Làm việc từ xa — nhiều lợi ích."]))


class LineInfo(Base):
    def test_lesson(self):
        self.assertIn("PROSE_LESSON", self.codes(["Qua dự án, tôi nhận ra tầm quan trọng của hợp tác."]))
        self.assertIn("PROSE_LESSON", self.codes(["Đó là bài học quý giá cho cả nhóm."]))

    def test_notjust(self):
        for line in ["Đây không chỉ là bài tập mà còn là thử thách.", "Việc này không đơn thuần là tiết kiệm.",
                     "Dự án không chỉ dừng lại ở phần mềm."]:
            self.assertIn("PROSE_NOTJUST", self.codes([line]), line)

    def test_notjust_plain_not_hit(self):
        self.assertNotIn("PROSE_NOTJUST", self.codes(["Nhiệm vụ này không khó nên xong sớm."]))

    def test_empty_emph(self):
        self.assertIn("PROSE_EMPTY_EMPH", self.codes(["Tôi đã học được vô cùng nhiều điều."]))

    def test_report_cliche(self):
        self.assertIn("PROSE_CLICHE_REPORT", self.codes(["Trong bối cảnh chuyển đổi số, doanh nghiệp phải đổi mới."]))
        self.assertIn("PROSE_CLICHE_REPORT", self.codes(["Bài viết này sẽ tìm hiểu làm việc từ xa."]))

    def test_blog_cliche(self):
        self.assertIn("PROSE_CLICHE_BLOG", self.codes(["Hôm nay chúng ta cùng tìm hiểu về Docker volume."]))
        self.assertIn("PROSE_CLICHE_BLOG", self.codes(["Hy vọng bài viết hữu ích với bạn."]))

    def test_quote_open_first_paragraph_only(self):
        self.assertIn("PROSE_QUOTE_OPEN", self.codes(["# Tiêu đề", "“Thất bại là mẹ thành công”, người xưa nói vậy.", FILLER]))
        self.assertIn("PROSE_QUOTE_OPEN", self.codes(["Ông bà ta có câu: có công mài sắt có ngày nên kim.", FILLER]))
        self.assertNotIn("PROSE_QUOTE_OPEN", self.codes([FILLER, "“Thất bại là mẹ thành công”, người xưa nói vậy."]))

    def test_info_hidden_without_flag(self):
        self.assertFalse(self.codes(["Tôi nhận ra tầm quan trọng của hợp tác."], info=False))


class ThinkWarn(Base):
    T = "Tôi cho rằng cách này đúng."

    def test_variants_counted(self):
        for v in ["Tôi nghĩ rằng cách này đúng.", "Theo tôi, cách này đúng.", "Em tin rằng cách này đúng.",
                  "Theo quan điểm cá nhân, cách này đúng."]:
            self.assertIn("PROSE_THINK", self.codes(body(2000) + [v] * 3), v)

    def test_conditional_not_counted(self):
        lines = ["Nếu tôi cho rằng A đúng thì phải kiểm chứng.", "Nếu tôi nghĩ rằng B sai thì tìm phản ví dụ.",
                 "Nếu tôi tin rằng C đúng thì tăng mẫu."]
        self.assertNotIn("PROSE_THINK", self.codes(body(2000) + lines))

    def test_short_two_pass(self):
        self.assertNotIn("PROSE_THINK", self.codes(body(2000) + [self.T] * 2))

    def test_short_three_warn(self):
        hits = S.scan(self.md(body(2000) + [self.T] * 3), False, True)
        warn = [h for h in hits if h[1] == "PROSE_THINK"]
        self.assertEqual(warn[0][0], "WARN")
        self.assertIn("3 lần", warn[0][3])

    def test_long_three_pass(self):
        self.assertNotIn("PROSE_THINK", self.codes(body(15000) + [self.T] * 3))

    def test_long_dense_warn(self):
        self.assertIn("PROSE_THINK", self.codes(body(15000) + [self.T] * 7))


class ConnectorWarn(Base):
    C = "Bên cạnh đó, làm việc từ xa giảm thời gian đi lại."

    def test_three_of_six_warn(self):
        self.assertIn("PROSE_CONNECTOR", self.codes([FILLER] * 3 + [self.C] * 3))

    def test_three_of_twenty_pass(self):
        self.assertNotIn("PROSE_CONNECTOR", self.codes([FILLER] * 17 + [self.C] * 3))

    def test_two_pass(self):
        self.assertNotIn("PROSE_CONNECTOR", self.codes([FILLER] * 2 + [self.C] * 2))

    def test_headings_not_counted(self):
        lines = ["# Phần một", "# Phần hai", "# Phần ba", "# Phần bốn"] + [FILLER] * 6 + [self.C] * 3
        self.assertIn("PROSE_CONNECTOR", self.codes(lines))


class ParagraphGrouping(Base):
    C3 = ["Ngoài ra, một.", "Hơn nữa, hai.", "Do đó, ba."]

    def test_md_wrapped_lines_are_one_paragraph(self):
        p = self.write("t.md", FILLER + "\n" + "\n".join(self.C3) + "\n")
        self.assertNotIn("PROSE_CONNECTOR", [h[1] for h in S.scan(p, True, True)])

    def test_blank_line_paragraphs_in_one_cell(self):
        paras = [("A1", "\n\n".join([FILLER] + self.C3))]
        self.assertIn("PROSE_CONNECTOR", [h[1] for h in S.prose_totals(S.split_paragraphs(paras), True)])

    def test_md_table_cells_not_counted(self):
        table = "\n".join(["| Mục | Mô tả |", "|---|---|"] + [f"| Mục {i} | Mô tả ở đây |" for i in range(4)])
        p = self.write("t.md", "\n\n".join([FILLER] + self.C3) + "\n\n" + table + "\n")
        self.assertIn("PROSE_CONNECTOR", [h[1] for h in S.scan(p, True, True)])

    def test_txt_single_newline_paragraphs(self):
        p = self.write("t.txt", "\n".join([FILLER] + self.C3) + "\n")
        self.assertIn("PROSE_CONNECTOR", [h[1] for h in S.scan(p, True, True)])

    def test_front_matter_skipped(self):
        p = self.write("t.md", "---\ntitle: Cảm nhận công cụ mới\n---\n\n“Thất bại là mẹ thành công”, người xưa nói.\n")
        self.assertIn("PROSE_QUOTE_OPEN", [h[1] for h in S.scan(p, True, True)])

    def test_front_matter_still_scanned_without_prose(self):
        p = self.write("t.md", "---\ntitle: Làm việc từ xa — cảm nhận\n---\n")
        self.assertIn("EMDASH", [h[1] for h in S.scan(p, False, False)])


class ReviewFalsePositives(Base):
    def test_unit_signs_not_nfd(self):
        self.assertNotIn("NFD", self.codes(["Điện trở 10 Ω mắc nối tiếp.", "Nhiệt độ 300 K ổn định."]))

    def test_title_case_names_hashtags_code(self):
        for line in ["## Bà Rịa Vũng Tàu", "## Nguyễn Thị Minh Khai", "#ViệtNam #DuLịch #ẨmThực #HàNội",
                     "## Lệnh `git` `add` `commit` trên máy chủ"]:
            self.assertNotIn("TITLE_CASE", self.codes([line, FILLER]), line)
        self.assertIn("TITLE_CASE", self.codes(["# Giới Thiệu Về Hệ Thống", FILLER]))

    def test_co_the_noi_chuyen_and_ui(self):
        self.assertNotIn("TL_COTHENOI", self.codes(["Có thể nói chuyện trực tiếp với bộ phận hỗ trợ.",
                                                     "Người dùng có thể thấy rằng nút Lưu đã sáng."]))

    def test_co_the_after_opener_or_bullet(self):
        self.assertIn("TL_COTHENOI", self.codes(["Như vậy, có thể thấy doanh thu tăng."]))
        self.assertIn("TL_COTHENOI", self.codes(["- Có thể thấy doanh thu tăng."]))

    def test_boi_causal(self):
        for line in ["Dự án được duyệt nhanh bởi ai cũng thấy lợi ích.", "Sản phẩm được đánh giá cao bởi nó rẻ."]:
            self.assertNotIn("TL_BOI", self.codes([line]), line)
        self.assertIn("TL_BOI", self.codes(["Sản phẩm được đánh giá cao bởi thế giới."]))

    def test_viec_lists_and_job(self):
        for line in ["Nhân viên cần ưu tiên việc gấp, việc quan trọng trước.",
                     "Chương trình hỗ trợ việc tìm việc làm cho sinh viên.", "Không ai biết việc này, việc kia."]:
            self.assertNotIn("TL_VIEC_CHAIN", self.codes([line]), line)

    def test_ratio_colon(self):
        self.assertNotIn("SPACE_BEFORE_PUNCT", self.codes(["Bản đồ tỷ lệ 1 : 25.000 dùng cho khảo sát."]))

    def test_dialogue_dash(self):
        self.assertNotIn("EMDASH", self.codes(["— Anh đi đâu đấy?", "  — Em về quê."]))

    def test_think_overcount(self):
        lines = ["Nếu chúng tôi cho rằng A đúng thì kiểm chứng.", "Nhiều người xem tin rằng phim hay.",
                 "Khán giả xem cho rằng phim dài."]
        self.assertNotIn("PROSE_THINK", self.codes(body(2000) + lines))

    def test_bom(self):
        p = self.write("t.md", "﻿# Kế Hoạch Triển Khai Dự Án Mới\n\n" + FILLER + "\n")
        self.assertIn("TITLE_CASE", [h[1] for h in S.scan(p, True, False)])

    def test_bad_xlsx_is_input_error(self):
        import zipfile
        p = Path(tempfile.mkdtemp()) / "t.xlsx"
        ns = 'xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"'
        rns = 'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
        with zipfile.ZipFile(p, "w") as z:
            z.writestr("xl/workbook.xml", f'<workbook {ns} {rns}><sheets><sheet name="A" r:id="r1"/></sheets></workbook>')
            z.writestr("xl/_rels/workbook.xml.rels", '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="r1" Target="worksheets/sheet1.xml"/></Relationships>')
            z.writestr("xl/sharedStrings.xml", f"<sst {ns}><si><t>Dự án</t></si></sst>")
            z.writestr("xl/worksheets/sheet1.xml", f'<worksheet {ns}><sheetData><row><c r="A1" t="s"><v>5</v></c></row></sheetData></worksheet>')
        r = subprocess.run([sys.executable, str(SCRIPT), str(p)], capture_output=True)
        self.assertEqual(r.returncode, 2, r.stdout.decode("utf-8", "replace"))


class Cli(Base):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True)

    def test_exit_codes(self):
        p = self.md(body(2000) + ["Tôi cho rằng nó đúng."] * 3)
        self.assertEqual(self.run_cli(str(p)).returncode, 0)
        self.assertEqual(self.run_cli(str(p), "--prose").returncode, 1)
        self.assertEqual(self.run_cli("khong-co.md").returncode, 2)

    def test_examples(self):
        ex = ROOT / "examples"
        self.assertEqual(self.run_cli(str(ex / "before.md")).returncode, 1)
        self.assertEqual(self.run_cli(str(ex / "after.md")).returncode, 0)


if __name__ == "__main__":
    unittest.main()
