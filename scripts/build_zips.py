# -*- coding: utf-8 -*-
"""Đóng gói plugin thành file zip để cài trên claude.ai mà không cần dòng lệnh.

Mỗi plugin trong plugins/ tạo ra hai file:
  <tên>-skill.zip   thư mục skill ở gốc zip, dùng cho Customize > Skills > Upload a skill
  <tên>-plugin.zip  .claude-plugin/plugin.json ở gốc zip, dùng cho Customize > Plugins > Upload plugin

usage: python scripts/build_zips.py [--out dist]
"""
import argparse
import sys
import zipfile
from pathlib import Path

SKIP_DIRS = {"__pycache__", ".pytest_cache"}
SKIP_SUFFIXES = {".pyc", ".pyo"}
SKIP_NAMES = {".DS_Store", "Thumbs.db"}
# Ngày cố định để cùng nội dung cho ra cùng một file zip
FIXED_TIME = (2026, 1, 1, 0, 0, 0)


def files_under(folder):
    for p in sorted(folder.rglob("*")):
        if not p.is_file() or p.name in SKIP_NAMES or p.suffix in SKIP_SUFFIXES:
            continue
        if SKIP_DIRS.intersection(p.relative_to(folder).parts):
            continue
        yield p


def write_zip(target, entries):
    """entries: [(đường dẫn trong zip, file nguồn)]."""
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as z:
        for arcname, src in entries:
            info = zipfile.ZipInfo(arcname, FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            # Đổi CRLF thành LF cho file văn bản để zip giống nhau trên Windows và macOS/Linux
            data = src.read_bytes()
            if src.suffix in {".md", ".py", ".json", ".sh", ".txt", ".html"}:
                data = data.replace(b"\r\n", b"\n")
            z.writestr(info, data)
    return target


def build(root, out):
    root, out = Path(root), Path(out)
    out.mkdir(parents=True, exist_ok=True)
    built = []
    for plugin in sorted(p for p in (root / "plugins").iterdir() if (p / ".claude-plugin" / "plugin.json").is_file()):
        name = plugin.name
        built.append(write_zip(out / f"{name}-plugin.zip",
                               [(f.relative_to(plugin).as_posix(), f) for f in files_under(plugin)]))
        for skill in sorted(d for d in (plugin / "skills").iterdir() if (d / "SKILL.md").is_file()):
            built.append(write_zip(out / f"{skill.name}-skill.zip",
                                   [(f"{skill.name}/{f.relative_to(skill).as_posix()}", f) for f in files_under(skill)]))
    return sorted(built)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default="dist", help="thư mục chứa file zip (mặc định: dist)")
    args = ap.parse_args()
    root = Path(__file__).resolve().parent.parent
    try:
        built = build(root, root / args.out if not Path(args.out).is_absolute() else args.out)
    except OSError as e:
        print(f"Lỗi khi đóng gói: {e}", file=sys.stderr)
        sys.exit(1)
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    for p in built:
        print(f"{p.name}: {p.stat().st_size:,} byte")


if __name__ == "__main__":
    main()
