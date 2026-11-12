# -*- coding: utf-8 -*-
"""Scanner dấu hiệu còn sót của stop-slop-vi.

Tách nội dung docx/pptx/xlsx/md/txt/html theo đoạn (ô) và chỉ tìm những dấu hiệu máy đo được
trong references/vi-slop-patterns.md. Sáo ngữ và nhịp câu do người (mô hình) đọc và quyết.

usage: python slop_scan.py FILE [FILE ...] [--info] [--prose] [--out report.txt]
exit : 0 = không có WARN (PASS), 1 = có WARN (FAIL), 2 = lỗi đầu vào
"""
import argparse
import html
import posixpath
import re
import sys
import unicodedata
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
S = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
PR = "{http://schemas.openxmlformats.org/package/2006/relationships}"

TABLE = "(bảng)"
WHOLE = "(toàn văn bản)"

# Chữ cái chỉ tiếng Việt mới có (sau NFC). Đoạn không có chữ nào như vậy (tiếng Anh, code) thì bỏ qua.
VIET = re.compile("[ăâđêôơưàáảãạằắẳẵặầấẩẫậèéẻẽẹềếểễệìíỉĩịòóỏõọồốổỗộờớởỡợùúủũụừứửữựỳýỷỹỵ]", re.I)
COMBINING = re.compile(r"[\u0300-\u036f]")  # dấu thanh/dấu phụ dạng tổ hợp (NFD)
EMOJI = re.compile("[✅❌❎✨⭐\U0001F300-\U0001FAFF]")
# Cách trước dấu câu: "dự án , kế hoạch", "xong ." Không bắt " ..." (dấu chấm lửng) và ":)".
SPACE_PUNCT = re.compile(r"""[\w)\]"'”’] +(?:[,.;!?]|:(?!\s*\d))(?=\s|$)""")
NO_SPACE_PUNCT = re.compile(r"(?<=[^\W\d_])[,;](?=[^\W\d_])")
# Không gắn \b ở cuối: Python coi dấu thanh tổ hợp (nếu còn sót) là ký tự từ.
COTHENOI = re.compile(r"(?:^\s*(?:[-*+]\s+)?|[.!?:]\s+|(?:như vậy|qua đó|từ đó|nhìn chung|tóm lại|do đó|vì vậy),\s*|"
                      r"(?<!\w)(?:chúng ta|người ta|ta) )có thể (nói|thấy|khẳng định)(?!\w)(?! (chuyện|rõ|dối|thật|được))", re.I)
VIEC = (r"(?<!công )(?<!làm )(?<!mọi )(?<!tìm )(?<!xin )(?<!nhận )(?<!giao )(?<!nghỉ )(?<!thôi )"
        r"(?<![\w])việc")

# (mã, mức, regex, gợi ý). Chạy trên văn bản đã chuẩn hóa NFC.
RULES = [
    ("EMDASH", "WARN", re.compile(r"(?<=\S)\s*—"), "em-dash trong câu: dùng ' – ', dấu phẩy, ngoặc hoặc tách câu"),
    ("STAR", "WARN", re.compile(r"[★☆]"), "sao trang trí: xóa (nhấn mạnh bằng in đậm/màu)"),
    ("EMOJI", "WARN", EMOJI, "emoji trang trí: xóa"),
    ("DIVIDE", "WARN", re.compile(r"÷"), "ký hiệu toán: viết bằng lời"),
    ("MIDDOT_SPACED2", "WARN", re.compile(r"[  ]·[  ].*[  ]·[  ]"), "liệt kê bằng ' · ': dùng dấu phẩy hoặc chấm phẩy"),
    ("MIDDOT_DOUBLE", "WARN", re.compile(r" {2,}·|· {2,}"), "cách đôi quanh dấu phân cách: dùng một dấu"),
    ("SPACE_BEFORE_PUNCT", "WARN", SPACE_PUNCT, "cách trước dấu câu: viết liền ('dự án, kế hoạch')"),
    ("TL_BOI", "WARN", re.compile(r"được(\s+[^\s,.;:!?]+){1,5}?\s+bởi(?!\s+((vì|lẽ|vậy|đó|nó|ai|họ|tôi|chúng|mình|anh|chị|em|"
                r"người ta)(?!\w)|thế(?!\s+giới)))", re.I),
     "văn dịch 'được … bởi': đưa tác nhân lên làm chủ ngữ"),
    ("TL_COTHENOI", "WARN", COTHENOI, "văn dịch 'có thể nói/thấy': khẳng định thẳng"),
    ("TL_VIEC_CHAIN", "WARN", re.compile(VIEC + r"\s+[^\s,;]+(\s+[^\s,;]+)?\s+" + VIEC, re.I),
     "'việc … việc' chồng danh từ hóa: bỏ chữ 'việc' thừa"),
    ("TL_TIENHANH", "INFO", re.compile(r"tiến hành\s+(?=\w)", re.I), "'tiến hành + động từ': dùng động từ luôn"),
    ("TL_DONGVAITRO", "INFO", re.compile(r"đóng\s+(một\s+)?vai trò", re.I), "'đóng vai trò': nói nó làm việc gì"),
    ("TL_LAMOTTRONG", "INFO", re.compile(r"là một trong (những|các)\b[^.!?\n]{0,40}\bnhất", re.I),
     "'là một trong những … nhất': nói thẳng hoặc dẫn số liệu"),
    ("TL_DOIVOIVIEC", "INFO", re.compile(r"(đối với|trong) việc(?!\w)", re.I), "'đối với/trong việc': bỏ hoặc đổi chủ ngữ"),
    ("TL_NHAM", "INFO", re.compile(r"nhằm mục đích", re.I), "'nhằm mục đích': dùng 'để'"),
    ("MIDDOT_SPACED1", "INFO", re.compile(r"[  ]·[  ]"), "một dấu ' · ': giữ nếu là phân cách hai thuộc tính"),
    ("NO_SPACE_AFTER_PUNCT", "INFO", NO_SPACE_PUNCT, "thiếu cách sau dấu phẩy/chấm phẩy"),
]

# Đếm theo mật độ: một lần là bình thường, dày đặc mới là dấu hiệu. (mã, regex, tối thiểu, ký tự trên mỗi lần, gợi ý)
DENSITY_RULES = [
    ("TL_MOTCACH", re.compile(r"một cách (?!(khác|để|nào|mà|này|đó|nữa|mới|giải|làm)(?!\w))\w", re.I), 3, 1000,
     "'một cách + tính từ' dày đặc: bỏ 'một cách'"),
    ("TL_THONGQUA", re.compile(r"thông qua", re.I), 3, 1000, "'thông qua' dày đặc: 'qua', 'bằng', 'nhờ'"),
]

# --prose: văn tự sự (tiểu luận, bài luận, blog, bình luận). Theo dòng là INFO, người quyết.
PROSE_RULES = [
    ("PROSE_LESSON", "INFO",
     re.compile(r"(nhận ra|hiểu ra|hiểu được|thấm thía)\s+(được\s+)?(tầm quan trọng|giá trị|ý nghĩa)|"
                r"bài học (quý giá|đắt giá|rút ra)|rút ra (được\s+)?(bài học|nhiều điều)|"
                r"giúp (tôi|em|mình|chúng tôi|chúng em) (hiểu|nhận ra)", re.I),
     "kết bằng bài học: thay bằng việc làm/sự thật thay đổi sau đó"),
    ("PROSE_NOTJUST", "INFO",
     re.compile(r"không (chỉ|đơn thuần|đơn giản|phải) là\b[^.!?\n]{0,40}?mà (còn|là)|"
                r"không chỉ dừng lại ở|không (đơn thuần|chỉ đơn thuần|đơn giản) là", re.I),
     "khung 'không chỉ là … mà còn': chỉ giữ vế có nội dung"),
    ("PROSE_EMPTY_EMPH", "INFO", re.compile(r"(?<!\w)(thực sự|thật sự|vô cùng|cực kỳ|hết sức|vô cùng)(?!\w)", re.I),
     "từ nhấn rỗng: xóa hoặc thay bằng số liệu, sự thật"),
    ("PROSE_CLICHE_REPORT", "INFO",
     re.compile(r"trong bối cảnh|trong kỷ nguyên|trong thời đại (số|công nghệ|4\.0|ngày nay)|"
                r"cùng với sự phát triển (không ngừng|mạnh mẽ)|"
                r"bài (viết|báo cáo|tiểu luận) này (sẽ\s+)?(tìm hiểu|trình bày|phân tích|làm rõ)|"
                r"tóm lại,? có thể (thấy|nói)", re.I),
     "sáo ngữ báo cáo: vào thẳng luận điểm, sự thật"),
    ("PROSE_CLICHE_BLOG", "INFO",
     re.compile(r"hôm nay,? (chúng ta|mình|tôi|chúng mình)( sẽ)? cùng (nhau\s+)?(tìm hiểu|khám phá)|"
                r"h[yi] vọng bài viết|đừng quên (like|chia sẻ|theo dõi|đăng ký)|cùng bắt đầu nào|mẹo hay", re.I),
     "sáo ngữ blog: bỏ lời chào, vào nội dung"),
]
QUOTE_OPEN = re.compile(r"^\s*(>\s*)?[“\"‘']|theo (từ điển|định nghĩa)|có (một\s+)?câu nói|"
                        r"(người xưa|ông bà( ta)?|ông cha( ta)?) (có câu|đã nói|dạy)|như [^.\n]{1,30} (đã\s+)?từng nói", re.I)
# "nếu tôi cho rằng …" là mệnh đề điều kiện, không phải ý kiến.
THINK = re.compile(r"(?<!nếu )(?<!nếu chúng )(?<!\w)(tôi|em|mình|chúng tôi)\s+(cho rằng|nghĩ rằng|nghĩ là|tin rằng|thấy rằng)|"
                   r"theo (quan điểm|ý kiến) (của\s+)?(tôi|em|mình|cá nhân)|(?<!\w)theo (tôi|em|mình),", re.I)
CONNECTOR = re.compile(r"^\s*(bên cạnh đó|ngoài ra|hơn nữa|đồng thời|tóm lại|nhìn chung|không những thế|"
                       r"thêm vào đó|do đó|vì vậy|từ đó)[,\s]", re.I)
# Một văn bản tiếng Việt dài hơn bản tiếng Hàn cùng nội dung khoảng 2,5 lần về số ký tự.
THINK_MIN, THINK_PER_CHARS = 3, 2500
CONNECTOR_MIN, CONNECTOR_RATIO = 3, 0.25

# Hai kiểu bỏ dấu: "hòa, khỏe, thúy" (truyền thống) và "hoà, khoẻ, thuý" (theo QĐ 240/1984).
# Chỉ xét âm tiết mở (không phụ âm cuối).
TONE_NEW = re.compile(r"(?<!\w)\w*([òóỏõọ][ae]|(?<!q)[ùúủũụ]y)(?!\w)", re.I)
TONE_OLD = re.compile(r"(?<!\w)\w*(o[àáảãạèéẻẽẹ]|(?<!q)u[ỳýỷỹỵ])(?!\w)", re.I)
BOLD_LABEL = re.compile(r"^\s*([-*+]|\d+[.)])?\s*\*\*[^*\n]{1,40}(:\*\*|\*\*\s*:)")
BOLD_LABEL_MIN = 4
TITLE_MIN_WORDS = 4
TITLE_LONG = 6


HEADING = re.compile(r"^\s*#{1,6}(\s|$)")
# Hư từ: tiêu đề Title Case thường viết hoa cả chúng; tên riêng nhiều âm tiết thì không có.
FUNCTION_WORDS = {"và", "của", "cho", "các", "những", "với", "trong", "về", "theo", "để", "từ", "đến", "tại",
                  "trên", "khi", "là", "một", "hoặc", "hay"}


def is_heading(text):
    return bool(HEADING.match(text))


def title_case(text):
    """Tiêu đề md viết hoa mọi chữ đầu (kiểu tiếng Anh). Bỏ qua viết tắt và tiêu đề viết hoa toàn bộ."""
    words = re.findall(r"[^\W\d_]+", HEADING.sub("", text, count=1))
    if len(words) < TITLE_MIN_WORDS:
        return False
    plain = [w for w in words if not (w.isupper() and len(w) > 1)]
    if len(plain) < TITLE_MIN_WORDS - 1 or all(w.isupper() for w in words):
        return False
    if not all(w[0].isupper() for w in plain):
        return False
    # Tên riêng (Bà Rịa Vũng Tàu, Nguyễn Thị Minh Khai) cũng viết hoa từng âm tiết: cần hư từ viết hoa hoặc tiêu đề dài
    return len(plain) >= TITLE_LONG or any(w.lower() in FUNCTION_WORDS for w in plain)


LIST_ITEM = re.compile(r"^\s*([-*+]|\d+[.)])\s")


def front_matter_end(path):
    """Dòng cuối của phần đầu md (--- ... ---). Không có thì 0."""
    lines = Path(path).read_text(encoding="utf-8-sig").splitlines()
    if not lines or lines[0].strip() != "---":
        return 0
    for n, line in enumerate(lines[1:], 2):
        if line.strip() == "---":
            return n
    return 0


def split_paragraphs(paras, group_lines=False, skip_until=0):
    """Danh sách đoạn để chấm. Dòng trống trong một ô tách đoạn; md gom các dòng liền nhau thành một đoạn.
    Dòng tiêu đề và mục danh sách đếm riêng; ô bảng và phần đầu md (đến dòng skip_until) không tính là đoạn."""
    out, prev_n = [], None
    for where, text in paras:
        if where.endswith(TABLE):
            prev_n = None
            continue
        line_no = re.match(r"L(\d+)", where)
        if line_no and int(line_no.group(1)) <= skip_until:
            continue
        m = re.fullmatch(r"L(\d+)", where) if group_lines else None
        n = int(m.group(1)) if m else None
        alone = is_heading(text) or LIST_ITEM.match(text)
        if (n is not None and prev_n is not None and n == prev_n + 1 and not alone and out
                and not is_heading(out[-1][1]) and not LIST_ITEM.match(out[-1][1])):
            out[-1] = (out[-1][0], out[-1][1] + " " + text.strip())
        else:
            out.extend((where, part) for part in re.split(r"\n\s*\n", text) if VIET.search(part))
        prev_n = n
    return out


def prose_totals(paras, show_info):
    """Dấu hiệu văn tự sự tính trên toàn văn bản. paras = [(where, text)] (đoạn thân bài có tiếng Việt)."""
    hits = []
    body = [(w, t) for w, t in paras if not is_heading(t)]
    if not body:
        return hits
    first_w, first_t = body[0]
    if show_info and QUOTE_OPEN.search(first_t):
        hits.append(("INFO", "PROSE_QUOTE_OPEN", first_w, first_t.strip()[:50],
                     "mở bằng danh ngôn/định nghĩa từ điển: mở bằng cảnh, sự thật"))
    chars = sum(len(t) for _w, t in body)
    think = sum(len(THINK.findall(t)) for _w, t in body)
    if think >= THINK_MIN and think * THINK_PER_CHARS >= chars:
        rate = think * 1000 / chars
        hits.append(("WARN", "PROSE_THINK", WHOLE,
                     f"'tôi cho rằng' {think} lần / {rate:.1f} lần mỗi 1.000 ký tự ({chars} ký tự)",
                     "nói bằng sự thật, việc làm hoặc khẳng định"))
    conn = sum(1 for _w, t in body if CONNECTOR.search(t))
    if conn >= CONNECTOR_MIN and conn >= CONNECTOR_RATIO * len(body):
        hits.append(("WARN", "PROSE_CONNECTOR", WHOLE, f"{conn} trên {len(body)} đoạn mở bằng liên từ",
                     "chỉ giữ liên từ ở chỗ thật cần"))
    return hits


def doc_totals(paras, show_info):
    """Dấu hiệu tính trên toàn văn bản, không phụ thuộc --prose."""
    if not show_info:
        return []
    hits = []
    texts = [t for _w, t in paras]
    joined = "\n".join(texts)
    chars = max(1, len(joined))
    for code, rx, min_n, per_chars, hint in DENSITY_RULES:
        n = len(rx.findall(joined))
        if n >= min_n and n * per_chars >= chars:
            hits.append(("INFO", code, WHOLE, f"{n} lần trong {chars} ký tự", hint))
    curly = len(re.findall(r"[“”]", joined))
    straight = joined.count('"')
    if curly and straight:
        hits.append(("INFO", "QUOTE_MIX", WHOLE, f"ngoặc cong {curly} / ngoặc thẳng {straight}",
                     "thống nhất theo quy ước sẵn có của văn bản"))
    if "…" in joined and "..." in joined:
        hits.append(("INFO", "ELLIPSIS_MIX", WHOLE, "lẫn '…' và '...'", "thống nhất một kiểu"))
    new, old = TONE_NEW.search(joined), TONE_OLD.search(joined)
    if new and old:
        hits.append(("INFO", "TONE_MARK_MIX", WHOLE, f"kiểu '{new.group(0)}' / kiểu '{old.group(0)}'",
                     "thống nhất một kiểu bỏ dấu (hòa/hoà, khỏe/khoẻ, thúy/thuý)"))
    labels = sum(1 for t in texts if BOLD_LABEL.match(t))
    if labels >= BOLD_LABEL_MIN:
        hits.append(("INFO", "BOLD_LABEL", WHOLE, f"{labels} dòng mở bằng '**Nhãn:**'",
                     "định dạng kiểu chatbot: cân nhắc viết thành câu hoặc bảng"))
    return hits


def is_marker(text):
    """Ô bảng chỉ có ký hiệu 'không áp dụng' (—, -, ―)."""
    return text.strip() in {"—", "-", "―", "–", "N/A"}


def parent_map(root):
    return {c: p for p in root.iter() for c in p}


def paragraphs_xml(root, p_tag, t_tag):
    """Gom phần tử t về tổ tiên p gần nhất (tách cả đoạn lồng trong textbox)."""
    parents = parent_map(root)
    order, buf = [], {}
    for p in root.iter(p_tag):
        order.append(p)
        buf[p] = []
    for t in root.iter(t_tag):
        node = parents.get(t)
        while node is not None and node.tag != p_tag:
            node = parents.get(node)
        if node is not None and t.text:
            buf[node].append(t.text)
    return [(i, "".join(buf[p]), p, parents) for i, p in enumerate(order, 1)]


def has_ancestor(node, parents, tag):
    node = parents.get(node)
    while node is not None:
        if node.tag == tag:
            return True
        node = parents.get(node)
    return False


def rels(z, path):
    base = posixpath.dirname(path)
    rp = posixpath.join(base, "_rels", posixpath.basename(path) + ".rels")
    if rp not in z.namelist():
        return {}
    out = {}
    for r in ET.fromstring(z.read(rp)).iter(PR + "Relationship"):
        tgt = r.get("Target")
        out[r.get("Id")] = tgt.lstrip("/") if tgt.startswith("/") else posixpath.normpath(posixpath.join(base, tgt))
    return out


def extract_docx(path):
    with zipfile.ZipFile(path) as z:
        parts = ["word/document.xml"] + sorted(
            n for n in z.namelist() if re.match(r"word/(header|footer|footnotes|endnotes)\d*\.xml$", n))
        for part in parts:
            if part not in z.namelist():
                continue
            root = ET.fromstring(z.read(part))
            label = "thân" if part == "word/document.xml" else Path(part).stem
            for i, text, p, parents in paragraphs_xml(root, W + "p", W + "t"):
                where = f"{label} p{i}" + (f" {TABLE}" if has_ancestor(p, parents, W + "tc") else "")
                yield where, text


def extract_pptx(path):
    with zipfile.ZipFile(path) as z:
        prs = ET.fromstring(z.read("ppt/presentation.xml"))
        rmap = rels(z, "ppt/presentation.xml")
        slides = [rmap[s.get(R + "id")] for s in prs.iter(
            "{http://schemas.openxmlformats.org/presentationml/2006/main}sldId")]
        for n, part in enumerate(slides, 1):
            root = ET.fromstring(z.read(part))
            for i, text, p, parents in paragraphs_xml(root, A + "p", A + "t"):
                where = f"slide{n} p{i}" + (f" {TABLE}" if has_ancestor(p, parents, A + "tc") else "")
                yield where, text


def extract_xlsx(path):
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        shared = []
        if "xl/sharedStrings.xml" in names:
            for si in ET.fromstring(z.read("xl/sharedStrings.xml")).iter(S + "si"):
                phonetic = {t for rph in si.iter(S + "rPh") for t in rph.iter(S + "t")}
                shared.append("".join(t.text or "" for t in si.iter(S + "t") if t not in phonetic))
        wb = ET.fromstring(z.read("xl/workbook.xml"))
        rmap = rels(z, "xl/workbook.xml")
        for sh in wb.iter(S + "sheet"):
            part = rmap.get(sh.get(R + "id"))
            if not part or part not in names:
                continue
            name = sh.get("name")
            for c in ET.fromstring(z.read(part)).iter(S + "c"):
                t, v = c.get("t"), c.find(S + "v")
                if t == "s" and v is not None:
                    text = shared[int(v.text)]
                elif t == "inlineStr":
                    text = "".join(x.text or "" for x in c.iter(S + "t"))
                elif t == "str" and v is not None:
                    text = v.text or ""
                else:
                    continue
                yield f"{name}!{c.get('r')}", text
        for part in sorted(n for n in names if re.match(r"xl/drawings/drawing\d+\.xml$", n)):
            root = ET.fromstring(z.read(part))
            for i, text, _p, _par in paragraphs_xml(root, A + "p", A + "t"):
                yield f"{Path(part).stem}(hình) p{i}", text


def extract_md(path):
    fence = False
    for n, line in enumerate(Path(path).read_text(encoding="utf-8-sig").splitlines(), 1):
        if line.lstrip().startswith(("```", "~~~")):
            fence = not fence
            continue
        if fence:
            continue
        # Code inline thay bằng "0": xóa hẳn thì "file `a.zip` ," thành "file  ," và báo nhầm; chữ số không bị tính là từ viết hoa
        line = re.sub(r"`[^`]*`", "0", line)
        if line.strip().startswith("|"):
            for k, cell in enumerate(line.strip().strip("|").split("|"), 1):
                if not re.fullmatch(r"\s*:?-{2,}:?\s*", cell):
                    yield f"L{n} c{k} {TABLE}", cell.strip()
        else:
            yield f"L{n}", line


def extract_html(path):
    src = Path(path).read_text(encoding="utf-8-sig")
    src = re.sub(r"(?is)<(script|style|pre|code)\b.*?</\1>", " ", src)
    src = re.sub(r"(?i)<(br|/p|/div|/li|/h\d|/td|/th|/tr)\b[^>]*>", "\n", src)
    for n, line in enumerate(html.unescape(re.sub(r"<[^>]+>", "", src)).splitlines(), 1):
        if line.strip():
            yield f"L{n}", line


EXTRACTORS = {".docx": extract_docx, ".pptx": extract_pptx, ".xlsx": extract_xlsx, ".xlsm": extract_xlsx,
              ".md": extract_md, ".txt": extract_md, ".html": extract_html, ".htm": extract_html}


def snippet(text, m):
    s, e = max(0, m.start() - 25), min(len(text), m.end() + 25)
    return ("…" if s else "") + text[s:e].replace("\n", " ") + ("…" if e < len(text) else "")


def scan_line(where, text, rules, show_info, is_md):
    hits, seen_middot2 = [], False
    for code, level, rx, hint in rules:
        if code == "MIDDOT_SPACED1" and seen_middot2:
            continue
        m = rx.search(text)
        if not m:
            continue
        if code == "MIDDOT_SPACED2":
            seen_middot2 = True
        if level == "INFO" and not show_info:
            continue
        hits.append((level, code, where, snippet(text, m), hint))
    if is_md and is_heading(text) and title_case(text):
        hits.append(("WARN", "TITLE_CASE", where, text.strip()[:60],
                     "tiêu đề tiếng Việt viết hoa kiểu câu: chỉ viết hoa chữ đầu và tên riêng"))
    return hits


def scan(path, show_info, prose=False):
    hits, paras, nfd = [], [], []
    rules = RULES + PROSE_RULES if prose else RULES
    is_md = path.suffix.lower() in {".md", ".txt"}
    for where, raw in EXTRACTORS[path.suffix.lower()](path):
        text = unicodedata.normalize("NFC", raw)
        if not text.strip() or is_marker(text):
            continue
        # Đoạn không có chữ tiếng Việt (tiếng Anh thuần, code) không phải đối tượng
        if not VIET.search(text):
            continue
        if COMBINING.search(raw):
            nfd.append(where)
        paras.append((where, text))
        hits.extend(scan_line(where, text, rules, show_info, is_md))
    if nfd:
        hits.append(("WARN", "NFD", WHOLE, f"{len(nfd)} đoạn dùng dấu tổ hợp (NFD), đầu tiên ở {nfd[0]}",
                     "chuẩn hóa về NFC (dựng sẵn) để tìm kiếm, sắp xếp không lỗi"))
    hits.extend(doc_totals(paras, show_info))
    if prose:
        # txt thường là văn bản dán từ form web, mỗi dòng một đoạn, nên không gom dòng
        is_md_file = path.suffix.lower() == ".md"
        skip = front_matter_end(path) if is_md_file else 0
        hits.extend(prose_totals(split_paragraphs(paras, is_md_file, skip), show_info))
    return hits


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+")
    ap.add_argument("--info", action="store_true", help="hiện cả mục INFO (cần người quyết)")
    ap.add_argument("--prose", action="store_true", help="kiểm tra thêm quy tắc văn tự sự (tiểu luận, blog, bình luận)")
    ap.add_argument("--out", help="lưu báo cáo ra file UTF-8 (tránh lỗi font console)")
    args = ap.parse_args()

    lines, total_warn, bad_input = [], 0, False
    for f in args.files:
        path = Path(f)
        if path.name.startswith("~$"):
            continue
        if not path.is_file() or path.suffix.lower() not in EXTRACTORS:
            lines.append(f"[SKIP] {f}: không có file hoặc định dạng không hỗ trợ")
            bad_input = True
            continue
        try:
            hits = scan(path, args.info, args.prose)
        except (zipfile.BadZipFile, ET.ParseError, KeyError, IndexError, ValueError, TypeError, OSError,
                RuntimeError, UnicodeDecodeError) as e:
            lines.append(f"[ERROR] {f}: {type(e).__name__}: {e}")
            bad_input = True
            continue
        warn = sum(1 for h in hits if h[0] == "WARN")
        total_warn += warn
        lines.append(f"== {path.name}: WARN {warn}, INFO {len(hits) - warn}")
        for level, code, where, snip, hint in hits:
            lines.append(f"  [{level}] {code} @ {where}: {snip}\n         -> {hint}")
    lines.append(f"RESULT: {'FAIL' if total_warn else 'PASS'} (WARN {total_warn})")

    report = "\n".join(lines)
    if args.out:
        Path(args.out).write_text(report + "\n", encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(report)
    sys.exit(2 if bad_input and not total_warn else (1 if total_warn else 0))


if __name__ == "__main__":
    main()
