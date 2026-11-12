#!/usr/bin/env python3
# UserPromptSubmit hook: yêu cầu viết, sửa tài liệu tiếng Việt thì chèn ngữ cảnh nhắc thứ tự dùng skill.
#   Tài liệu chia sẻ có đối tượng đọc cụ thể -> stakeholder-brief trước, stop-slop-vi sau cùng
#   Tài liệu khác                           -> chế độ tạo mới của stop-slop-vi
# Điều kiện: (từ khóa tài liệu hoặc đối tượng đọc) + động từ viết. So khớp trên chuỗi đã bỏ dấu,
# nên gõ không dấu ("soan bao cao") cũng nhận ra. `--selftest` in bảng tự kiểm.
import sys, json, re, unicodedata
from pathlib import Path


def fold_char(c):
    if c in "đĐ":
        return "d"
    base = [b for b in unicodedata.normalize("NFD", c) if unicodedata.category(b) != "Mn"]
    return base[0].lower() if len(base) == 1 else c.lower()


def fold(text):
    """Bỏ dấu, chữ thường, giữ nguyên độ dài (để lấy lại từ khóa có dấu từ chuỗi gốc)."""
    return "".join(fold_char(c) for c in unicodedata.normalize("NFC", text))


def rx(pattern):
    return re.compile(pattern, re.I)


# Loại tài liệu chắc chắn: kể cả trong ngữ cảnh code ("viết README cho repo") vẫn là viết tài liệu.
DOC_ONLY = (r"bien ban|to trinh|cong van|giay moi|readme|huong dan su dung|dac ta|"
            r"tai lieu (api|ky thuat|thiet ke|huong dan|dac ta|du an)|(ban|file) huong dan|"
            r"quyet dinh (so|ve viec|bo nhiem|phe duyet|khen thuong|ky luat)|(du thao|ban) (quyet dinh|quy dinh|de an)")
DOC_STRONG = rx(r"\b(" + DOC_ONLY + r"|bao cao|quy che|(ban|to|van ban) de xuat|"
                r"de xuat (du an|kinh phi|ngan sach|giai phap)|de an (du an|phat trien|kinh doanh|tuyen sinh)|"
                r"slides?|pptx?|powerpoint|docx|xlsx|bang tinh|markdown|file md)\b|\.md\b")
DOC_ONLY_RX = rx(r"\b(" + DOC_ONLY + r")\b")
# Từ khóa tài liệu dễ trùng với yêu cầu code ("tạo function gửi email"): chỉ tính khi không có ngữ cảnh code.
DOC_WEAK = rx(r"\b(tai lieu|thong bao(?! loi(?! nhuan))|ke hoach|e-?mail|mail|"
              r"thu (moi|cam on|xin|tra loi|phan hoi|ngo|chao)|excel|word|van ban)\b")
CODE = rx(r"\b(code|bug|build|gradle|function|class|component|api|endpoint|unit test|test|refactor|commit|"
          r"deploy|script|module|repo|pull request|database|sql|schema|query|log|cache|redis|"
          r"docker|git|pandas|python|javascript|typescript|react|css|app|web|website|server|"
          r"ham|lap trinh|ung dung|giao dien|nut|tinh nang|chuc nang|co so du lieu|bien so|bien moi truong|"
          r"vong lap|tai khoan|man hinh|may chu|trang (web|chu|dang nhap|blog)|"
          r"(sua|fix|bat|bi|gap|xu ly|khac phuc) loi(?! chinh ta)|loi (build|parse|hien thi|dang nhap))\b")
AUDIENCE = rx(r"\bcho (lanh dao|ban giam doc|giam doc|sep|cap tren|khach hang|doi tac|nhan vien moi|nguoi moi|"
              r"team khac|phong ban khac|ben khach|ca cong ty|toan cong ty|nha dau tu|hoi dong quan tri|"
              r"ban lanh dao|pm)\b|\b(tai lieu|ban|file|slide|bai|noi dung)\b[^.?!\n]{0,30}\bde chia se\b|"
              r"\bban tom tat cho\b|\bbrief\b|\btai lieu (gioi thieu|onboarding)\b")
# Sau khi bỏ dấu nhiều động từ một âm tiết trùng với từ thường (Việt, chính, lặp, đích), nên chỉ giữ dạng an toàn.
VERB = rx(r"(?<!tieng )\bviet\b(?! nam)|\b(soan|tao|lam|sua|chinh sua|bien tap|trau chuot|ra soat|cap nhat|"
          r"tom tat|hoan thien|draft|chuyen thanh)\b|"
          r"\blap(?= (bao cao|ke hoach|bien ban|to trinh|de an|du toan)\b)|\bdich(?= (sang|ra|bai|tai lieu|van ban)\b)")
TONE = rx(r"\b(giong (ai|may|chatgpt)|van (may|dich)|(cho|nghe|doc) (tu nhien|giong nguoi)|"
          r"khop giong|(theo|thong nhat|khop) van phong)\b")
OPT_OUT = rx(r"\b(khong|dung|tat|bo qua|khoi|bo) (dung |can )?stop-?slop|stop-?slop.{0,15}\b(khong|tat|bo qua)\b|"
             r"\bgiu nguyen (van phong|cau chu|loi van)\b|\bkhong sua cau chu\b")
# Văn tự sự. "bài báo" không phải "bài báo cáo"; "đoạn văn" không phải "đoạn văn bản".
PROSE = rx(r"\b(tieu luan|bai luan|bai thu hoach|bai cam nhan|blog|bai bao(?! cao)|"
           r"bai viet|bai dang|binh luan|bai tap lon|luan van|khoa luan|thu xin viec|cover letter|"
           r"doan van(?! ban)|van xuoi|bai van|van tu su)\b")
# Động từ và từ khóa tài liệu phải cách nhau không quá bấy nhiêu từ.
NEAR_WORDS = 6
CODE_NEAR_WORDS = 2

# Thông báo task nền và báo cáo của subagent đến dưới dạng prompt mở bằng các thẻ này.
NOTICE_HEAD = ("<task-notification>", "<agent-message")
NOTICE_BLOCK = re.compile(r"<(task-notification|agent-message)\b.*?</\1>", re.S)

# Tính từ gốc plugin: skills/stop-slop-vi/scripts/slop_scan.py cạnh thư mục hooks/
SCANNER = (Path(__file__).resolve().parent.parent / "skills" / "stop-slop-vi" / "scripts" / "slop_scan.py").as_posix()
# Gợi ý chính interpreter đang chạy hook (máy chỉ có python3 có thể không có `python`)
PYTHON = Path(sys.executable).as_posix() if sys.executable else "python3"
SCAN = f"`\"{PYTHON}\" \"{SCANNER}\" <file>`"
SCAN_PROSE = f"`\"{PYTHON}\" \"{SCANNER}\" --prose <file>`"
MESSAGES = {
    "brief": (
        "[Điều hướng skill tài liệu] Nhận diện là tài liệu chia sẻ cho đối tượng đọc cụ thể (từ khóa: {kw}). "
        "Thứ tự: 1) nếu có skill stakeholder-brief thì nạp trước để chọn góc nhìn đối tượng và loại tài liệu "
        "(đồng thuận/hướng dẫn), dựng cấu trúc (không có thì bỏ qua bước này). 2) Câu chữ viết theo chuẩn "
        f"stop-slop-vi và áp làm lượt chỉnh giọng cuối. 3) Kiểm tra file kết quả bằng {SCAN} và báo PASS/FAIL. "
        "Nếu yêu cầu không viết tài liệu thì bỏ qua."
    ),
    "brief_explicit": (
        "[Điều hướng skill tài liệu] Gọi trực tiếp stakeholder-brief. Dựng cấu trúc xong thì áp stop-slop-vi "
        f"làm lượt chỉnh giọng cuối, kiểm tra bằng {SCAN} và báo PASS/FAIL."
    ),
    "slop": (
        "[stop-slop-vi tự áp dụng] Nhận diện là yêu cầu viết/sửa tài liệu tiếng Việt (từ khóa: {kw}). "
        "Trước khi viết câu chữ tiếng Việt vào tài liệu, nạp skill stop-slop-vi và làm theo chế độ phù hợp "
        "(viết mới = tạo mới, sửa tài liệu có sẵn = làm sạch, theo văn phong tài liệu khác = khớp giọng). "
        f"Tạo file xong thì kiểm tra bằng {SCAN}, sửa hết WARN rồi báo kết quả (PASS/FAIL). "
        "Dùng cùng skill docx/pptx/xlsx. Nếu yêu cầu không viết chữ vào tài liệu (đọc, phân tích, code) thì bỏ qua."
    ),
    "prose": (
        "[stop-slop-vi tự áp dụng] Nhận diện là yêu cầu viết/sửa văn tự sự tiếng Việt "
        "(tiểu luận, blog, bình luận, thư xin việc; từ khóa: {kw}). Nạp skill stop-slop-vi, chọn văn phong tự sự "
        "và làm theo references/prose-patterns.md (viết mới = tạo mới, chỉnh sửa = làm sạch và không đổi xưng hô, "
        "theo văn phong bài khác = khớp giọng). Không bịa sự thật, luận điểm, nguồn. "
        f"Tạo file thì kiểm tra bằng {SCAN_PROSE} và báo kết quả (PASS/FAIL). Nếu yêu cầu không viết bài thì bỏ qua."
    ),
}


def words_between(folded, a, b):
    lo, hi = sorted([a, b], key=lambda m: m.start())
    return len(folded[lo.end():hi.start()].split())


def near(folded, verb_rx, target_rx, limit):
    """Một động từ và một từ khóa đứng cách nhau tối đa `limit` từ. Trả về match của từ khóa."""
    verbs = list(verb_rx.finditer(folded))
    for m in target_rx.finditer(folded):
        if any(words_between(folded, v, m) <= limit for v in verbs):
            return m
    return None


def route(prompt):
    """(loại, từ khóa có dấu) hoặc None."""
    if not isinstance(prompt, str):
        return None
    # Bỏ các khối thông báo, phần còn lại mới là yêu cầu người dùng. Mở bằng thẻ thông báo mà thiếu thẻ đóng cũng tính là thông báo.
    text = unicodedata.normalize("NFC", NOTICE_BLOCK.sub(" ", prompt))
    head = text.lstrip()
    if not head or head.startswith(NOTICE_HEAD):
        return None
    if head.startswith("/stop-slop-vi"):
        return None
    folded = fold(text)
    if OPT_OUT.search(folded):
        return None

    def kw(m):
        return text[m.start():m.end()]

    if head.startswith("/stakeholder-brief"):
        return "brief_explicit", "/stakeholder-brief"
    if CODE.search(folded):
        # Ngữ cảnh code: chỉ nhận khi động từ viết đi ngay với một loại tài liệu chắc chắn ("viết README").
        doc = near(folded, VERB, DOC_ONLY_RX, CODE_NEAR_WORDS)
        if not doc:
            return None
        aud = AUDIENCE.search(folded)
        return ("brief", kw(aud)) if aud else ("slop", kw(doc))
    verb = VERB.search(folded)
    aud = AUDIENCE.search(folded)
    if verb and aud:
        return "brief", kw(aud)
    tone = TONE.search(folded)
    prose = PROSE.search(folded) if tone else near(folded, VERB, PROSE, NEAR_WORDS)
    if prose:
        return "prose", kw(prose)
    if tone:
        return "slop", kw(tone)
    doc = near(folded, VERB, DOC_STRONG, NEAR_WORDS) or near(folded, VERB, DOC_WEAK, NEAR_WORDS)
    if doc:
        return "slop", kw(doc)
    return None


SELFTEST = [
    ("Soạn biên bản họp tuần này dạng docx", "slop"),
    ("viet bao cao thang 10", "slop"),
    ("Soạn công văn gửi Sở Tài chính", "slop"),
    ("Viết email trả lời khách", "slop"),
    ("Làm slide pptx cho buổi họp", "slop"),
    ("Bỏ giọng AI trong slide 14 đến 17", "slop"),
    ("Chương 3 viết theo văn phong chương 1", "slop"),
    ("Tóm tắt tài liệu thiết kế này cho lãnh đạo", "brief"),
    ("Làm bản brief cho khách hàng dạng HTML", "brief"),
    ("/stakeholder-brief thiet-ke.md cho khách hàng", "brief_explicit"),
    ("Viết tiểu luận về làm việc từ xa", "prose"),
    ("Sửa bài blog này", "prose"),
    ("Viết thư xin việc vị trí backend", "prose"),
    ("Viết bài báo cáo tổng kết năm", "slop"),
    ("Viết bài báo về chuyển đổi số", "prose"),
    ("Sửa bug build gradle", None),
    ("Tạo function gửi email trong code", None),
    ("Thêm bình luận vào code hàm này", None),
    ("Sửa thông báo lỗi khi đăng nhập", None),
    ("Làm API cho khách hàng", None),
    ("Đọc báo cáo này và trả lời bằng tiếng Việt", None),
    ("Viết script chuyển docx sang pdf", None),
    ("Viết hàm gửi thông báo cho người dùng", None),
    ("Viết README cho repo này", "slop"),
    ("soan thong bao loi nhuan quy 3", "slop"),
    ("Đọc file excel này rồi phân tích", None),
    ("Làm pptx nhưng không dùng stop-slop", None),
    ("/stop-slop-vi bao-cao.md", None),
    ("<task-notification> Đã soạn xong tài liệu chia sẻ </task-notification>", None),
]


def selftest():
    fails = 0
    for prompt, want in SELFTEST:
        got = route(prompt)
        got_kind = got[0] if got else None
        ok = got_kind == want
        fails += not ok
        print(f"{'ok  ' if ok else 'FAIL'} {str(got_kind):15} {prompt}")
    print(f"RESULT: {'PASS' if not fails else 'FAIL'} ({len(SELFTEST) - fails}/{len(SELFTEST)})")
    return 1 if fails else 0


def main():
    if "--selftest" in sys.argv:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.exit(selftest())
    try:
        hook = json.loads(sys.stdin.buffer.read().decode("utf-8", errors="replace"))
    except Exception:
        sys.exit(0)
    if not isinstance(hook, dict):
        sys.exit(0)
    hit = route(hook.get("prompt") or "")  # route() bỏ qua prompt không phải chuỗi
    if not hit:
        sys.exit(0)
    kind, kw = hit
    ctx = MESSAGES[kind].format(kw=kw)
    out = {"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": ctx}}
    # ensure_ascii: JSON thuần ASCII, an toàn với mọi code page của console
    sys.stdout.write(json.dumps(out))


if __name__ == "__main__":
    main()
