#!/bin/sh
# Chọn interpreter Python có sẵn rồi chạy hook điều hướng tài liệu (macOS/Linux=python3, Windows=python).
# Không có Python thì kết thúc, không chèn gì.
dir=$(dirname "$0")
for py in python3 python; do
  if command -v "$py" >/dev/null 2>&1 && "$py" -c "import sys" </dev/null >/dev/null 2>&1; then
    exec "$py" "$dir/stop-slop-doc-reminder.py"
  fi
done
exit 0
