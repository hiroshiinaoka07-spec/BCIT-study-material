"""Tile sampled frames from silent lab videos into 2x2 contact sheets in _wsa_extract/sheets/."""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
TR = ROOT / "transcripts"
OUT = ROOT / "_wsa_extract" / "sheets"
OUT.mkdir(parents=True, exist_ok=True)

VIDEOS = {
    "DHCP": 8, "DHCP Failover": 16, "DHCP Relay Agent (Challenge)": 16, "DNS Lab": 16,
    "Group Nesting": 8, "How to Install the Second Domain Controller": 12,
    "How to install and configure subdomain": 12, "How to install and configure a domain tree controller": 12,
    "How to fix your client lost the trust relationship witht your domain": 12,
    "add another server to manage": 8, "Remove Client from Domain": 4,
    "Storage Pool and iSCSI Server": 16, "Hyper-V": 16, "PStools installation and comments for psgetsid": 12,
    "Windows 2016 Server Core Installation and Configuration": 16,
    "Windows Server 2022 Domain Controller Installation": 12,
    "How to configure Second Domain SubDomain and Domain Tree": 20, "Lenovo Server IMM": 8,
    "Install Widnows Server 2022": 8, "Virtualbox Configurations": 4, "Virtualbox Clone Machine": 4,
    "Windows 10 Installation": 4,
}
CELL_W = 960


def sample(frames, n):
    if len(frames) <= n:
        return frames
    step = (len(frames) - 1) / (n - 1)
    return [frames[round(i * step)] for i in range(n)]


for name, n in VIDEOS.items():
    frames = sorted((TR / name / "frames").glob("*.jpg"))
    if not frames:
        print("missing", name, file=sys.stderr)
        continue
    picks = sample(frames, n)
    slug = "".join(c if c.isalnum() else "_" for c in name)[:40]
    for s in range(0, len(picks), 4):
        group = picks[s:s + 4]
        ims = [Image.open(p).convert("RGB") for p in group]
        ims = [im.resize((CELL_W, round(im.height * CELL_W / im.width))) for im in ims]
        cell_h = max(im.height for im in ims)
        sheet = Image.new("RGB", (CELL_W * 2, cell_h * 2), "white")
        d = ImageDraw.Draw(sheet)
        for i, (im, p) in enumerate(zip(ims, group)):
            x, y = (i % 2) * CELL_W, (i // 2) * cell_h
            sheet.paste(im, (x, y))
            d.rectangle([x, y, x + 150, y + 22], fill="yellow")
            d.text((x + 4, y + 4), p.stem, fill="black")
        out = OUT / f"{slug}_{s // 4 + 1:02d}.jpg"
        sheet.save(out, quality=85)
    print(name, len(picks))
