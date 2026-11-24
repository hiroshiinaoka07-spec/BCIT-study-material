"""Render image-only lecture pages and extract DOCX images into _wsa_extract/pages/."""
import zipfile
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "Window-server-admin"
OUT = ROOT / "_wsa_extract" / "pages"
OUT.mkdir(parents=True, exist_ok=True)

PAGES = {
    "Lectures/Module 2A Installation and Configuration.pdf": [7, 8, 9, 10, 11, 14, 22, 23, 25, 27, 32],
    "Lectures/ACIT3420 Domain Controller.pdf": [13, 20, 22, 24, 29, 30, 32, 34, 42, 43, 44],
    "Lectures/ACIT3420 Server Storage.pdf": [7, 8, 10, 11, 12, 13, 14],
    "Lectures/ACIT3420 DHCP.pdf": [11, 12, 13, 14],
    "Lectures/ACIT3420 DNS.pdf": [6, 7, 12, 16, 19, 20, 25, 27],
    "Lectures/IPv4 and IPv6.pdf": [8, 9, 11],
    "Lectures/Block Level Storage vs File Level Storage.pdf": [1, 2, 3, 4, 5, 6],
    "Lectures/Hyper-V Snapshots vs Snapshot Explained.pdf": [1, 2, 3, 4, 5, 6, 7, 8],
    "Lectures/Windows Server Introduction.pdf": [16, 25],
}
DOCX = [
    "Lectures/DNS Topics.docx",
    "Lectures/Nested Virtualization.docx",
    "Labs/Lab - Copy (9)/DNS+Namespace+Design+for+Adatum.com.docx",
]

for rel, pages in PAGES.items():
    stem = Path(rel).stem.replace(" ", "_")[:30]
    with pymupdf.open(SRC / rel) as doc:
        for p in pages:
            pix = doc[p - 1].get_pixmap(dpi=110)
            pix.save(OUT / f"{stem}_p{p:02d}.png")

for rel in DOCX:
    stem = Path(rel).stem.replace(" ", "_").replace("+", "_")[:30]
    with zipfile.ZipFile(SRC / rel) as z:
        for n in z.namelist():
            if n.startswith("word/media/"):
                (OUT / f"{stem}_{Path(n).name}").write_bytes(z.read(n))

for f in sorted(OUT.iterdir()):
    print(f.stat().st_size, f.name)
