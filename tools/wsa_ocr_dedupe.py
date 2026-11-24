"""Collapse per-frame OCR text into unique, sentence-like lines per video."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OCR = ROOT / "_wsa_extract" / "ocr"
NOISE = re.compile(
    r"^(File|Edit|View|VM|Tabs|Help|Home|Library|My Computer|Server Manager|Dashboard|Local Server|All Servers|"
    r"Manage|Tools|Notifications|TASKS|PROPERTIES|EVENTS|SERVICES|Filter|Shared VMs|Type here to search)\b",
    re.I,
)

for f in sorted(OCR.glob("*.txt")):
    if f.name.endswith(".uniq.txt"):
        continue
    seen, out = set(), []
    for line in f.read_text(encoding="utf8", errors="ignore").splitlines():
        s = line.strip()
        if s.startswith("====="):
            out.append(s)
            continue
        if len(s) < 14 or " " not in s or NOISE.match(s):
            continue
        key = re.sub(r"\W+", "", s.lower())
        if key in seen:
            continue
        seen.add(key)
        out.append(s)
    cleaned = [l for i, l in enumerate(out) if not (l.startswith("=====") and (i + 1 == len(out) or out[i + 1].startswith("=====")))]
    (OCR / (f.stem + ".uniq.txt")).write_text("\n".join(cleaned), encoding="utf8")
    print(f"{len(cleaned):>5}  {f.stem}")
