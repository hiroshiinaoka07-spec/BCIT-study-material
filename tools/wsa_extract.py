"""Dump text from every PDF/DOCX/PPTX in Window-server-admin into _wsa_extract/."""
import re
import sys
import zipfile
from pathlib import Path

import pymupdf
import docx

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "Window-server-admin"
OUT = ROOT / "_wsa_extract"
OUT.mkdir(exist_ok=True)


def pdf_text(p):
    with pymupdf.open(p) as d:
        return "\n".join(f"--- page {i+1} ---\n{pg.get_text()}" for i, pg in enumerate(d))


def docx_text(p):
    d = docx.Document(p)
    parts = [para.text for para in d.paragraphs]
    for t in d.tables:
        for row in t.rows:
            parts.append(" | ".join(c.text for c in row.cells))
    return "\n".join(parts)


def pptx_text(p):
    parts = []
    with zipfile.ZipFile(p) as z:
        slides = sorted(
            (n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml", n)),
            key=lambda n: int(re.findall(r"\d+", n)[0]),
        )
        for n in slides:
            xml = z.read(n).decode("utf8")
            paras = re.findall(r"<a:p>(.*?)</a:p>", xml, re.S)
            lines = ["".join(re.findall(r"<a:t>(.*?)</a:t>", pp)) for pp in paras]
            parts.append(f"--- {n} ---\n" + "\n".join(l for l in lines if l))
    return "\n".join(parts)


seen = set()
for f in sorted(SRC.rglob("*")):
    ext = f.suffix.lower()
    if ext not in (".pdf", ".docx", ".pptx", ".html"):
        continue
    key = (f.name, f.stat().st_size)
    if key in seen:
        continue
    seen.add(key)
    try:
        if ext == ".pdf":
            txt = pdf_text(f)
        elif ext == ".docx":
            txt = docx_text(f)
        elif ext == ".pptx":
            txt = pptx_text(f)
        else:
            txt = re.sub(r"<[^>]+>", " ", f.read_text(encoding="utf8", errors="ignore"))
    except Exception as e:  # noqa: BLE001
        print("FAIL", f, e, file=sys.stderr)
        continue
    rel = f.relative_to(SRC)
    name = re.sub(r"[^\w.-]+", "_", str(rel)) + ".txt"
    (OUT / name).write_text(txt, encoding="utf8")
    print(f"{len(txt):>8}  {name}")
